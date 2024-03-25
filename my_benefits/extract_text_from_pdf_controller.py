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
