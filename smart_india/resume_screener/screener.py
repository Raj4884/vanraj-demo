import docx
from PyPDF2 import PdfReader
import io

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def screen_resume(file):
    filename = file.filename
    content = ""
    if filename.endswith('.docx'):
        content = read_docx(io.BytesIO(file.read()))
    elif filename.endswith('.pdf'):
        content = read_pdf(io.BytesIO(file.read()))
    else:
        return {"error": "Unsupported file type"}

    # Placeholder for resume analysis
    # In a real application, this would use NLP to provide feedback
    return {
        "filename": filename,
        "content_length": len(content),
        "feedback": "This is a placeholder for resume feedback."
    }
