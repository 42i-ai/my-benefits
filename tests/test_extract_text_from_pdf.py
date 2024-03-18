from my_benefits.extract_text_from_pdf import extract_text_from_pdf
from my_benefits.extract_text_from_pdf import write_text_to_file
import os
class TestExtractTextFromPdf:
    def test_extract_text_from_pdf(self):
        # Given
        pdf_path = "tests/data/pdf_test_no_ocr.pdf"
        # When
        text = extract_text_from_pdf(pdf_path)
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