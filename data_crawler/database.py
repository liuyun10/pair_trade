from pymongo import MongoClient

# database_01
DB_CONN = MongoClient('mongodb://127.0.0.1:27017')['database_01']