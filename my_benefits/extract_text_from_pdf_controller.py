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
from datetime import datetime
import logging


class ExtractTextFromPDFController:

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        self.nlp = spacy.load(spacy_model)
        now = datetime.now()
        formatted_date_time = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.logger = logging.getLogger('debug_logger')
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(
            f'./my_benefits/logs/extract-pdf-{formatted_date_time}.log')

        self.file_handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.debug(
            f"""Initializing extract text from pdf controller""")

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
            self.logger.debug(
                f"""Processing document - file documents - {file}""")
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
            self.logger.debug(
                f"""Pages loaded from documents - {len(df)}""")
        return df

    # TODO: Write test for this method
    def process_pdf_file(self, pdf_file_path: str, pdf_filename: str) -> pl.DataFrame:
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

        document = fitz.open(os.path.join(pdf_file_path, pdf_filename))
        self.logger.debug(
            f"""Processing document - file documents - {pdf_filename}""")
        page_number: int = 0
        for page in document:
            page_number += 1
            row: Dictionary = {
                "filename": pdf_filename,
                "page_number": page_number,
                "text": page.get_text().replace("\n", "  ")
            }
            row_df = pl.DataFrame([row])
            df = pl.concat([df, row_df])
        self.logger.debug(
            f"""Pages loaded from documents - {len(df)}""")
        return df
