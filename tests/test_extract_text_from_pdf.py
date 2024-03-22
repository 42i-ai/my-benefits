"""Test the extract_text_from_pdf module"""
import os
import re
import shutil
from pypdf import PdfReader
from pprint import pprint
from typing import List
import pandas as pd
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pytest
import fitz
import spacy
import nltk
from nltk.corpus import stopwords
from array import array
from my_benefits.extract_text_from_pdf import open_pdf_file, read_files_from_directory
from my_benefits.extract_text_from_pdf import write_pdf_pages_to_file
from my_benefits.extract_text_from_pdf import extract_text_from_pdf_with_pymupdf
from my_benefits.extract_text_from_pdf import preprocessing_text
from my_benefits.extract_text_from_pdf import generate_pretrained_model
from my_benefits.extract_text_from_pdf import read_text_pages_extracted_from_pdf
from my_benefits.extract_text_from_pdf import get_list_of_topics_from_document
from my_benefits.extract_text_from_pdf import load_pretrained_model


@pytest.fixture
def prepare_document_extract_text():
    """Prepare test enviroment to extract text"""
    if os.path.isdir("tests/raw"):
        shutil.rmtree("tests/raw")
    os.mkdir("tests/raw")
    if os.path.isdir("tests/silver"):
        shutil.rmtree("tests/silver")
    os.mkdir("tests/silver")
    if os.path.isdir("tests/models"):
        shutil.rmtree("tests/models")
    os.mkdir("tests/models")
    pytest.landing_directory =  "tests/landing"
    pytest.raw_directory = "tests/raw"
    pytest.silver_directory = "tests/silver"
    pytest.models_directory = "tests/models"
    pytest.file_for_test = "pdf_test_no_ocr.pdf"
    pytest.file_topic_model = "pdf_for_topic_modeling.pdf"
    pytest.nlp = spacy.load("en_core_web_sm")

class TestExtractTextFromPdf:
    """Class Test the extract_text_from_pdf module"""
    
    def test_read_files_from_directory(self, prepare_document_extract_text):
        """This method aims to test the read_files_from_directory method"""
        # Given pytest.directory
        # When
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        filename = ""
        for f in files:
            if f == pytest.file_for_test:
                filename = f
        # Then
        assert filename ==  pytest.file_for_test
   
    def test_extract_text_from_pdf_with_pymupdf(self):
        """This method aims to text the pdf extraction"""
        # Given
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,pytest.file_for_test))
        # When
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        # Then
        assert list_of_pages[0] == "Employee Benefits"
    
    def test_write_text_to_file(self):
        """This method aims to test the write function to a text file"""
        # Given
        filename:str = "test.txt"
        text:str = "This is a test"
        # When
        result:str = write_pdf_pages_to_file(pytest.raw_directory, filename, text)
        exist:bool = os.path.isfile(result)
        # Then
        assert exist is True

    def test_extract_text_from_pdf_write_to_file(self):
        """This method aims to test the extraction of text from a pdf and write it to a file"""
        # Given
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,pytest.file_for_test))
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        # When
        write_pdf_pages_to_file(pytest.raw_directory, pytest.file_for_test, list_of_pages)
        f = open(os.path.join( pytest.raw_directory, pytest.file_for_test.replace(".pdf",".txt")), "r", encoding="utf-8")
        saved_text:str = f.read()
        f.close()
        list_of_lines_saved_text:List[str] = saved_text.splitlines()
        # Then
        assert list_of_pages[0] == list_of_lines_saved_text[0]
        
    def test_read_text_pages_extracted_from_pdf(self):
        #Given
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory, pytest.file_for_test))
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        #When
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory,pytest.file_for_test.replace(".pdf",".txt"))
        #Then
        assert list_of_pages[0] == pages_read_from_file[0]

    def test_build_pretrained_model(self):
        # Given
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory, pytest.file_topic_model))
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        write_pdf_pages_to_file(pytest.raw_directory, pytest.file_topic_model, list_of_pages)
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory,pytest.file_topic_model.replace(".pdf",".txt"))
        preprocessed_pages = [preprocessing_text(page, pytest.nlp) for page in pages_read_from_file]
        #When
        generate_pretrained_model(preprocessed_pages, pytest.models_directory)
        #Then
        pretrained_lda_model, pretrained_dictionary = load_pretrained_model(pytest.models_directory)
        assert len(pretrained_dictionary) > 0 
        
    def test_get_list_of_topics_from_document(self):
        #Given
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory, pytest.file_topic_model.replace(".pdf",".txt"))
        preprocessed_pages = [preprocessing_text(page, pytest.nlp) for page in pages_read_from_file]
        #when
        sorted_topics:List[str] = get_list_of_topics_from_document(preprocessed_pages,pytest.models_directory)
        #Then
        assert len(sorted_topics) > 0
        
    
    
        
        
       
           

       