import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu



st.set_page_config(
    page_title="My Benefits", 
    page_icon=":moneybag:", 
    layout="centered", 
    initial_sidebar_state="auto", 
    menu_items=None)

with st.sidebar:
    selected = option_menu("Main Menu", ["Dashboard","Data Visualization"], 
        icons=['house','pie-chart'], menu_icon="cast", default_index=0)
    selected

if selected == 'Dashboard':
    st.markdown("---")
    st.title('Welcome To Streamlit Learn Dashboard')

    st.write(" Streamlit Learn Dashboard merupakan tampilan visual yang dapat digunakan untuk mempresentasikan informasi mengenai produk secara ringkas dan terstruktur. Dashboard ini dapat digunakan untuk memantau produk, menganalisis tren penjualan produk, dan dapat digunakan sebagai bahan untuk pengambilan keputusan .")
    
    st.write('Silahkan Upload File dan Pilih Menu Sidebar untuk mulai melakukan analisa')
    # st.write('')
    st.markdown("---")

