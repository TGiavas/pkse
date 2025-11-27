import os
from pypdf import PdfReader

def extract_text_from_file(file_path):
    """
    Extract text from a file based on its extension.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.pdf':
        return _extract_from_pdf(file_path)
    elif ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']:
        return _extract_from_text(file_path)
    else:
        return ""

def _extract_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def _extract_from_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading text file {file_path}: {e}")
        return ""

