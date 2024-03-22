"""This module provides a function to extract text from a PDF file
First step extract text and tables from each PDF page
- Focus on extracting entities from the text using spacy
   https://medium.com/@mjghadge9007/building-your-own-custom-named-entity-recognition-ner-model-with-spacy-v3-a-step-by-step-guide-15c7dcb1c416
- To extract the text I will use pymupdf
- To extraxt the tables I will use tabula 

Save each table and text on separated files
Next step check how to use duckdb to facilitate this process
Add a button to my app page and run the process to extract the data
"""
import os, re
import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from typing import List, Tuple
from array import array
import fitz
import pandas as pd

#TODO: Change this method to use multithreading
def read_files_from_directory(directory: str) -> list:
    """Read files from a directory"""
    return os.listdir(directory)

#TODO: Create a function which read an directory and return a list of pdf files to be processed
def open_pdf_file(pdf_path: str) -> fitz.Document:
    """Open a PDF file and return a fitz.Document object"""
    return fitz.open(pdf_path)

def extract_tables_from_pdf_document(doc: fitz.Document) -> pd.DataFrame:
    """This can be used to extract tables https://www.youtube.com/watch?v=w2r2Bg42UPY"""
     
    df: pd.DataFrame = pd.DataFrame()
    return df

def extract_text_from_pdf_with_pymupdf(doc: fitz.Document) -> List[str]:
    """
    Extract text from each page from a PDF file and retun as a list of strings.
    
    Parameters:
        fitz.Documents: the result of the processing of the library pymupdf.
    Returns:
        list: a list of strings where each position is a page from the pdf.
    """
    documents: List[str] = []
    for page in doc:
        documents.append(clean_text(page.get_text()))
    return documents

def clean_text(text):
    """
    Clean text 
    
    Parameters:
       str: text extract from pdfs
    
    Returns:
       str: text without line breaks, hyphens, special characters, puctuations 
    """   
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def write_pdf_pages_to_file(path: str,filename: str, pages: List[str]) -> str:
    """
    Write pdf pages to a file.
    
    Parameters:
        path (str): path where the function will write the file
        filename (str): filename which the file will be write
        text pages (str): pages from the pdf to be write
    Returns:
        list: A list of preprocessed tokens.
    """
    filename_txt = filename.replace(".pdf",".txt")
    with open(os.path.join( path, filename_txt), "w", encoding="utf-8") as file:
        for page in pages:
            file.write(f"{page}\n")
    return path + "/" + filename

def read_text_pages_extracted_from_pdf(path: str, filename: str) -> List[str]:
    """
    Read pages from text file 

    Args:
        path (str): _description_
        filename (str): _description_

    Returns:
        List[str]: _description_
    """
    with open(os.path.join( path, filename), "r") as file:
         saved_pages:str = file.readlines()
    lines = [page.rstrip('\n') for page in saved_pages]
    return lines

def preprocessing_text(text:str, nlp: spacy.language)-> List[str]:
    """
    Tokenizes and preprocesses the input text, removing stopwords and short
    tokens.

    Parameters:
        text (str): The input text to preprocess.
        spacy language: .
    Returns:
        list: A list of preprocessed tokens.
    """
    # Tokenize and preprocess each document
    doc = re.sub(r'\W', ' ', text)
    # Convert text to lowercase
    doc = doc.lower()
    doc = nlp(doc)
    # Lemmatize and remove stop words
    tokens:List[str] = []
    for token in doc:
        if token.is_alpha and not token.is_stop: 
            tokens.append(token.text)
    return tokens

def extract_bag_of_words(preprocessed_docs : List[str], path_to_serialize : str) :
    """
    Create a bag of words (BoW) and serialize it representation for each document using Gensim.
    Args:
        preprocessed_docs (List[str]): pages extracted from pdfs clennead and tokenized
    """
    dictionary = corpora.Dictionary(preprocessed_docs)
    bow_corpus = [dictionary.doc2bow(doc) for doc in preprocessed_docs]
    corpora.MmCorpus.serialize(os.join(path_to_serialize,'bow_corpus.mm'), bow_corpus)

def build_lda_model(corpus : dict) -> dict:
    """
    Given the bag of words dictionary return the topic model
    Args:
        corpus (dict): dictionary of bag of words
    """
    #lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)
    my_dictionary = {}
    return my_dictionary
    