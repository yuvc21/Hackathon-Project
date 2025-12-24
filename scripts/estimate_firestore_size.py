#yet to be implemented
import os
import json
from google.cloud import firestore

# Make sure this env var points to your service account JSON
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccount.json"

project_id = "YOUR_PROJECT_ID"
db = firestore.Client(project=project_id)

def estimate_collection_size(collection_name: str) -> int:
    """Return rough size in bytes of all docs in a collection."""
    docs = db.collection(collection_name).stream()
    total_bytes = 0

    for doc in docs:
        data = doc.to_dict() or {}
        # include document id as well
        data["_id"] = doc.id
        # serialize to JSON bytes
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        total_bytes += len(encoded)

    return total_bytes

def estimate_db_size(root_collections=None):
    if root_collections is None:
        root_collections = [c.id for c in db.collections()]

    sizes = {}
    total = 0
    for col in root_collections:
        size = estimate_collection_size(col)
        sizes[col] = size
        total += size

    return sizes, total

if __name__ == "__main__":
    sizes, total = estimate_db_size()
    print("Per‑collection (approx):")
    for col, sz in sizes.items():
        print(f"  {col}: {sz/1024:.2f} KB")

    print(f"\nApprox total: {total/1024/1024:.3f} MB")