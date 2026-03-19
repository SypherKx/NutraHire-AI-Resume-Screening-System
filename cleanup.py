import sys
import re

files = [
    "c:/Users/itska/OneDrive/Desktop/Resume Tracker/app.py", 
    "c:/Users/itska/OneDrive/Desktop/Resume Tracker/screening_engine.py", 
    "c:/Users/itska/OneDrive/Desktop/Resume Tracker/resume_parser.py", 
    "c:/Users/itska/OneDrive/Desktop/Resume Tracker/generate_samples.py"
]

for f in files:
    try:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Remove top level docstrings (file description)
        content = re.sub(r'^"""\n(?:.*?\n)*?.*?"""\n+', '', content)
        
        # Remove the massive horizontal line comments
        content = re.sub(r'# ─+[^\n]*\n', '', content)
        
        # Remove specific headers with lines like # ── Some Text ──
        content = re.sub(r'# ──[^\n]*\n', '', content)
        
        # Remove the custom CSS comment dividers
        content = re.sub(r' +/\* ──.*?── \*/\n', '', content)
        
        # Remove typical AI descriptive comments like # Step 1: Extract text
        content = re.sub(r'# Step \d+: [^\n]*\n', '', content)
        
        # Also let's clean up consecutive blank lines caused by removed comments
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove some specific obvious AI comments
        content = content.replace("# Auto-load API key from .env\n", "")
        content = content.replace("# Show guide when nothing has been processed yet\n", "")
        content = content.replace("# Build HTML table\n", "")
        content = content.replace("# Initialize Groq client\n", "")
        
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Cleaned {f}")
    except Exception as e:
        print(f"Error on {f}: {e}")
