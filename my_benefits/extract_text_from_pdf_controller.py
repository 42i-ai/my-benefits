"""This module provides a function to extract text from a PDF file"""
import os
import re
import spacy
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from typing import List, Tuple
from array import array
import fitz
import polars as pl


class ExtractTextFromPDFController:

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        self.nlp = spacy.load(spacy_model)

    def process_pdf_files(self, pdf_file_path: str) -> pl.DataFrame:
        """
        Extract text from each page from a PDF file and retun as a list of strings.
        Parameters:
        fitz.Documents: the result of the processing of the library pymupdf.
        Returns:
        list: a list of strings where each position is a page from the pdf.
        """
        schema = [
            ("filename", pl.String),
            ("page_number", pl.Int64),
            ("text", pl.String)
        ]
        df = pl.DataFrame({name: pl.Series([], dtype=dtype)
                          for name, dtype in schema})

        for file in os.listdir(pdf_file_path):
            document = fitz.open(os.path.join(pdf_file_path, file))
            page_number: int = 0
            for page in document:
                page_number += 1
                row: Dictionary = {
                    "filename": file,
                    "page_number": page_number,
                    "text": page.get_text().replace("\n", "  ")
                }
                row_df = pl.DataFrame([row])
                df = pl.concat([df, row_df])
        return df


# def load_pretrained_model(path_to_serialize : str) -> Tuple[LdaModel, Dictionary] :
#     """_summary_

#     Args:
#         path_to_serialize (str): _description_

#     Returns:
#         Tuple[LdaModel, Dictionary]: _description_
#     """
#     pretrained_lda_model = LdaModel.load(os.path.join(path_to_serialize,'pretrained_lda_model.model'))
#     pretrained_dictionary = corpora.Dictionary.load(os.path.join(path_to_serialize,'pretrained_dictionary.dict'))
#     return pretrained_lda_model, pretrained_dictionary

# def get_list_of_topics_from_document(preprocessed_docs : List[str], path_pretrained_model : str)-> List[str]:
#     """_summary_
#     """
#     pretrained_lda_model, pretrained_dictionary  = load_pretrained_model(path_pretrained_model)
#     new_corpus = [pretrained_dictionary.doc2bow(doc) for doc in preprocessed_docs]
#     # Classify the new documents using the pre-trained LDA model
#     for i, doc_bow in enumerate(new_corpus):
#         print(f"Document {i+1}:")
#         topic_distribution = pretrained_lda_model[doc_bow]
#         sorted_topics = sorted(topic_distribution, key=lambda x: x[1], reverse=True)
#     topics_words = []
#     for topic_id, _ in sorted_topics:
#             topic_words = pretrained_lda_model.show_topic(topic_id)
#             for word, prob in topic_words:
#                 topics_words.append(f"\t{word} (Probability: {prob:.3f})")
#     return  topic_words
