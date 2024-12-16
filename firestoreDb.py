from google.cloud import firestore
from config import Config as config

# Initialize Firestore client
db = firestore.Client.from_service_account_json(config.firestore_db_path)