from fpdf import FPDF
import os

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def create_pdf(filename, lines_data):
    """Create a PDF. lines_data = list of (style, text) tuples."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    for style, text in lines_data:
        if style == "h1":
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        elif style == "h2":
            pdf.set_font("Helvetica", "B", 13)
            pdf.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")
        elif style == "blank":
            pdf.ln(4)
        else:
            pdf.set_font("Helvetica", "", 11)
            # Use cell for short lines, multi_cell for long ones
            if len(text) < 90:
                pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.multi_cell(0, 6, text)

    path = os.path.join(SAMPLE_DIR, filename)
    pdf.output(path)
    print(f"  Created: {filename}")

JD = (
    "Data Analyst - Job Description\n\n"
    "Company: TechNova Solutions\n"
    "Location: Bangalore, India (Hybrid)\n"
    "Experience: 2-4 years\n\n"
    "Role Overview:\n"
    "We are looking for a skilled Data Analyst to join our analytics team. "
    "The ideal candidate will transform raw data into actionable insights.\n\n"
    "Key Responsibilities:\n"
    "- Analyze large datasets using SQL and Python to identify trends\n"
    "- Build interactive dashboards using Tableau or Power BI\n"
    "- Collaborate with product and engineering teams to define KPIs\n"
    "- Perform A/B testing analysis and statistical modeling\n"
    "- Clean, validate, and preprocess data from multiple sources\n"
    "- Present findings to stakeholders through clear visualizations\n\n"
    "Required Skills:\n"
    "- Strong proficiency in SQL (complex queries, joins, window functions)\n"
    "- Python programming (pandas, numpy, matplotlib/seaborn)\n"
    "- Experience with Tableau or Power BI\n"
    "- Understanding of statistics and probability\n"
    "- Experience with A/B testing methodologies\n"
    "- Strong communication and presentation skills\n\n"
    "Preferred Skills:\n"
    "- Experience with cloud platforms (AWS/GCP)\n"
    "- Knowledge of machine learning basics\n"
    "- Experience with Excel/Google Sheets\n"
    "- Familiarity with Git version control\n\n"
    "Education:\n"
    "Bachelor's degree in CS, Statistics, Mathematics, or related field"
)

with open(os.path.join(SAMPLE_DIR, "job_description.txt"), "w", encoding="utf-8") as f:
    f.write(JD)
print("Created: job_description.txt")

create_pdf("resume_ananya_sharma.pdf", [
    ("h1", "Ananya Sharma"),
    ("body", "Email: ananya.sharma@email.com"),
    ("body", "Phone: +91-9876543210"),
    ("body", "LinkedIn: linkedin.com/in/ananyasharma"),
    ("body", "Location: Bangalore, India"),
    ("blank", ""),
    ("h2", "Professional Summary"),
    ("body", "Data Analyst with 3 years of experience in transforming"),
    ("body", "complex datasets into actionable business insights."),
    ("body", "Proficient in SQL, Python, and Tableau."),
    ("blank", ""),
    ("h2", "Work Experience"),
    ("body", "Data Analyst - Flipkart (2022 - Present)"),
    ("body", "- Analyzed customer behavior data using SQL and Python"),
    ("body", "  processing 10M+ daily records with pandas"),
    ("body", "- Built 15+ interactive Tableau dashboards for KPIs"),
    ("body", "- Designed and analyzed A/B tests, improving conversions by 12%"),
    ("body", "- Collaborated with PMs and engineers on metrics"),
    ("body", "- Automated weekly reporting with Python, saving 8hrs/week"),
    ("blank", ""),
    ("body", "Junior Data Analyst - Infosys (2021 - 2022)"),
    ("body", "- Wrote complex SQL with window functions and CTEs"),
    ("body", "- Cleaned and preprocessed data using Python pandas"),
    ("body", "- Created Power BI reports for client dashboards"),
    ("body", "- Performed statistical analysis on customer churn data"),
    ("blank", ""),
    ("h2", "Technical Skills"),
    ("body", "Languages: Python (pandas, numpy, matplotlib, seaborn), SQL"),
    ("body", "Visualization: Tableau, Power BI, Matplotlib"),
    ("body", "Tools: Jupyter Notebook, Git, Excel, Google Sheets"),
    ("body", "Cloud: AWS (S3, Redshift), basic GCP"),
    ("body", "Statistics: Hypothesis testing, A/B testing, regression"),
    ("blank", ""),
    ("h2", "Education"),
    ("body", "B.Tech in Computer Science - BITS Pilani (2021)"),
    ("body", "CGPA: 8.4"),
    ("blank", ""),
    ("h2", "Certifications"),
    ("body", "- Google Data Analytics Professional Certificate"),
    ("body", "- Tableau Desktop Specialist"),
])

create_pdf("resume_rahul_verma.pdf", [
    ("h1", "Rahul Verma"),
    ("body", "Email: rahul.verma@email.com"),
    ("body", "Phone: +91-9123456780"),
    ("body", "LinkedIn: linkedin.com/in/rahulverma"),
    ("body", "Location: Hyderabad, India"),
    ("blank", ""),
    ("h2", "Summary"),
    ("body", "Data-driven analyst with 2.5 years of experience in"),
    ("body", "SQL-heavy analytics roles. Passionate about turning data"),
    ("body", "into stories that influence product strategy."),
    ("blank", ""),
    ("h2", "Experience"),
    ("body", "Business Analyst - Swiggy (2023 - Present)"),
    ("body", "- Lead analyst for delivery optimization, 5M+ daily orders"),
    ("body", "- Built end-to-end Tableau dashboards for operations"),
    ("body", "- Conducted A/B tests on delivery fees, +8% order volume"),
    ("body", "- Advanced SQL (CTEs, window functions) on Snowflake"),
    ("blank", ""),
    ("body", "Data Analyst - Zoho Analytics (2021 - 2023)"),
    ("body", "- Analyzed product usage with Python and SQL for 50K+ users"),
    ("body", "- Developed automated data pipelines for ETL"),
    ("body", "- Created statistical models for customer segmentation"),
    ("body", "- Presented weekly insights to VP of Product"),
    ("blank", ""),
    ("h2", "Skills"),
    ("body", "SQL: PostgreSQL, Snowflake, MySQL (advanced level)"),
    ("body", "Python: pandas, numpy, scipy, scikit-learn, matplotlib"),
    ("body", "Visualization: Tableau (certified), Power BI, Looker"),
    ("body", "Statistics: A/B testing, hypothesis testing, regression"),
    ("body", "Tools: Git, Jupyter, Airflow, dbt"),
    ("body", "Cloud: GCP (BigQuery), AWS basics"),
    ("blank", ""),
    ("h2", "Education"),
    ("body", "B.Sc Statistics - ISI Kolkata (2021) - First Class"),
    ("blank", ""),
    ("h2", "Certifications"),
    ("body", "- Tableau Certified Data Analyst"),
    ("body", "- IBM Data Science Professional Certificate"),
])

create_pdf("resume_priya_patel.pdf", [
    ("h1", "Priya Patel"),
    ("body", "Email: priya.patel@email.com"),
    ("body", "Phone: +91-9988776655"),
    ("body", "LinkedIn: linkedin.com/in/priyapatel"),
    ("body", "Location: Mumbai, India"),
    ("blank", ""),
    ("h2", "About Me"),
    ("body", "Marketing analyst transitioning into data analytics."),
    ("body", "2 years of experience with data in marketing contexts."),
    ("body", "Strong Excel skills and learning Python."),
    ("blank", ""),
    ("h2", "Work Experience"),
    ("body", "Marketing Analyst - Nykaa (2023 - Present)"),
    ("body", "- Analyzed campaign performance with Google Analytics"),
    ("body", "- Created reports with pivot tables and Excel formulas"),
    ("body", "- Used basic SQL to extract customer data"),
    ("body", "- Helped build campaign tracking dashboards"),
    ("blank", ""),
    ("body", "Marketing Executive - OYO Rooms (2022 - 2023)"),
    ("body", "- Tracked social media metrics and performance reports"),
    ("body", "- Used Google Sheets for budget tracking and ROI"),
    ("body", "- Assisted in customer segmentation using Excel"),
    ("blank", ""),
    ("h2", "Skills"),
    ("body", "Excel/Google Sheets: Advanced (VLOOKUP, pivot tables)"),
    ("body", "SQL: Basic to intermediate (SELECT, JOIN, GROUP BY)"),
    ("body", "Python: Beginner (completing online courses)"),
    ("body", "Tools: Google Analytics, HubSpot, Canva"),
    ("body", "Visualization: Basic Excel charts, learning Tableau"),
    ("blank", ""),
    ("h2", "Education"),
    ("body", "BBA in Marketing - Mumbai University (2022)"),
    ("body", "CGPA: 7.2"),
    ("blank", ""),
    ("h2", "Courses in Progress"),
    ("body", "- Python for Data Analysis (Coursera) - 60% complete"),
    ("body", "- SQL Bootcamp (Udemy) - Completed"),
])

create_pdf("resume_vikram_singh.pdf", [
    ("h1", "Vikram Singh"),
    ("body", "Email: vikram.singh@email.com"),
    ("body", "Phone: +91-9012345678"),
    ("body", "Location: Delhi, India"),
    ("body", "GitHub: github.com/vikramsingh"),
    ("blank", ""),
    ("h2", "Profile"),
    ("body", "Software developer with 3 years of backend experience."),
    ("body", "Strong in Python and databases. Looking to transition"),
    ("body", "into a data-focused role."),
    ("blank", ""),
    ("h2", "Experience"),
    ("body", "Backend Developer - Paytm (2022 - Present)"),
    ("body", "- Developed RESTful APIs using Python Flask and Django"),
    ("body", "- Designed and optimized PostgreSQL database schemas"),
    ("body", "- Wrote complex SQL queries for data migrations"),
    ("body", "- Built automated testing frameworks using pytest"),
    ("blank", ""),
    ("body", "Junior Developer - TCS (2021 - 2022)"),
    ("body", "- Worked on Java-based enterprise applications"),
    ("body", "- Used MySQL for database management"),
    ("body", "- Participated in Agile sprints and code reviews"),
    ("body", "- Created internal tools using Python scripting"),
    ("blank", ""),
    ("h2", "Technical Skills"),
    ("body", "Python: Flask, Django, pytest, requests (strong)"),
    ("body", "SQL: PostgreSQL, MySQL (advanced queries, optimization)"),
    ("body", "JavaScript: Basic React, Node.js"),
    ("body", "Cloud: AWS EC2, S3, RDS"),
    ("body", "Tools: Git, Docker, Jenkins, Linux"),
    ("blank", ""),
    ("h2", "Notes"),
    ("body", "- No experience with Tableau or Power BI"),
    ("body", "- Limited statistics/analytics background"),
    ("body", "- No A/B testing experience"),
    ("blank", ""),
    ("h2", "Education"),
    ("body", "B.Tech Computer Science - DTU, Delhi (2021)"),
    ("body", "CGPA 8.1"),
])

create_pdf("resume_meera_joshi.pdf", [
    ("h1", "Meera Joshi"),
    ("body", "Email: meera.joshi@email.com"),
    ("body", "Phone: +91-8765432190"),
    ("body", "Location: Pune, India"),
    ("blank", ""),
    ("h2", "Summary"),
    ("body", "Creative graphic designer with 4 years of experience"),
    ("body", "in brand identity and UI/UX design. Passionate about"),
    ("body", "visual storytelling and user-centered design."),
    ("blank", ""),
    ("h2", "Work Experience"),
    ("body", "Senior Graphic Designer - Freshworks (2022 - Present)"),
    ("body", "- Designed marketing collaterals and brand materials"),
    ("body", "- Created UI mockups using Figma"),
    ("body", "- Led the rebranding initiative for 3 product lines"),
    ("body", "- Managed a team of 2 junior designers"),
    ("blank", ""),
    ("body", "Graphic Designer - Zomato (2020 - 2022)"),
    ("body", "- Designed email templates, app banners, promotions"),
    ("body", "- Worked with marketing team on campaign visuals"),
    ("body", "- Created presentation decks for leadership"),
    ("blank", ""),
    ("h2", "Skills"),
    ("body", "Design: Photoshop, Illustrator, InDesign, Figma, Canva"),
    ("body", "UI/UX: Figma, Adobe XD, wireframing, prototyping"),
    ("body", "Video: Adobe Premiere Pro, After Effects (basic)"),
    ("body", "Other: Typography, color theory, brand identity"),
    ("blank", ""),
    ("h2", "Education"),
    ("body", "B.Des in Graphic Design - NID Ahmedabad (2020)"),
    ("blank", ""),
    ("h2", "Portfolio"),
    ("body", "behance.net/meerajoshi"),
])

print(f"\nAll sample files created in: {SAMPLE_DIR}")
print("You can now upload these PDFs in the app to test.")
