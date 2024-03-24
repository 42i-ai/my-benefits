import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
from train_model import extract_pdf_text
from train_model import write_corpus_to_file
from train_model import get_list_of_words_from_document
from wordcloud import WordCloud
DEFAULT_HIGHLIGHT_PROBABILITY_MINIMUM = 0.001
DEFAULT_NUM_TOPICS = 6
WORDCLOUD_FONT_PATH = r'./assets/Inkfree.ttf'

def extract_information_from_the_pdf_files():
    # Code that gets executed when the button is clicked
    with st.spinner('Extracting text from documents ...'):
         extract_pdf_text()
    with st.spinner('Writting preprocessed document to file ...'):
         write_corpus_to_file()

@st.cache_data()
def generate_wordcloud():
    
    df = get_list_of_words_from_document()
    wordcloud_text = ' '.join(df['Letter'].tolist())
    wordcloud = WordCloud(font_path=WORDCLOUD_FONT_PATH, width=700, height=600,
                          background_color='white', collocations=True).generate(wordcloud_text)
    return wordcloud

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