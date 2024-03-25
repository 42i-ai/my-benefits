import duckdb
from enum import Enum, auto

class DataLayerType(Enum):
    RAW = auto()
    SILVER = auto()
    GOLD = auto()


class MyBenefitsModel:
    
    raw_database_dir: str = "./my_benefits/raw"
    silver_database_dir: str = "./my_benefits/silver"
    gold_database_dir: str = "./my_benefits/gold"
   
    def __init__(self):       
        self.connection_raw = duckdb.connect(self.raw_database_dir)
        self.connection_silver = duckdb.connect(self.silver_database_dir)
        self.connection_gold = duckdb.connect(self.gold_database_dir)
        self.connection_raw.execute("""CREATE 
                                       TABLE 
                                       document_pages 
                                       (
                                        filename TEXT, 
                                        page_number INTEGER, 
                                        text TEXT
                                       )
                                    """)

    def add_document_page_raw(self, filename: str, page_number: int, text: str):
        self.connection_raw.execute(f"INSERT INTO document_pages VALUES ('{filename}', {page_number}, '{text}')")

