import PyPDF2
import fitz
import os



def extract_text_from_pdf_with_pymupdf(pdf_path: str) -> str:
    """Extract text from a PDF file and retun it as a string"""
    text = ""
    document = fitz.open(pdf_path)
    for page_number in range(len(document)):
        page = document[page_number]
        text += page.get_text()
    return text


def write_text_to_file(path: str,filename: str, text: str) -> str:
    """Write text to a file"""
    with open(os.path.join( path, filename), "w") as file:
        file.write(text)
    return path + "/" + filename

def clean_pdf_data(path: str,filename: str) -> str:
    """Clean data"""
    with open(os.path.join( path, filename), "r") as file:
        text = file.read()
        text = text.replace("\n", " ")
        text = text.replace("  ", " ")
    return text

