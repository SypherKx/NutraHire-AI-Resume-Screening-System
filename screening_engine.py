import json
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

def configure_groq(api_key: str = None):
    """Configure the Groq API client."""
    global _client
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("Please provide a valid Groq API key.")
    _client = Groq(api_key=key)

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze a single resume against a job description using Groq (Llama 3.3 70B).
    
    Args:
        resume_text: Extracted text from the resume PDF
        job_description: The job description text
    
    Returns:
        Dictionary with: candidate_name, match_score, strengths, gaps, recommendation
    """
    global _client
    if not _client:
        configure_groq()

    prompt = f"""You are an expert HR recruiter and resume screening specialist.

Analyze the following resume against the provided job description. Evaluate the candidate thoroughly and provide a structured assessment.

---
JOB DESCRIPTION:
{job_description}
---

---
RESUME:
{resume_text}
---

You MUST respond with ONLY a valid JSON object (no markdown, no code blocks, no extra text) in this exact format:
{{
    "candidate_name": "Full name of the candidate (extract from resume, use 'Unknown' if not found)",
    "match_score": <integer from 0 to 100>,
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "gaps": ["gap 1", "gap 2", "gap 3"],
    "recommendation": "<one of: Strong Fit, Moderate Fit, Not Fit>"
}}

SCORING GUIDELINES:
- 80-100: Strong Fit — candidate meets most/all key requirements
- 50-79: Moderate Fit — candidate meets some requirements but has notable gaps
- 0-49: Not Fit — candidate lacks critical requirements

For strengths and gaps:
- Provide exactly 2-3 points each
- Be specific and reference actual skills/experience from the resume
- Compare directly against job description requirements

Respond with ONLY the JSON object, nothing else."""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = _client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert HR recruiter. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024,
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code block if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                lines = [l for l in lines if not l.strip().startswith("```")]
                response_text = "\n".join(lines)
            
            result = json.loads(response_text)
            
            # Validate and sanitize
            result["match_score"] = max(0, min(100, int(result.get("match_score", 0))))
            result["strengths"] = result.get("strengths", ["N/A"])[:3]
            result["gaps"] = result.get("gaps", ["N/A"])[:3]
            
            if result.get("recommendation") not in ("Strong Fit", "Moderate Fit", "Not Fit"):
                score = result["match_score"]
                if score >= 80:
                    result["recommendation"] = "Strong Fit"
                elif score >= 50:
                    result["recommendation"] = "Moderate Fit"
                else:
                    result["recommendation"] = "Not Fit"
            
            return result

        except json.JSONDecodeError:
            return {
                "candidate_name": "Parse Error",
                "match_score": 0,
                "strengths": ["Could not parse response"],
                "gaps": ["LLM response was not valid JSON"],
                "recommendation": "Not Fit"
            }
        except Exception as e:
            error_msg = str(e)
            if ("429" in error_msg or "rate" in error_msg.lower()) and attempt < max_retries - 1:
                wait_time = 5 * (2 ** attempt)
                time.sleep(wait_time)
                continue
            return {
                "candidate_name": "Error",
                "match_score": 0,
                "strengths": ["Error occurred during analysis"],
                "gaps": [error_msg[:100]],
                "recommendation": "Not Fit"
            }

def rank_candidates(results: list[dict]) -> list[dict]:
    """Sort candidates by match score (highest first) and add rank numbers."""
    sorted_results = sorted(results, key=lambda x: x.get("match_score", 0), reverse=True)
    for i, candidate in enumerate(sorted_results, 1):
        candidate["rank"] = i
    return sorted_results
