"""
This module is responsible for training the model of the topic modeling.
https://bpw1621.com/archive/streamlit-topic-modeling/
"""
import os
from datetime import datetime
import logging
import spacy
import fitz
from typing import List
from extract_text_from_pdf import extract_text_from_pdf_with_pymupdf
from extract_text_from_pdf import read_files_from_directory 
from extract_text_from_pdf import write_pdf_pages_to_file
from extract_text_from_pdf import preprocessing_text
from extract_text_from_pdf import open_pdf_file
from extract_text_from_pdf import read_text_pages_extracted_from_pdf
from extract_text_from_pdf import generate_pretrained_model
from extract_text_from_pdf import get_list_of_topics_from_document


PDF_NO_OCR_PATH = "./my_benefits/data/pdf-no-ocr-data"
RAW_DIRECTORY = "./my_benefits/raw"
SILVER_DIRECTORY = "./my_benefits/silver"
GOLD_DIRECTORY = "./my_benefits/gold"
MODELS_DIRECTORY = "./my_benefits/models"
LOGS_DIRECTORY = "./my_benefits/logs"

if not os.path.exists(PDF_NO_OCR_PATH):
    os.makedirs(PDF_NO_OCR_PATH)

if not os.path.exists(RAW_DIRECTORY):
    os.makedirs(RAW_DIRECTORY)

if not os.path.exists(SILVER_DIRECTORY):
    os.makedirs(SILVER_DIRECTORY)

if not os.path.exists(GOLD_DIRECTORY):
    os.makedirs(GOLD_DIRECTORY)

if not os.path.exists(MODELS_DIRECTORY):
    os.makedirs(MODELS_DIRECTORY)

if not os.path.exists(LOGS_DIRECTORY):
    os.makedirs(LOGS_DIRECTORY)

now = datetime.now()

# Format the date and time
formatted_date_time = now.strftime("%d-%m-%Y-%H-%M-%S")

logger = logging.getLogger('debug_logger')
logger.setLevel(logging.DEBUG)  
file_handler = logging.FileHandler(f'./my_benefits/logs/train_model-{formatted_date_time}.log')
file_handler.setLevel(logging.DEBUG)  
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

nlp = spacy.load("en_core_web_sm")

def extract_pdf_text():
    """
    Preprocess the files in the directory and save the content in a new file
    """
    for file in read_files_from_directory(PDF_NO_OCR_PATH):
        fitz.Document = open_pdf_file(os.path.join(PDF_NO_OCR_PATH,file))
        pages: List[str] = extract_text_from_pdf_with_pymupdf(fitz.Document)
        write_pdf_pages_to_file(RAW_DIRECTORY, file.replace(".pdf", ".txt"), pages)
        logger.debug(f'file processed {file}')




#TODO: Add an function to persist preprecessded text in a file
def train_model():
    """
    Train the model of the topic modeling
    """
    documents_to_train_model: List[str] = []
    for file in read_files_from_directory(RAW_DIRECTORY):
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(RAW_DIRECTORY,file)
        preprocessed_pages: List[str] = [preprocessing_text(page, nlp) for page in pages_read_from_file]
        logger.debug(f'load {len(preprocessed_pages)} pages from {file}')
        documents_to_train_model.extend(preprocessed_pages)
    write_pdf_pages_to_file(SILVER_DIRECTORY, "all_processed_documents.txt", documents_to_train_model)
    generate_pretrained_model(documents_to_train_model, MODELS_DIRECTORY, 20, 10)
    logger.debug(f'generated model from {len(preprocessed_pages)} pages')

def extract_topics_from_documents():
    """
    Extract text from pdf files
    """
    for file in read_files_from_directory(RAW_DIRECTORY):
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(RAW_DIRECTORY,file)
        preprocessed_pages: List[str] = [preprocessing_text(page, nlp) for page in pages_read_from_file]
        topics_words:List[str] = get_list_of_topics_from_document(preprocessed_pages,RAW_DIRECTORY)
        print(topics_words)

#extract_pdf_text()
#train_model()
#extract_topics_from_documents()