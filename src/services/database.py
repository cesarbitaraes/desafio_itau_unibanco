"""
Funções relacionadas a conexão com banco de dados.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.settings import DB_CONNECTION_STRING

connection_pool = create_engine(DB_CONNECTION_STRING, pool_size=10, max_overflow=0, echo=False)
Session = sessionmaker(bind=connection_pool)
BaseModel = declarative_base()


def get_conn():
    """
    Pega uma conexão do pool e retorna.
    """
    conn = Session()
    try:
        yield conn
    except Exception as error:
        raise error
    finally:
        conn.close()
