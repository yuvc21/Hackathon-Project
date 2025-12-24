from lib.firebase_config import save_to_firestore, get_from_firestore

# Write test
print("Writing to Firebase...")
doc_id = save_to_firestore("test_collection", {
    "message": "Firebase working!",
    "project": "MSME Payment Automation"
})
print(f"✅ Saved with ID: {doc_id}")

# Read test
print("\nReading from Firebase...")
docs = get_from_firestore("test_collection")
print(f"✅ Found {len(docs)} documents:")
for doc in docs:
    print(f"   {doc}")