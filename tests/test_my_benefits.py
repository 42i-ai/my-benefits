"""Test the extract_text_from_pdf module"""
import os
import re
import shutil
import pytest
import polars as pl
import duckdb
from my_benefits.extract_text_from_pdf_controller import ExtractTextFromPDFController
from my_benefits.document_model import DocumentsModel

@pytest.fixture
def prepare_document_extract_text():
    """Prepare test enviroment to extract text"""
    if not os.path.isdir("tests/landing"):
        os.mkdir("tests/landing")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/2014BenefitsGuide.pdf", "tests/landing/pdf_test_no_ocr.pdf")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/Benefits Handbook.pdf", "tests/landing/pdf_for_topic_modeling.pdf")
    if os.path.isdir("tests/raw"):
        shutil.rmtree("tests/raw")
    os.mkdir("tests/raw")
    if os.path.isdir("tests/silver"):
        shutil.rmtree("tests/silver")
    os.mkdir("tests/silver")
    if os.path.isdir("tests/gold"):
        shutil.rmtree("tests/gold")
    os.mkdir("tests/gold")
    if os.path.isdir("tests/models"):
        shutil.rmtree("tests/models")
    os.mkdir("tests/models")
    pytest.landing_directory =  "tests/landing"
    pytest.raw_directory = "tests/raw"
    pytest.silver_directory = "tests/silver"
    pytest.gold_directory = "tests/gold"
    pytest.models_directory = "tests/models"


class TestPDFExtraction:
    """Class Test the extract_text_from_pdf module"""
    
    def test_extract_text_from_pdf(self, prepare_document_extract_text):
        """This method aims to text the pdf extraction"""
        # Given
        extract: ExtractTextFromPDFController = ExtractTextFromPDFController()   
        # When
        df: pl.DataFrame  = extract.process_pdf_files(pytest.landing_directory)
        # Then
        assert df.select(pl.col("text"))[0].item() == 'Employee Benefits  2014  '



class TestDocumentModel:
    """Class Test the my_benefits_model module"""
    def test_persist_dataframe_on_document_pages(self, prepare_document_extract_text):
        """This method aims to test the persist of a dataframe on document_pages table"""
        # Given
        my_document_model = DocumentsModel(
                                            pytest.raw_directory,
                                            pytest.silver_directory,
                                            pytest.gold_directory
                                          )
        extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
        df: pl.DataFrame  = extract.process_pdf_files(pytest.landing_directory)
        connection = duckdb.connect(my_document_model.get_raw_database_dir())
        # When
        my_document_model.add_document_page_raw(df)
        # Then
        result: pl.DataFrame = connection.execute("""
                                                  SELECT 
                                                  count(*) 
                                                  FROM 
                                                  document_pages
                                                  """
                                                 ).pl()
        assert result['count_star()'][0] == 66
        
    # def test_extract_text_from_pdf_with_pymupdf(self):
    #     """This method aims to text the pdf extraction"""
    #     # Given
    #     doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,pytest.file_for_test))
    #     # When
    #     list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
    #     # Then
    #     assert list_of_pages[0] == "Employee Benefits"
    
    # def test_write_text_to_file(self):
    #     """This method aims to test the write function to a text file"""
    #     # Given
    #     filename:str = "test.txt"
    #     text:str = "This is a test"
    #     # When
    #     result:str = write_pdf_pages_to_file(pytest.raw_directory, filename, text)
    #     exist:bool = os.path.isfile(result)
    #     # Then
    #     os.remove(result)
    #     assert exist is True

    # def test_extract_text_from_pdf_write_to_file(self):
    #     """This method aims to test the extraction of text from a pdf and write it to a file"""
    #     # Given
    #     doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory,pytest.file_for_test))
    #     list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
    #     # When
    #     write_pdf_pages_to_file(pytest.raw_directory, pytest.file_for_test, list_of_pages)
    #     f = open(os.path.join( pytest.raw_directory, pytest.file_for_test.replace(".pdf",".txt")), "r", encoding="utf-8")
    #     saved_text:str = f.read()
    #     f.close()
    #     list_of_lines_saved_text:List[str] = saved_text.splitlines()
    #     # Then
    #     assert list_of_pages[0] == list_of_lines_saved_text[0]
        
    # def test_read_text_pages_extracted_from_pdf(self):
    #     #Given
    #     doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory, pytest.file_for_test))
    #     list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
    #     #When
    #     pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory,pytest.file_for_test.replace(".pdf",".txt"))
    #     #Then
    #     assert list_of_pages[0] == pages_read_from_file[0]

    # def test_build_pretrained_model(self):
    #     # Given
    #     doc: fitz.Document = open_pdf_file(os.path.join(pytest.landing_directory, pytest.file_topic_model))
    #     list_of_pages: List[str] = extract_text_from_pdf_with_pymupdf(doc)
    #     write_pdf_pages_to_file(pytest.raw_directory, pytest.file_topic_model, list_of_pages)
    #     pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory,pytest.file_topic_model.replace(".pdf",".txt"))
    #     preprocessed_pages = [preprocessing_text(page, pytest.nlp) for page in pages_read_from_file]
    #     #When
    #     generate_pretrained_model(preprocessed_pages, pytest.models_directory)
    #     #Then
    #     pretrained_lda_model, pretrained_dictionary = load_pretrained_model(pytest.models_directory)
    #     assert len(pretrained_dictionary) > 0 
        
    # def test_get_list_of_topics_from_document(self):
    #     #Given
    #     pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory, pytest.file_topic_model.replace(".pdf",".txt"))
    #     preprocessed_pages = [preprocessing_text(page, pytest.nlp) for page in pages_read_from_file]
    #     #when
    #     topics_words:List[str] = get_list_of_topics_from_document(preprocessed_pages,pytest.models_directory)
    #     #Then
    #     assert len(topics_words) > 0

    # def test_write_preprocessed_corpus_to_file(self):
    #     #Given
    #     file_name:str = "all_preprocessed_documents.txt"
    #     documents : List[str]= [] 
    #     for file in read_files_from_directory(pytest.raw_directory):
    #         pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(pytest.raw_directory, file)
    #         preprocessed_pages = [preprocessing_text(page, pytest.nlp) for page in pages_read_from_file]
    #         documents.extend(preprocessed_pages)
    #     #When
    #     result:str = write_preprocessed_corpus_to_file(pytest.raw_directory,pytest.silver_directory, file_name,  pytest.nlp)
    #     f = open(os.path.join( pytest.silver_directory, file_name), "r", encoding="utf-8")
    #     saved_documents:str = f.read()
    #     f.close()
    #     list_of_lines_saved_documents:List[str] = saved_documents.splitlines()
    #     #Then
    #     assert len(documents) == len(list_of_lines_saved_documents)

    
        
    
    
        
        
       
           

       