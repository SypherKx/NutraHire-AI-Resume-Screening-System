import os
import sys

# Add the parent directory (project root) to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import io

# Import the original business logic from the parent folder files
from resume_parser import extract_text_from_pdf
from screening_engine import configure_groq, analyze_resume, rank_candidates, generate_excel

load_dotenv()

# Get the parent directory (where index.html lives)
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=PARENT_DIR)
# Enable CORS for local cross-origin if needed
CORS(app, expose_headers=["Content-Disposition"])

@app.route('/')
def serve_index():
    return send_from_directory(PARENT_DIR, 'index.html')

@app.route('/favicon.svg')
def serve_favicon():
    return send_from_directory(PARENT_DIR, 'favicon.svg')

@app.route('/api/screen', methods=['POST'])
def screen():
    job_description = request.form.get("job_description", "")
    api_key = request.form.get("api_key", os.getenv("GROQ_API_KEY", ""))
    
    # In Flask, uploaded files are in request.files
    files = request.files.getlist("resumes")

    if not job_description.strip():
        return jsonify({"error": "Missing Job Description."}), 400
    if not files or len(files) == 0:
        return jsonify({"error": "Missing Resume PDFs."}), 400
    if not api_key:
        return jsonify({"error": "API Key is required."}), 400

    try:
        configure_groq(api_key)
    except Exception as e:
        return jsonify({"error": f"API Key Error: {str(e)}"}), 400

    results = []
    
    for file in files:
        if file.filename == '':
            continue
        
        # We can pass the FileStorage object directly to PyPDF2 via our existing parsing function,
        # because FileStorage has a .read() method simulating an open file!
        resume_text = extract_text_from_pdf(file)
        
        if resume_text.startswith("[Error"):
             results.append({
                 "candidate_name": file.filename,
                 "match_score": 0,
                 "strengths": ["Could not read PDF"],
                 "gaps": ["File may be corrupted or image-based"],
                 "recommendation": "Not Fit"
             })
             continue
             
        result = analyze_resume(resume_text, job_description)
        result["file_name"] = file.filename
        results.append(result)

    ranked_results = rank_candidates(results)
    
    # Calculate simple aggregate metrics for the dashboard
    total = len(ranked_results)
    avg_score = sum(r.get("match_score", 0) for r in ranked_results) / total if total > 0 else 0
    strong_fits = sum(1 for r in ranked_results if r.get("recommendation") == "Strong Fit")
    moderate_fits = sum(1 for r in ranked_results if r.get("recommendation") == "Moderate Fit")
    
    return jsonify({
        "results": ranked_results,
        "metrics": {
            "total": total,
            "avg_score": round(avg_score),
            "strong_fits": strong_fits,
            "moderate_fits": moderate_fits
        }
    })


@app.route('/api/export', methods=['POST'])
def export_excel():
    """
    Export screening results to Excel.
    Expects JSON body with 'results' array and optional 'job_description'.
    """
    data = request.get_json()

    if not data or 'results' not in data:
        return jsonify({"error": "Missing results data"}), 400

    results = data['results']
    job_description = data.get('job_description', '')

    if not isinstance(results, list) or len(results) == 0:
        return jsonify({"error": "Results must be a non-empty array"}), 400

    try:
        excel_bytes = generate_excel(results, job_description)

        # Create safe filename with timestamp
        from datetime import datetime
        from flask import make_response
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_screening_results_{timestamp}.xlsx"

        response = make_response(excel_bytes)
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return jsonify({"error": f"Excel generation failed: {str(e)}"}), 500

# Main block specifically for running the server locally on port 5000.
# On Vercel, the 'app' object exposed above is automatically used.
if __name__ == "__main__":
    app.run(port=5000, debug=True)
