import PyPDF2
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file and retun it as a string"""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text()
    return text

def write_text_to_file(path: str,filename: str, text: str) -> str:
    """Write text to a file"""
    with open(os.path.join( path, filename), "w") as file:
        file.write(text)
    return path + "/" + filename

