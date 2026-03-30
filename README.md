# AI Resume Screening System - NutraHire

An AI-powered resume screening platform that evaluates multiple resumes against a job description in seconds and produces structured, ranked candidate assessments.

## Features

- **Smart Resume Parsing** — Extracts text from PDF resumes automatically using `PyPDF2`.
- **Ultra-Fast AI Analysis** — Uses **Groq API (Llama-3.3-70b-versatile)** to evaluate each resume against the JD, ensuring near-instant results.
- **Structured Output** — Provides a Match Score (0–100), 3 Key Strengths, 3 Key Gaps, and a final Recommendation.
- **Candidate Ranking** — Candidates are dynamically sorted by match score (highest first).
- **Vercel-Ready Architecture** — Built with a serverless Python Flask backend and a responsive Vanilla HTML/CSS/JS frontend replicating a premium dark UI.

## Output Format

| Rank | Candidate | Score | Strengths | Gaps | Recommendation |
|------|-----------|-------|-----------|------|----------------|
| 1 | Candidate A | 85 | Strong SQL, Tableau expert | Limited cloud exp | Strong Fit |
| 2 | Candidate B | 62 | Good Python | No visualization tools | Moderate Fit |
| 3 | Candidate C | 28 | Creative design skills | No data/SQL skills | Not Fit |

## Tech Stack

- **Frontend** — HTML5, CSS3 (Custom Premium Dark Theme), Vanilla JS
- **Backend Framework** — Python 3, Flask (Vercel Serverless Functions)
- **AI / LLM** — Groq API (Llama 3.3 70B Model)
- **PDF Processing** — PyPDF2

## Setup & Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Run the Servers
Since this app separates the backend and frontend:

**Terminal 1 (Backend API):**
```bash
python api/index.py
# Server will run on http://127.0.0.1:5000
```

**Terminal 2 (Frontend UI):**
```bash
python -m http.server 8505
# Open your browser and go to http://localhost:8505
```

### 4. Use the App
1. Paste the **Job Description** in the sidebar.
2. Upload **resume PDFs** (you can accumulate up to 10 files before screening).
3. Click **Screen Resumes**.
4. View ranked results, scores, and individual analysis cards.

## Deployment on Vercel
This repository is configured out-of-the-box for deployment on **Vercel**.
1. Import the repository in Vercel.
2. Vercel will auto-detect the `vercel.json` routing configuration.
3. Add your `GROQ_API_KEY` to Vercel's Environment Variables.
4. Hit Deploy!

## Sample Data (Testing Edge-Cases)
The `sample_data/` folder contains a `job_description.txt` and 5 custom-tailored sample resumes to quickly test the application's ranking accuracy without hunting for real resumes.
You can regenerate or modify them via:
```bash
python generate_samples.py
```

## Scoring Criteria

| Score Range | Recommendation | Meaning |
|-------------|---------------|---------|
| 80–100 | Strong Fit | Meets most/all key requirements |
| 50–79 | Moderate Fit | Meets some requirements, has notable gaps |
| 0–49 | Not Fit | Lacks critical requirements |
