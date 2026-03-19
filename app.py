import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
from resume_parser import extract_text_from_pdf
from screening_engine import configure_groq, analyze_resume, rank_candidates

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# PAGE CONFIG
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS — Premium AI-themed dark UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #111111;
        color: #e6edf3;
    }

    header[data-testid="stHeader"] {
        background-color: #111111 !important;
    }
    .stToolbar {
        background-color: #111111 !important;
    }
    div[data-testid="stToolbar"] {
        background-color: #111111 !important;
    }
    div[data-testid="stDecoration"] {
        background-image: none !important;
        background-color: #111111 !important;
    }
    .stDeployButton {
        background-color: #111111 !important;
    }
    div[data-testid="stStatusWidget"] {
        background-color: #111111 !important;
    }
    #MainMenu {
        color: #8b949e !important;
    }

    .hero-header {
        background: linear-gradient(135deg, #1a1a1a, #1e2028, #111111);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(48, 54, 61, 0.8);
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .hero-header h1 {
        color: #e6edf3;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-header .accent {
        background: linear-gradient(90deg, #58a6ff, #3fb950, #58a6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-header p {
        color: #8b949e;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    .metrics-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        flex: 1;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #58a6ff;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }

    .results-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #30363d;
        box-shadow: 0 4px 25px rgba(0,0,0,0.3);
        margin-top: 1rem;
    }
    .results-table thead th {
        background: #161b22;
        color: #8b949e;
        padding: 14px 16px;
        text-align: left;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #30363d;
    }
    .results-table tbody tr {
        transition: all 0.2s ease;
    }
    .results-table tbody tr:nth-child(even) {
        background: rgba(22, 27, 34, 0.6);
    }
    .results-table tbody tr:nth-child(odd) {
        background: rgba(17, 17, 17, 0.8);
    }
    .results-table tbody tr:hover {
        background: rgba(48, 54, 61, 0.4);
    }
    .results-table td {
        padding: 14px 16px;
        color: #e6edf3;
        font-size: 0.9rem;
        border-bottom: 1px solid #21262d;
        vertical-align: top;
    }

    .score-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 1.1rem;
    }
    .score-high {
        background: rgba(63, 185, 80, 0.12);
        color: #3fb950;
        border: 2px solid rgba(63, 185, 80, 0.4);
    }
    .score-mid {
        background: rgba(210, 153, 34, 0.12);
        color: #d29922;
        border: 2px solid rgba(210, 153, 34, 0.4);
    }
    .score-low {
        background: rgba(248, 81, 73, 0.12);
        color: #f85149;
        border: 2px solid rgba(248, 81, 73, 0.4);
    }

    .rec-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .rec-strong {
        background: rgba(63, 185, 80, 0.12);
        color: #3fb950;
        border: 1px solid rgba(63, 185, 80, 0.3);
    }
    .rec-moderate {
        background: rgba(210, 153, 34, 0.12);
        color: #d29922;
        border: 1px solid rgba(210, 153, 34, 0.3);
    }
    .rec-not {
        background: rgba(248, 81, 73, 0.12);
        color: #f85149;
        border: 1px solid rgba(248, 81, 73, 0.3);
    }

    section[data-testid="stSidebar"] {
        background: #111111;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] .stTextArea textarea {
        background: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] .stFileUploader {
        border: 2px dashed #30363d;
        border-radius: 12px;
        padding: 0.5rem;
    }

    .detail-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 15px rgba(0,0,0,0.25);
    }
    .detail-card h3 {
        color: #e6edf3;
        font-size: 1.1rem;
        margin: 0 0 1rem 0;
    }
    .detail-card .detail-row {
        display: flex;
        gap: 2rem;
    }
    .detail-card .detail-col {
        flex: 1;
    }
    .detail-card .detail-col h4 {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .detail-card .strength-label { color: #3fb950; }
    .detail-card .gap-label { color: #f85149; }
    .detail-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    .detail-card ul li {
        color: #c9d1d9;
        font-size: 0.88rem;
        padding: 4px 0;
        padding-left: 16px;
        position: relative;
    }
    .detail-card ul.strengths li::before {
        content: "\u2713";
        position: absolute;
        left: 0;
        color: #3fb950;
        font-weight: 700;
    }
    .detail-card ul.gaps li::before {
        content: "\u2717";
        position: absolute;
        left: 0;
        color: #f85149;
        font-weight: 700;
    }

    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(35, 134, 54, 0.5) !important;
    }

    /* download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3) !important;
    }

    .rank-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(88, 166, 255, 0.12);
        color: #58a6ff;
        font-weight: 800;
        font-size: 0.95rem;
        border: 1px solid rgba(88, 166, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# HERO HEADER
st.markdown("""
<div class="hero-header">
    <h1>🎯 <span class="accent">AI Resume</span> Screening System</h1>
    <p>Upload resumes, paste a job description, and let AI rank your candidates instantly</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR — Inputs
with st.sidebar:
    
    st.markdown("### 📋 Job Description")
    
    job_description = st.text_area(
        "Paste the Job Description",
        height=250,
        placeholder="Paste the complete job description here...\n\nExample:\nWe are looking for a Data Analyst with 2+ years of experience in Python, SQL, and data visualization tools like Tableau or Power BI..."
    )
    
    st.markdown("---")
    st.markdown("### 📄 Upload Resumes")
    
    uploaded_files = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload up to 10 resume PDFs"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} resume(s) uploaded")
    
    st.markdown("---")
    
    screen_btn = st.button("🚀 Screen Resumes", use_container_width=True)

# MAIN AREA — Processing & Results

if "results" not in st.session_state:
    st.session_state.results = None

if screen_btn:
    if not job_description.strip():
        st.error("⚠️ Please paste a job description in the sidebar.")
    elif not uploaded_files:
        st.error("⚠️ Please upload at least one resume PDF.")
    elif not GROQ_API_KEY:
        st.error("⚠️ API key not found. Please add your Groq API key to the .env file.")
    else:
        try:
            configure_groq(GROQ_API_KEY)
        except ValueError as e:
            st.error(f"⚠️ API Key Error: {str(e)}")
            st.stop()
        
        results = []
        progress_bar = st.progress(0, text="Initializing AI screening engine...")
        status_container = st.empty()
        
        for i, file in enumerate(uploaded_files):
            progress = (i) / len(uploaded_files)
            progress_bar.progress(progress, text=f"📄 Analyzing resume {i+1}/{len(uploaded_files)}: {file.name}")
            
            status_container.info(f"🔍 Extracting text from **{file.name}**...")
            resume_text = extract_text_from_pdf(file)
            
            if resume_text.startswith("[Error"):
                results.append({
                    "candidate_name": file.name,
                    "match_score": 0,
                    "strengths": ["Could not read PDF"],
                    "gaps": ["File may be corrupted or image-based"],
                    "recommendation": "Not Fit"
                })
                continue
            
            status_container.info(f"🤖 AI is evaluating **{file.name}** against the job description...")
            result = analyze_resume(resume_text, job_description)
            result["file_name"] = file.name
            results.append(result)
            
            time.sleep(1)  # Small delay between calls
        
        progress_bar.progress(1.0, text="✅ Screening complete!")
        status_container.empty()
        
        ranked_results = rank_candidates(results)
        st.session_state.results = ranked_results
        
        time.sleep(0.5)
        st.rerun()

# DISPLAY RESULTS
if st.session_state.results:
    results = st.session_state.results
    
    total = len(results)
    avg_score = sum(r["match_score"] for r in results) / total if total > 0 else 0
    strong_fits = sum(1 for r in results if r["recommendation"] == "Strong Fit")
    moderate_fits = sum(1 for r in results if r["recommendation"] == "Moderate Fit")
    
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card">
            <div class="metric-value">{total}</div>
            <div class="metric-label">Total Candidates</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{avg_score:.0f}</div>
            <div class="metric-label">Average Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{strong_fits}</div>
            <div class="metric-label">Strong Fits</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{moderate_fits}</div>
            <div class="metric-label">Moderate Fits</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Candidate Rankings")
    
    def get_score_class(score):
        if score >= 80: return "score-high"
        if score >= 50: return "score-mid"
        return "score-low"
    
    def get_rec_class(rec):
        if rec == "Strong Fit": return "rec-strong"
        if rec == "Moderate Fit": return "rec-moderate"
        return "rec-not"
    
    table_html = """<table class="results-table">
    <thead>
        <tr>
            <th>Rank</th>
            <th>Candidate</th>
            <th>Score</th>
            <th>Strengths</th>
            <th>Gaps</th>
            <th>Recommendation</th>
        </tr>
    </thead>
    <tbody>"""
    
    for r in results:
        strengths_html = "<br>".join([f"✓ {s}" for s in r.get("strengths", [])])
        gaps_html = "<br>".join([f"✗ {g}" for g in r.get("gaps", [])])
        
        table_html += f"""
        <tr>
            <td><span class="rank-num">{r.get('rank', '-')}</span></td>
            <td><strong>{r.get('candidate_name', 'Unknown')}</strong></td>
            <td><span class="score-badge {get_score_class(r['match_score'])}">{r['match_score']}</span></td>
            <td style="color: #86efac; font-size: 0.85rem;">{strengths_html}</td>
            <td style="color: #fca5a5; font-size: 0.85rem;">{gaps_html}</td>
            <td><span class="rec-badge {get_rec_class(r.get('recommendation', 'Not Fit'))}">{r.get('recommendation', 'Not Fit')}</span></td>
        </tr>"""
    
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("### 🔎 Detailed Analysis")
    
    for r in results:
        strengths_items = "".join([f"<li>{s}</li>" for s in r.get("strengths", [])])
        gaps_items = "".join([f"<li>{g}</li>" for g in r.get("gaps", [])])
        
        st.markdown(f"""
        <div class="detail-card">
            <h3>#{r.get('rank', '-')} — {r.get('candidate_name', 'Unknown')}
                <span class="score-badge {get_score_class(r['match_score'])}" style="margin-left: 12px; width: 42px; height: 42px; font-size: 0.95rem;">{r['match_score']}</span>
                <span class="rec-badge {get_rec_class(r.get('recommendation', 'Not Fit'))}" style="margin-left: 8px;">{r.get('recommendation', 'Not Fit')}</span>
            </h3>
            <div class="detail-row">
                <div class="detail-col">
                    <h4 class="strength-label">✓ Key Strengths</h4>
                    <ul class="strengths">{strengths_items}</ul>
                </div>
                <div class="detail-col">
                    <h4 class="gap-label">✗ Key Gaps</h4>
                    <ul class="gaps">{gaps_items}</ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    export_data = []
    for r in results:
        export_data.append({
            "Rank": r.get("rank", ""),
            "Candidate": r.get("candidate_name", "Unknown"),
            "Score": r.get("match_score", 0),
            "Strengths": " | ".join(r.get("strengths", [])),
            "Gaps": " | ".join(r.get("gaps", [])),
            "Recommendation": r.get("recommendation", "")
        })
    
    df = pd.DataFrame(export_data)
    csv_data = df.to_csv(index=False)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name="screening_results.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: #8b949e;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📄 → 🤖 → 📊</div>
        <h3 style="color: #e6edf3; font-weight: 600;">Ready to Screen Candidates</h3>
        <p style="max-width: 500px; margin: 0.5rem auto; line-height: 1.6;">
            1. Paste your <strong style="color: #58a6ff;">Job Description</strong> in the sidebar<br>
            2. Upload <strong style="color: #58a6ff;">Resume PDFs</strong> (up to 10)<br>
            3. Click <strong style="color: #58a6ff;">Screen Resumes</strong> and let AI do the work
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: #4b5563; font-size: 0.8rem;">
    Built with Streamlit &amp; Groq AI | AI Resume Screening System
</div>
""", unsafe_allow_html=True)
