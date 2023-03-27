from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


db = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(db)
