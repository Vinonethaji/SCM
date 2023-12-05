from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

MONGODB_URL=os.getenv("MONGODB_URL")

conn = MongoClient(MONGODB_URL)

client = conn


# Create a MongoDB client and connect to a database and collection
mydatabase = client['SCM']
signup_collection = mydatabase['SignUP']
Createshipment_collection = mydatabase['Createshipment']
device_collection = mydatabase["device_data"]
# token_blacklist_collection = mydatabase['token_blacklist']


