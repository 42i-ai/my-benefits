import os
import duckdb
import streamlit as st
import polars as pl
import seaborn as sns
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
from document_model import DocumentsModel
from topic_modeling import TopicModeling
from extract_text_from_pdf_controller import ExtractTextFromPDFController
from wordcloud import WordCloud


WORDCLOUD_FONT_PATH = r'./assets/Inkfree.ttf'
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

document_model = DocumentsModel()
extract_data_from_documents = ExtractTextFromPDFController()
topic_modeling = TopicModeling()


def preprocessing_text() -> pl.DataFrame:
    """
    Tokenizes and preprocesses the input text, removing stopwords and short tokens.

    Returns:
    list: A list of lemmatized preprocessed tokens.
    """
    connection_raw = duckdb.connect(document_model.get_raw_database_dir())
    connection_silver = duckdb.connect(
        document_model.get_silver_database_dir())
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
    document_model.add_document_page_silver(tokenized_documents)
    result: pl.DataFrame = connection_silver.execute("""
                                                  SELECT 
                                                  tokenized_text 
                                                  FROM 
                                                  document_pages
                                                  """
                                                     ).pl()
    return result


def extract_information_from_the_pdf_files():
    # Code that gets executed when the button is clicked
    with st.spinner('Extracting text from documents ...'):
        documents: pl.DataFrame = extract_data_from_documents.process_pdf_files(
            PDF_NO_OCR_PATH)
        document_model.add_document_page_raw(documents)
    with st.spinner('Preprocessing document ...'):
        preprocessed_documents: pl.DataFrame = preprocessing_text()
    with st.spinner('Training model  ...'):
        topic_modeling.train_model(preprocessed_documents)


@st.cache_data()
def generate_wordcloud():

    # df = get_list_of_words_from_document()
    # wordcloud_text = ' '.join(df['Letter'].tolist())
    # wordcloud = WordCloud(font_path=WORDCLOUD_FONT_PATH, width=700, height=600,
    # background_color='white', collocations=True).generate(wordcloud_text)
    return None  # wordcloud


st.set_page_config(
    page_title="My Benefits",
    page_icon=":moneybag:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)


preprocessing_options = st.sidebar.form('preprocessing-options')

with preprocessing_options:
    st.header('Extract data from PDF files')
    submitted_extract_data = st.form_submit_button("Extract Data")

visualization_options = st.sidebar.form('visualization-options')

with visualization_options:
    st.header('Visualize data')
    submitted_visualize_data = st.form_submit_button("Visualize Data")


if submitted_extract_data:
    extract_information_from_the_pdf_files()
    st.write('Data has been extracted from the PDF files')

if submitted_visualize_data:
    generate_wordcloud()
