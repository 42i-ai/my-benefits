"""This module provides a function to extract text from a PDF file"""
import os
import shutil
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
from pdf2image import convert_from_path
from PIL import Image
import pytesseract


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
    # TODO: Check how to improve using threads

    def process_pdf_files_ocr(self, pdf_file_path: str, image_conversion_path: str) -> pl.DataFrame:
        """
        Extract text from ocr pfd  from a PDF file and retun as a list of strings.
        Parameters: 
        """

        schema = [
            ("filename", pl.String),
            ("page_number", pl.Int64),
            ("text", pl.String),
            ("is_ocr", pl.Boolean)
        ]
        df = pl.DataFrame({name: pl.Series([], dtype=dtype)
                          for name, dtype in schema})
        folder_name = ''
        for file in os.listdir(pdf_file_path):
            images = convert_from_path(os.path.join(pdf_file_path, file))
            folder_name = file.lower().replace(
                ' ', '').replace('.pdf', '')
            if os.path.isdir(os.path.join(image_conversion_path, folder_name)):
                shutil.rmtree(os.path.join(
                    image_conversion_path, folder_name))
            os.makedirs(os.path.join(image_conversion_path, folder_name))
            for i, image in enumerate(images):
                image.save(os.path.join(image_conversion_path,
                           folder_name, f'page_{i}.jpg'), 'JPEG')
            page_number: int = 0
            for page in os.listdir(os.path.join(image_conversion_path, folder_name)):
                page_number += 1
                page_image = Image.open(os.path.join(
                    image_conversion_path, folder_name, page))
                text = pytesseract.image_to_string(page_image)
                row: Dictionary = {
                    "filename": file,
                    "page_number": page_number,
                    "text": text.replace("\n", "  "),
                    "is_ocr": True
                }
                row_df = pl.DataFrame([row])
                df = pl.concat([df, row_df])

        return df

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
            ("text", pl.String),
            ("is_ocr", pl.Boolean)
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
                    "text": page.get_text().replace("\n", "  "),
                    "is_ocr": False
                }
                row_df = pl.DataFrame([row])
                df = pl.concat([df, row_df])
            self.logger.debug(
                f"""Pages loaded from documents - {len(df)}""")
        return df
