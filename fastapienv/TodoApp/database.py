from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATA_URL = 'sqlite:///./todos.db'

engine = create_engine(SQLALCHEMY_DATA_URL, connect_args={'check_same_thread': False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #telling them you want to have full control of the database
Base = declarative_base()

#inserting into DB