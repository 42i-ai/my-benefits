"""Test the extract_text_from_pdf module"""
import os
import shutil
from typing import List
import pandas as pd
import pytest
import fitz
from my_benefits.extract_text_from_pdf import open_pdf_file, read_files_from_directory
from my_benefits.extract_text_from_pdf import write_text_to_file
from my_benefits.extract_text_from_pdf import extract_text_from_pdf_with_pymupdf
from my_benefits.extract_text_from_pdf import extract_tables_from_pdf_document

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
        text = extract_text_from_pdf_with_pymupdf(doc)
        list_of_lines = text.splitlines()
        # Then
        assert list_of_lines[0] == "Employee Benefits"

    def test_write_text_to_file(self):
        """This method aims to test the write function to a text file"""
        # Given
        filename:str = "test.txt"
        text:str = "This is a test"
        # When
        result:str = write_text_to_file(pytest.raw_directory, filename, text)
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
        text_extracted:str = extract_text_from_pdf_with_pymupdf(doc)
        list_of_lines_pdf = text_extracted.splitlines()
        write_text_to_file(pytest.raw_directory, text_file_name, text_extracted)
        f = open(os.path.join( pytest.raw_directory, text_file_name), "r", encoding="utf-8")
        saved_text:str = f.read()
        f.close()
        list_of_lines_saved_text = saved_text.splitlines()
        # Then
        assert list_of_lines_pdf[0] == list_of_lines_saved_text[0]