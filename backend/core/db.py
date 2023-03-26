from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import user_management

def get_db(is_test=False):
    engine = create_engine("sqlite:///mydatabase.db") if not is_test else create_engine("sqlite:///test_mydatabase.db")
    user_management.create_tables(engine)
    SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionMaker()


def close_db(session):
    session.close()