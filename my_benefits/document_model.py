import os
from datetime import datetime
import logging
import duckdb
import polars as pl
from enum import Enum, auto


class DataLayerType(Enum):
    RAW = auto()
    SILVER = auto()
    GOLD = auto()


class DocumentsModel:

    raw_database_dir: str = "./my_benefits/raw/"
    silver_database_dir: str = "./my_benefits/silver/"
    gold_database_dir: str = "./my_benefits/gold/"

    def __init__(self,
                 raw_database_dir: str = None,
                 silver_database_dir: str = None,
                 gold_database_dir: str = None
                 ):
        now = datetime.now()
        formatted_date_time = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.logger = logging.getLogger('debug_logger')
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(
            f'./my_benefits/logs/document-model-{formatted_date_time}.log')
        self.file_handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.debug(
            f"""Initializing document model""")

        if raw_database_dir is not None:
            self.raw_database_dir = raw_database_dir
        self.connection_raw = duckdb.connect(
            os.path.join(self.raw_database_dir, "raw.db"))

        if silver_database_dir is not None:
            self.silver_database_dir = silver_database_dir
        self.connection_silver = duckdb.connect(
            os.path.join(self.silver_database_dir, "silver.db"))

        if gold_database_dir is not None:
            self.gold_database_dir = gold_database_dir
        self.connection_gold = duckdb.connect(
            os.path.join(self.gold_database_dir, "gold.db"))

        self.connection_raw.execute("""CREATE 
                                       TABLE 
                                       IF NOT EXISTS
                                       document_pages 
                                       (
                                        filename TEXT, 
                                        page_number INTEGER, 
                                        text TEXT,
                                        is_ocr BOOLEAN   
                                       )
                                    """)

        self.connection_silver.execute("""CREATE 
                                       TABLE 
                                       IF NOT EXISTS
                                       document_pages 
                                       (
                                        filename TEXT, 
                                        page_number INTEGER, 
                                        text TEXT,
                                        is_ocr BOOLEAN,
                                        tokenized_text TEXT[]
                                       )
                                    """)

    def add_document_page_raw(self, df: pl.DataFrame):
        self.logger.debug(
            f"""Cleannig raw tables""")
        self.connection_raw.sql("Delete from document_pages")
        self.connection_raw.sql("INSERT INTO document_pages SELECT * FROM df")
        self.logger.debug(f"""Documents wrote on raw database - table document_pages {
            len(df)} documents""")

    def add_document_page_silver(self, df: pl.DataFrame):
        self.logger.debug(
            f"""Cleannig silver tables""")
        self.connection_raw.sql("Delete from document_pages")
        self.connection_silver.sql(
            "INSERT INTO document_pages SELECT * FROM df")
        self.logger.debug(f"""Documents wrote on silver database - table document_pages {
            len(df)}""")

    def get_raw_database_dir(self) -> str:
        return os.path.join(self.raw_database_dir, "raw.db")

    def get_silver_database_dir(self) -> str:
        return os.path.join(self.silver_database_dir, "silver.db")

    def get_gold_database_dir(self) -> str:
        return os.path.join(self.gold_database_dir, "gold.db")
