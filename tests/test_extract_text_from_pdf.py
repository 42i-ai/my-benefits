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
from my_benefits.extract_text_from_pdf import extract_bag_of_words
from my_benefits.extract_text_from_pdf import read_text_pages_extracted_from_pdf


@pytest.fixture
def prepare_document_extract_text():
    """Prepare test enviroment to extract text"""
    if os.path.isdir("tests/raw"):
        shutil.rmtree("tests/raw")
    os.mkdir("tests/raw")
    if os.path.isdir("tests/silver"):
        shutil.rmtree("tests/silver")
    os.mkdir("tests/silver")
    pytest.landing_directory =  "tests/landing"
    pytest.raw_directory = "tests/raw"
    pytest.silver_directory = "tests/silver"

class TestExtractTextFromPdf:
    """Class Test the extract_text_from_pdf module"""
    
    def test_read_files_from_directory(self, prepare_document_extract_text):
        """This method aims to test the read_files_from_directory method"""
        # Given pytest.directory
        # When
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        # Then
        assert files[0] == "pdf_test_no_ocr.pdf"
   
    def test_extract_text_from_pdf_with_pymupdf(self):
        """This method aims to text the pdf extraction"""
        # Given
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,files[0]))
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
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        text_file_name:str = "pdf_test_no_ocr.txt"
        # When
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,files[0]))
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        write_pdf_pages_to_file(pytest.raw_directory, text_file_name, list_of_pages)
        f = open(os.path.join( pytest.raw_directory, text_file_name), "r", encoding="utf-8")
        saved_text:str = f.read()
        f.close()
        list_of_lines_saved_text:List[str] = saved_text.splitlines()
        # Then
        assert list_of_pages[0] == list_of_lines_saved_text[0]

    def test_test_topic_modelig(self):
        # Given
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        text_file_name:str = files[0].replace(".pdf", ".txt")
        nlp = spacy.load("en_core_web_sm")
        #When
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,'pdf_test_no_ocr.pdf'))
        pages = extract_text_from_pdf_with_pymupdf(doc)
        preprocessed_pages = [preprocessing_text(page, nlp) for page in pages]
        corpus = extract_bag_of_words(preprocessed_pages)
        #Then
        assert len(corpus) > 0
    
    def test_read_text_pages_extracted_from_pdf(self):
        #Given
        files:List[str] = read_files_from_directory(pytest.landing_directory)
        nlp = spacy.load("en_core_web_sm")
        doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,'pdf_test_no_ocr.pdf'))
        list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
        #When
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory,'pdf_test_no_ocr.txt')
        #Then
        assert list_of_pages[0] == pages_read_from_file[0]
       
           

       