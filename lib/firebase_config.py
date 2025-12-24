import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("/home/yuvaraj/hackathon-project/Hackathon-project/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Firestore database client
db = firestore.client()

def save_to_firestore(collection: str, data: dict):
    """Save data to Firestore collection"""
    doc_ref = db.collection(collection).add(data)
    return doc_ref[1].id

def get_from_firestore(collection: str, limit=10):
    """Read data from Firestore collection"""
    docs = db.collection(collection).limit(limit).stream()
    return [doc.to_dict() for doc in docs]
