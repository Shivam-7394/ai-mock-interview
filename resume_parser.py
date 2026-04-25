import fitz
from docx import Document

def extract_text(file):
    if file.type == "application/pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        return " ".join([page.get_text() for page in pdf])

    elif "word" in file.type:
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    return ""