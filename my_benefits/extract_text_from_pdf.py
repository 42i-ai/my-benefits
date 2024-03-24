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
from gensim.corpora.dictionary import Dictionary
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
    # Patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})'
    url_pattern = r'\b(?:http[s]?://|www\.)[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/))'

    # Removing entities
    text = re.sub(email_pattern, '', text)
    text = re.sub(phone_pattern, '', text)
    text = re.sub(url_pattern, '', text)   
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
    return path + "/" + filename_txt

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
        nlp (spacy.language): spacy language model
    Returns:
        list: A list of lemmatized preprocessed tokens.
    """
    # Tokenize and preprocess each document
    doc = re.sub(r'\W', ' ', text)
    # Convert text to lowercase
    doc = doc.lower()
    doc = nlp(doc)
    # Lemmatize and remove stop words
    tokens:List[str] = []
    for token in doc:
        if token.is_alpha and not token.is_stop and len(token) > 3: 
            tokens.append(token.lemma_)
    return tokens

def write_preprocessed_corpus_to_file( 
                                    path_all_documents: str,  
                                    path_corpus: str, 
                                    filename: str,
                                    nlp: spacy.language
                                    ):
    """
    Write preprocessed corpus to a file.
    
    Parameters:
        path_all_documents (str): path where we will write the all documents file
        path_corpus (str): path where we will write the corpus file
        filename (str): filename which the file will be write
        nlp (spacy.language): spacy language model
    """
    documents : List[str]= [] 
    for file in read_files_from_directory(path_all_documents):
        pages_read_from_file: List[str] = read_text_pages_extracted_from_pdf(
                                                                    path_all_documents, 
                                                                    file
                                                                           )
        preprocessed_pages = [preprocessing_text(page, nlp) for page in pages_read_from_file]
        documents.extend(preprocessed_pages)
    with open(os.path.join( path_corpus, filename), "w", encoding="utf-8") as file:
        for doc in documents:
            file.write(f"{doc}\n")
    

def generate_pretrained_model(preprocessed_docs : List[str], path_to_serialize : str, num_topics : int = 20, passes : int = 10):
    """
    Create a bag of words (BoW) and serialize it representation for each document using Gensim.
    Args:
        preprocessed_docs (List[str]): pages extracted from pdfs clennead and tokenized
        path_to_serialize (str): path for bag_of_words file
        num_topics (int): number of topics
        passes (int): lda algorithm 
    """
    dictionary = corpora.Dictionary(preprocessed_docs)
    dictionary.filter_extremes(no_below=2, no_above=0.5)
    bow_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in preprocessed_docs]
    lda_model = LdaModel(corpus=bow_corpus, id2word=dictionary, num_topics=num_topics, passes=10)
    lda_model.save(os.path.join(path_to_serialize,'pretrained_lda_model.model'))
    dictionary.save(os.path.join(path_to_serialize,'pretrained_dictionary.dict'))
    
def load_pretrained_model(path_to_serialize : str) -> Tuple[LdaModel, Dictionary] :
    """_summary_

    Args:
        path_to_serialize (str): _description_

    Returns:
        Tuple[LdaModel, Dictionary]: _description_
    """
    pretrained_lda_model = LdaModel.load(os.path.join(path_to_serialize,'pretrained_lda_model.model'))
    pretrained_dictionary = corpora.Dictionary.load(os.path.join(path_to_serialize,'pretrained_dictionary.dict'))
    return pretrained_lda_model, pretrained_dictionary

def get_list_of_topics_from_document(preprocessed_docs : List[str], path_pretrained_model : str)-> List[str]:
    """_summary_
    """
    pretrained_lda_model, pretrained_dictionary  = load_pretrained_model(path_pretrained_model)
    new_corpus = [pretrained_dictionary.doc2bow(doc) for doc in preprocessed_docs]
    # Classify the new documents using the pre-trained LDA model
    for i, doc_bow in enumerate(new_corpus):
        print(f"Document {i+1}:")
        topic_distribution = pretrained_lda_model[doc_bow]
        sorted_topics = sorted(topic_distribution, key=lambda x: x[1], reverse=True)
    topics_words = []
    for topic_id, _ in sorted_topics:
            topic_words = pretrained_lda_model.show_topic(topic_id)
            for word, prob in topic_words:
                topics_words.append(f"\t{word} (Probability: {prob:.3f})")
    return  topic_words







    