from sqlalchemy.orm import sessionmaker
from models import db

def get_db_session():
    '''Dependency to get a database session'''
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()