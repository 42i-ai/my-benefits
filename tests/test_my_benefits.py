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
from typing import List, Tuple


@pytest.fixture
def prepare_document_extract_text():
    """Prepare test enviroment to extract text"""
    if not os.path.isdir("tests/landing"):
        os.mkdir("tests/landing")
        os.mkdir("tests/landing/pdf-no-ocr-data")
        os.mkdir("tests/landing/image_conversion")
        os.mkdir("tests/landing/pdf-ocr-data")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/2014BenefitsGuide.pdf",
                        "tests/landing/pdf-no-ocr-data/pdf_test_no_ocr.pdf")
        shutil.copyfile("./my_benefits/data/pdf-no-ocr-data/Benefits Handbook.pdf",
                        "tests/landing/pdf-no-ocr-data/pdf_for_topic_modeling.pdf")
        shutil.copyfile("./my_benefits/data/pdf-ocr-data/employee_benefits_3.pdf",
                        "tests/landing/pdf-ocr-data/employee_benefits_3.pdf")

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
    pytest.landing_directory_no_ocr_data = "tests/landing/pdf-no-ocr-data"
    pytest.landing_directory_ocr_data = "tests/landing/pdf-ocr-data"
    pytest.raw_directory = "tests/raw"
    pytest.silver_directory = "tests/silver"
    pytest.gold_directory = "tests/gold"
    pytest.models_directory = "tests/models"
    pytest.image_conversion = "tests/landing/image_conversion"


@pytest.fixture
def prepare_topic_modeling():
    """Prepare test enviroment topic modeling"""
    my_document_model = DocumentsModel(
        pytest.raw_directory,
        pytest.silver_directory,
        pytest.gold_directory
    )
    extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
    df: pl.DataFrame = extract.process_pdf_files(
        pytest.landing_directory_no_ocr_data)
    connection_raw = duckdb.connect(my_document_model.get_raw_database_dir())
    connection_silver = duckdb.connect(
        my_document_model.get_silver_database_dir())
    my_document_model.add_document_page_raw(df)
    pytest.document_extracted_from_pdf = connection_raw.execute("""
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
        df: pl.DataFrame = extract.process_pdf_files(
            pytest.landing_directory_no_ocr_data)
        # Then
        assert df.select(pl.col("text"))[
            0].item() == 'Employee Benefits  2014  '

    def test_extract_text_from_pdf_ocr(self, prepare_document_extract_text):
        """This method aims to text the pdf extraction"""
        # Given
        extract: ExtractTextFromPDFController = ExtractTextFromPDFController()
        # When
        df: pl.DataFrame = extract.process_pdf_files_ocr(
            pytest.landing_directory_ocr_data, pytest.image_conversion)
        # Then
        assert len(df) == 2


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
            pytest.landing_directory_no_ocr_data)
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
            pytest.landing_directory_no_ocr_data)
        my_document_model.add_document_page_raw(extract_documents)
        documents_pages: pl.DataFrame = connection_raw.execute("""
                                                  SELECT 
                                                  filename,
                                                  page_number,    
                                                  text,
                                                  is_ocr
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
        documents_to_process: pl.DataFrame = pytest.document_extracted_from_pdf
        topic_modeling: TopicModeling = TopicModeling(
            path_to_serialize=pytest.models_directory)
        # When
        tokenized_documents: pl.DataFrame = documents_to_process.with_columns(
            pl.col("text").apply(lambda x: topic_modeling.preprocessing_text(x)).alias('tokenized_text'))
        # Then
        assert tokenized_documents.select(
            pl.col("tokenized_text").list.get(0))[0].item() == 'employee'

    def test_train_model(self, prepare_document_extract_text, prepare_topic_modeling):
        # Given
        documents_to_process: pl.DataFrame = pytest.document_extracted_from_pdf
        topic_modeling: TopicModeling = TopicModeling(
            path_to_serialize=pytest.models_directory)
        tokenized_documents: pl.DataFrame = documents_to_process.with_columns(
            pl.col("text").apply(lambda x: topic_modeling.preprocessing_text(x)).alias('tokenized_text'))
        # When
        topic_modeling.train_model(tokenized_documents)
        # Then
        assert os.path.isfile(os.path.join(
            pytest.models_directory, topic_modeling.get_lda_model_filename())) is True

    def test_get_list_of_topics(self, prepare_document_extract_text, prepare_topic_modeling):
        # Given
        documents_to_process: pl.DataFrame = pytest.document_extracted_from_pdf
        topic_modeling: TopicModeling = TopicModeling(
            path_to_serialize=pytest.models_directory)
        tokenized_documents: pl.DataFrame = documents_to_process.with_columns(
            pl.col("text").apply(lambda x: topic_modeling.preprocessing_text(x)).alias('tokenized_text'))
        topic_modeling.train_model(tokenized_documents)
        document: str = duckdb.execute(
            """
                                Select listagg(element) 
                                from (
                                    Select unnest(tokenized_text) AS element 
                                    from tokenized_documents 
                                    where filename = 'pdf_test_no_ocr.pdf') 
                                    subquery
            """).fetchall()[0][0].split(',')
        # when
        topics_words = topic_modeling.get_list_of_topics_from_document(
            document, pytest.models_directory)
        # Then
        assert len(topics_words) > 0
