from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os

### DB link
def linkdb():
    if not os.path.exists("/.dockerenv"):
        from dotenv import load_dotenv
        load_dotenv()
    link = {
        'DB_SERVER': os.getenv('DB_SERVER') , 
        'DB_DATABASE':os.getenv('DB_DATABASE'),
        'DB_UID':os.getenv('DB_UID'),
        'DB_PWD':os.getenv('DB_PWD'),
    }
    params = quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={link['DB_SERVER']}\\SQLEXPRESS;"
        f"DATABASE={link['DB_DATABASE']};"
        f"UID={link['DB_UID']};"
        f"PWD={link['DB_PWD']};"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    try:
        return engine.connect()
    except Exception as e:
        return "連線失敗"