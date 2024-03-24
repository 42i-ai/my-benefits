import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
from train_model import extract_pdf_text
from train_model import write_corpus_to_file
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

@st.experimental_memo()
def generate_wordcloud():

    wordcloud_text = (' '.join(' '.join(doc) for doc in docs))
    wordcloud = WordCloud(font_path=WORDCLOUD_FONT_PATH, width=700, height=600,
                          background_color='white', collocations=collocations).generate(wordcloud_text)
    return wordcloud

st.set_page_config(
    page_title="My Benefits", 
    page_icon=":moneybag:", 
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items=None)

""" with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard","Data Visualization"], 
        icons=['house','pie-chart'], menu_icon="cast", default_index=0)
    selected

if selected == 'Dashboard':
    st.markdown("---")
    st.title('Welcome To Streamlit Learn Dashboard')

    st.write(" Streamlit Learn Dashboard merupakan tampilan visual yang dapat digunakan untuk mempresentasikan informasi mengenai produk secara ringkas dan terstruktur. Dashboard ini dapat digunakan untuk memantau produk, menganalisis tren penjualan produk, dan dapat digunakan sebagai bahan untuk pengambilan keputusan .")
    
    st.write('Silahkan Upload File dan Pilih Menu Sidebar untuk mulai melakukan analisa')
    # st.write('')
    st.markdown("---") """

preprocessing_options = st.sidebar.form('preprocessing-options')

with preprocessing_options:
        st.header('Extract data from PDF files')
        submitted = st.form_submit_button("Extract Data")


if submitted:
    extract_information_from_the_pdf_files()
    st.write('Data has been extracted from the PDF files')