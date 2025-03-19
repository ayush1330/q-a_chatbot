# utils/file_utils.py

import os
from datetime import datetime
from PyPDF2 import PdfReader
import docx


def save_uploaded_file(uploaded_file):
    # Create 'data' directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create a unique file name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = os.path.splitext(uploaded_file.name)[1]
    file_name = f"resume_{timestamp}{file_extension}"
    file_path = os.path.join("data", file_name)

    # Save the file to the 'data' directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def validate_file_type(uploaded_file, allowed_types):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    return file_extension in allowed_types


def is_file_size_valid(uploaded_file, max_size):
    uploaded_file.seek(0, os.SEEK_END)
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)
    return file_size <= max_size

def extract_text_from_resume(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return ""

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)
