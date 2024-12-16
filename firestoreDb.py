import firebase_admin
from firebase_admin import credentials, firestore
from config import Config as config

cred = credentials.Certificate(config.firestore_db_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
