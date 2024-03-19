"""This module provides a function to extract text from a PDF file"""
import os
import fitz

def extract_text_from_pdf_with_pymupdf(pdf_path: str) -> str:
    """Extract text from a PDF file and retun it as a string"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def write_text_to_file(path: str,filename: str, text: str) -> str:
    """Write text to a file"""
    with open(os.path.join( path, filename), "w", encoding="utf-8") as file:
        file.write(text)
    return path + "/" + filename

def clean_pdf_data(path: str,filename: str) -> str:
    """Clean data"""
    with open(os.path.join( path, filename), "r", encoding="utf-8") as file:
        text = file.read()
        text = text.replace("\n", " ")
        text = text.replace("  ", " ")
    return text
