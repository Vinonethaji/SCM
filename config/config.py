from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

MONGODB_URL=os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL)

# Create a MongoDB client and connect to a database and collection
mydatabase = client['SCM']
user_collection = mydatabase['user']
shipment_collection = mydatabase['shipment']
device_collection = mydatabase["device_data"]



