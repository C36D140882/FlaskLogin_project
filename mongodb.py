from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri=os.getenv('MONGO_URI','mongodb://localhost:27017')
db_name=os.getenv('DB_NAME')
client=MongoClient(mongo_uri)
db=client[db_name]
collection=db['userData']