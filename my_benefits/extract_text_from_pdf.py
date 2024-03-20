"""This module provides a function to extract text from a PDF file
First step extract text and tables from each PDF page
- To extract the text I will use pymupdf
- To extraxt the tables I will use tabula 
Save each table and text on separated files
Next step check how to use duckdb to facilitate this process
Add a button to my app page and run the process to extract the data
"""
import os
from typing import List, Tuple
import fitz
import pandas as pd

#TODO: Change this method to use multithreading
def read_files_from_directory(directory: str) -> list:
    """Read files from a directory"""
    return os.listdir(directory)

#TODO: Create a function which read an directory and return a list of pdf files to be processed
def open_pdf_file(pdf_path: str) -> fitz.Document:
    """Open a PDF file and return a fitz.Document object"""
    return fitz.open(pdf_path)

def extract_tables_from_pdf_document(doc: fitz.Document) -> pd.DataFrame:
    """This can be used to extract tables https://www.youtube.com/watch?v=w2r2Bg42UPY"""
     
    df: pd.DataFrame = pd.DataFrame()
    return df

def extract_text_from_pdf_with_pymupdf(doc: fitz.Document) -> str:
    """Extract text from a PDF file and retun it as a string
       In the future we can create an abstract method to use distinct 
       libraries to extract text from PDFs
    """
    tables_list: List[pd.DataFrame] = []
    text = ""
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

def load_all_pdf_join_them(source_folder: str, destination_folder: str, destination_file: str) -> str:
    """Load all PDF files from a directory and join them in a single file"""
    all_pdf_text = []
    for filename in os.listdir(source_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(source_folder, filename)
        with open(pdf_path, 'rb') as pdf_file:
            text = extract_text_from_pdf_with_pymupdf(pdf_file)
            all_pdf_text.append(text)
    combined_text = '\n\n'.join(all_pdf_text)  
    with open(os.path.join( destination_folder, destination_file), 'w', encoding='utf-8') as combined_txt_file:
        combined_txt_file.write(combined_text)
    return destination_folder + "/" + destination_file