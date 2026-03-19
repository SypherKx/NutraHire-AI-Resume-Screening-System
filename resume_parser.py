import PyPDF2
import io

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from a PDF file uploaded via Streamlit.
    
    Args:
        uploaded_file: A Streamlit UploadedFile object (PDF)
    
    Returns:
        Cleaned text string from the PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text_parts = []

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        # Reset file pointer for potential re-reads
        uploaded_file.seek(0)

        full_text = "\n".join(text_parts)
        # Clean up excessive whitespace
        lines = [line.strip() for line in full_text.splitlines() if line.strip()]
        return "\n".join(lines)

    except Exception as e:
        return f"[Error extracting text: {str(e)}]"
