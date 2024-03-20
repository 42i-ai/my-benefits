"""This module provides a function to extract text from a PDF file
First step extract text and tables from each PDF page
Save each table and text on separated files
Next step check how to use duckdb to facilitate this process
Add a button to my app page and run the process to extract the data
"""
import os
import concurrent.futures
import fitz
import pandas as pd

#TODO: Change this method to use multithreading
def read_files_from_directory(directory: str) -> list:
    """Read files from a directory"""
    return os.listdir(directory)


def extract_tables_from_pdf_document(doc: fitz.Document) -> pd.DataFrame:
    """This can be used to extract tables https://www.youtube.com/watch?v=w2r2Bg42UPY"""
    df: pd.DataFrame = pd.DataFrame()
    return df

#TODO: Create a function which read an directory and return a list of pdf files to be processed
def open_pdf_file(pdf_path: str) -> fitz.Document:
    """Open a PDF file and return a fitz.Document object"""
    return fitz.open(pdf_path)

def extract_text_from_pdf_with_pymupdf(doc: fitz.Document) -> str:
    """Extract text from a PDF file and retun it as a string
       In the future we can create an abstract method to use distinct 
       libraries to extract text from PDFs
    """
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
