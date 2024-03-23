"""
This module is responsible for training the model of the topic modeling.
https://bpw1621.com/archive/streamlit-topic-modeling/
"""
import os
import logging
import fitz
from extract_text_from_pdf import extract_text_from_pdf_with_pymupdf, read_files_from_directory, write_pdf_pages_to_file
from extract_text_from_pdf import open_pdf_file
from typing import List

PDF_NO_OCR_PATH = "./my_benefits/data/pdf-no-ocr-data"
RAW_DIRECTORY = "./my_benefits/raw"

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
                  )


logger = logging.getLogger('./my_benefits/example_logger')

for file in read_files_from_directory(PDF_NO_OCR_PATH):
    fitz.Document = open_pdf_file(os.path.join(PDF_NO_OCR_PATH,file))
    pages: List[str] = extract_text_from_pdf_with_pymupdf(fitz.Document)
    write_pdf_pages_to_file(RAW_DIRECTORY, file.replace(".pdf", ".txt"), pages)


