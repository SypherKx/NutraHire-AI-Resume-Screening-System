# AI Resume Screening System

An AI-powered resume screening tool that evaluates multiple resumes against a job description and produces structured, ranked candidate assessments.

## Features

- **Smart Resume Parsing** — Extracts text from PDF resumes automatically
- **AI-Powered Analysis** — Uses Google Gemini to evaluate each resume against the JD
- **Structured Output** — Match score (0–100), key strengths, key gaps, and recommendation
- **Candidate Ranking** — Candidates sorted by match score (highest first)
- **CSV Export** — Download results as a spreadsheet
- **Modern UI** — Clean, professional dark-themed interface

## Output Format

| Rank | Candidate | Score | Strengths | Gaps | Recommendation |
|------|-----------|-------|-----------|------|----------------|
| 1 | Candidate A | 85 | Strong SQL, Tableau expert | Limited cloud exp | Strong Fit |
| 2 | Candidate B | 62 | Good Python | No visualization tools | Moderate Fit |
| 3 | Candidate C | 28 | Creative design skills | No data/SQL skills | Not Fit |

## Tech Stack

- **Python** — Core language
- **Streamlit** — Web application framework
- **Google Gemini API** — LLM for resume analysis
- **PyPDF2** — PDF text extraction
- **pandas** — Data handling and CSV export

## Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Key
- Visit [Google AI Studio](https://aistudio.google.com/apikey)
- Generate a free API key
- You can enter it directly in the app sidebar

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Use the App
1. Paste your **API key** in the sidebar
2. Paste the **Job Description**
3. Upload **resume PDFs** (up to 10)
4. Click **Screen Resumes**
5. View ranked results and download CSV

## Sample Data

The `sample_data/` folder contains:
- `job_description.txt` — A Data Analyst JD for testing
- 5 sample resume PDFs with varying skill levels

To regenerate sample data:
```bash
python generate_samples.py
```

## Project Structure

```
Resume Tracker/
├── app.py                  # Main Streamlit application
├── resume_parser.py        # PDF text extraction module
├── screening_engine.py     # AI analysis engine (Gemini)
├── generate_samples.py     # Sample data generator
├── requirements.txt        # Python dependencies
├── .env                    # API key (gitignored)
├── .gitignore
├── README.md
└── sample_data/
    ├── job_description.txt
    ├── resume_ananya_sharma.pdf
    ├── resume_rahul_verma.pdf
    ├── resume_priya_patel.pdf
    ├── resume_vikram_singh.pdf
    └── resume_meera_joshi.pdf
```

## How It Works

1. **Input**: User provides a Job Description + uploads resume PDFs
2. **Parse**: PyPDF2 extracts text from each PDF
3. **Analyze**: Each resume is sent to Google Gemini with the JD for evaluation
4. **Score**: AI returns a structured JSON with score, strengths, gaps, and recommendation
5. **Rank**: Candidates are sorted by match score
6. **Output**: Results displayed in a ranked table with export option

## Scoring Criteria

| Score Range | Recommendation | Meaning |
|-------------|---------------|---------|
| 80–100 | Strong Fit | Meets most/all key requirements |
| 50–79 | Moderate Fit | Meets some requirements, has notable gaps |
| 0–49 | Not Fit | Lacks critical requirements |
