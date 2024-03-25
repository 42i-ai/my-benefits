"""Test the extract_text_from_pdf module"""
import os
import re
import shutil
import pytest
import polars as pl
import duckdb
from my_benefits.extract_text_from_pdf_controller import ExtractTextFromPDFController
from my_benefits.document_model import DocumentsModel
from my_benefits.topic_modeling import TopicModeling


@pytest.fixture
def prepare_document_extract_text():
    """Prepare test enviroment to extract text"""
    if not os.path.isdir("tests/landing"):
        os.mkdir("tests/landing")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/2014BenefitsGuide.pdf",
                        "tests/landing/pdf_test_no_ocr.pdf")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/Benefits Handbook.pdf",
                        "tests/landing/pdf_for_topic_modeling.pdf")
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
    pytest.landing_directory = "tests/landing"
    pytest.raw_directory = "tests/raw"
    pytest.silver_directory = "tests/silver"
    pytest.gold_directory = "tests/gold"
    pytest.models_directory = "tests/models"


@pytest.fixture
def prepare_topic_modeling():
    """Prepare test enviroment topic modeling"""
    my_document_model = DocumentsModel(
        pytest.raw_directory,
        pytest.silver_directory,
        pytest.gold_directory
    )
    extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
    df: pl.DataFrame = extract.process_pdf_files(pytest.landing_directory)
    connection = duckdb.connect(my_document_model.get_raw_database_dir())
    my_document_model.add_document_page_raw(df)
    pytest.documents = connection.execute("""
                                                  SELECT 
                                                  filename,
                                                  page_number,    
                                                  text
                                                  FROM 
                                                  document_pages
                                                  """
                                          ).pl()


class TestPDFExtraction:
    """Class Test the extract_text_from_pdf module"""

    def test_extract_text_from_pdf(self, prepare_document_extract_text):
        """This method aims to text the pdf extraction"""
        # Given
        extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
        # When
        df: pl.DataFrame = extract.process_pdf_files(pytest.landing_directory)
        # Then
        assert df.select(pl.col("text"))[
            0].item() == 'Employee Benefits  2014  '


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
        extracted_documents: pl.DataFrame = extract.process_pdf_files(
            pytest.landing_directory)
        connection = duckdb.connect(my_document_model.get_raw_database_dir())
        # When
        my_document_model.add_document_page_raw(extracted_documents)
        # Then
        result: pl.DataFrame = connection.execute("""
                                                  SELECT 
                                                  count(*) 
                                                  FROM 
                                                  document_pages
                                                  """
                                                  ).pl()
        assert result['count_star()'][0] == 66

    def test_persist_dataframe_on_document_pages_silver(self, prepare_document_extract_text):
        """This method aims to test the persist of a dataframe on document_pages table"""
        # Given
        topic_modeling: TopicModeling = TopicModeling()
        my_document_model: DocumentsModel = DocumentsModel(
            pytest.raw_directory,
            pytest.silver_directory,
            pytest.gold_directory
        )
        connection_raw = duckdb.connect(
            my_document_model.get_raw_database_dir())
        connection_silver = duckdb.connect(
            my_document_model.get_silver_database_dir())
        extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
        extract_documents: pl.DataFrame = extract.process_pdf_files(
            pytest.landing_directory)
        my_document_model.add_document_page_raw(extract_documents)
        documents_pages: pl.DataFrame = connection_raw.execute("""
                                                  SELECT 
                                                  filename,
                                                  page_number,    
                                                  text
                                                  FROM 
                                                  document_pages
                                                  """
                                                               ).pl()
        tokenized_documents = documents_pages.with_columns(
            pl.col("text").apply(lambda x: topic_modeling.preprocessing_text(x)).alias('tokenized_text'))
        # When
        my_document_model.add_document_page_silver(tokenized_documents)
        # Then
        result: pl.DataFrame = connection_silver.execute("""
                                                  SELECT 
                                                  tokenized_text 
                                                  FROM 
                                                  document_pages
                                                  """
                                                         ).pl()
        assert tokenized_documents.select(
            pl.col("tokenized_text").list.get(0))[0].item() == 'employee'


class TestTopicModeling:
    """Class Test the topic modeling  module"""

    def test_preprocess_step(self, prepare_document_extract_text, prepare_topic_modeling):
        # Given
        documents_to_process: pl.DataFrame = pytest.documents
        topic_modeling: TopicModeling = TopicModeling()
        # When
        tokenized_documents: pl.DataFrame = documents_to_process.with_columns(
            pl.col("text").apply(lambda x: topic_modeling.preprocessing_text(x)).alias('tokenized_text'))
        # Then
        assert tokenized_documents.select(
            pl.col("tokenized_text").list.get(0))[0].item() == 'employee'

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
