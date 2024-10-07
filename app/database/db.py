# app/database/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("DB_HOST"))
db = client[os.getenv("DB")]

def get_db():
    return db
