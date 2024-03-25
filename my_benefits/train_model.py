"""
This module is responsible for training the model of the topic modeling.
https://bpw1621.com/archive/streamlit-topic-modeling/
"""
import os
from datetime import datetime
import logging
import spacy
import fitz
import pandas as pd
from typing import List
from my_benefits.extract_text_from_pdf_controller import extract_text_from_pdf_with_pymupdf
from my_benefits.extract_text_from_pdf_controller import read_files_from_directory 
from my_benefits.extract_text_from_pdf_controller import write_pdf_pages_to_file
from my_benefits.extract_text_from_pdf_controller import preprocessing_text
from my_benefits.extract_text_from_pdf_controller import open_pdf_file
from my_benefits.extract_text_from_pdf_controller import read_text_pages_extracted_from_pdf
from my_benefits.extract_text_from_pdf_controller import generate_pretrained_model
from my_benefits.extract_text_from_pdf_controller import get_list_of_topics_from_document
from my_benefits.extract_text_from_pdf_controller import write_preprocessed_corpus_to_file

#TODO: Probabily this all file will become a kind of storage class to persist the data
PDF_NO_OCR_PATH = "./my_benefits/data/pdf-no-ocr-data"
RAW_DIRECTORY = "./my_benefits/raw"
SILVER_DIRECTORY = "./my_benefits/silver"
GOLD_DIRECTORY = "./my_benefits/gold"
MODELS_DIRECTORY = "./my_benefits/models"
LOGS_DIRECTORY = "./my_benefits/logs"
DOCUMENT_CORPUS = "all_preprocessed_documents.txt" 

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

def write_corpus_to_file():
    """
    Write the preprocessed corpus to a file
    """
    write_preprocessed_corpus_to_file(RAW_DIRECTORY,SILVER_DIRECTORY, DOCUMENT_CORPUS, nlp)

def get_list_of_words_from_document()-> pd.DataFrame:
    """
    Get the list of words from the document corpus
    """
    f = open(os.path.join( SILVER_DIRECTORY,DOCUMENT_CORPUS), "r", encoding="utf-8")
    saved_documents:str = f.read()
    list_of_lines_saved_documents:List[str] = saved_documents.splitlines()
    for pages in list_of_lines_saved_documents:  
        for word in pages:
            print(word) 
    df : pd.DataFrame = pd.DataFrame(list_of_lines_saved_documents, columns=['Number', 'Letter'])
    return df



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
get_list_of_words_from_document()