import os
from pathlib import Path

def ensure_temp_directory():
    """Ensure temp directory exists"""
    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)
    return temp_dir

def clean_filename(filename):
    """Clean filename for safe file operations"""
    import re
    # Remove or replace unsafe characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe_filename[:100]  # Limit length

def get_file_extension(doc_type):
    """Get appropriate file extension for document type"""
    extensions = {
        "Exercise List": "docx",
        "PowerPoint Presentation": "pptx", 
        "Summary": "docx"
    }
    return extensions.get(doc_type, "docx")

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def load_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        return file.read()

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

def file_exists(file_path):
    return os.path.exists(file_path)