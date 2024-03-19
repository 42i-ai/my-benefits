from my_benefits.extract_text_from_pdf import write_text_to_file
from my_benefits.extract_text_from_pdf import extract_text_from_pdf_with_pymupdf
import os
class TestExtractTextFromPdf:
    def test_extract_text_from_pdf_with_pymupdf(self):
        # Given
        pdf_path = "tests/data/pdf_test_no_ocr.pdf"
        # When
        text = extract_text_from_pdf_with_pymupdf(pdf_path)
        list_of_lines = text.splitlines()
        # Then
        assert list_of_lines[0] == "Employee Benefits"
    
    def test_write_text_to_file(self):
        # Given
        path:str = "tests/raw"
        filename:str = "test.txt"
        text:str = "This is a test"
        # When
        result:str = write_text_to_file(path, filename, text)
        exist:bool = os.path.isfile(result)
        # Then
        assert exist == True

    def test_extract_text_from_pdf_write_to_tile(self):
        # Given
        pdf_path = "tests/data/pdf_test_no_ocr.pdf"
        text_path:str = "tests/raw"
        text_file_name:str = "pdf_test_no_ocr.txt"
        # When
        text_extracted:str = extract_text_from_pdf_with_pymupdf(pdf_path)
        list_of_lines_pdf = text_extracted.splitlines()
        result:str = write_text_to_file(text_path, text_file_name, text_extracted)
        f = open(os.path.join( text_path, text_file_name), "r")
        saved_text:str = f.read()
        list_of_lines_saved_text = saved_text.splitlines()
        # Then
        assert list_of_lines_pdf[0] == list_of_lines_saved_text[0]
    
    