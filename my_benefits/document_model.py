import os
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
   
    def __init__(self):       
        self.connection_raw = duckdb.connect(os.path.join(self.raw_database_dir, "raw.db"))
        self.connection_silver = duckdb.connect(os.path.join(self.silver_database_dir, "silver.db"))
        self.connection_gold = duckdb.connect(os.path.join(self.gold_database_dir, "gold.db"))
        self.connection_raw.execute("""CREATE 
                                       TABLE 
                                       IF NOT EXISTS
                                       document_pages 
                                       (
                                        filename TEXT, 
                                        page_number INTEGER, 
                                        text TEXT
                                       )
                                    """)

    def add_document_page_raw(self, df: pl.DataFrame):
        self.connection_raw.sql("INSERT INTO document_pages SELECT * FROM df")
        ##self.connection_raw.execute(f"INSERT INTO document_pages VALUES ('{filename}', {page_number}, '{text}')")

