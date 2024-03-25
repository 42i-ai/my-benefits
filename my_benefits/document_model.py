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
    
    def __init__(self, 
                 raw_database_dir: str = None, 
                 silver_database_dir: str = None, 
                 gold_database_dir: str = None
                 ):       
        if raw_database_dir is not None:
            self.raw_database_dir = raw_database_dir
        self.connection_raw = duckdb.connect(os.path.join(self.raw_database_dir, "raw.db"))
        
        if silver_database_dir is not None:
            self.silver_database_dir = silver_database_dir
        self.connection_silver = duckdb.connect(os.path.join(self.silver_database_dir, "silver.db"))
        
        if gold_database_dir is not None:
            self.gold_database_dir = gold_database_dir
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
    
    def get_raw_database_dir(self)->str:
        return os.path.join(self.raw_database_dir,"raw.db")
    
    def get_silver_database_dir(self)->str:
        return os.path.join(self.silver_database_dir,"silver.db")
    
    def get_gold_database_dir(self)->str:
        return os.path.join(self.gold_database_dir,"gold.db")