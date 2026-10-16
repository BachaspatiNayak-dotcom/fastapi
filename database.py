from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("db_url")

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)