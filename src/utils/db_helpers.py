import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DATABASE_NAME", "GenAi")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "embeddings_rag")

def get_collection():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION_NAME], client

def verify_tenant_data(tenant_id):
    """Checks document counts and samples for a specific tenant."""
    col, client = get_collection()
    print(f"\n--- Verifying Data for Tenant: {tenant_id} ---")
    
    count = col.count_documents({"tenant_id": tenant_id})
    text_count = col.count_documents({"tenant_id": tenant_id, "type": "text"})
    image_count = col.count_documents({"tenant_id": tenant_id, "type": "image"})
    
    print(f"Total: {count} | Text: {text_count} | Images: {image_count}")
    
    # List distinct pages
    pages = sorted(col.distinct("page_number", {"tenant_id": tenant_id}))
    print(f"Indexed Pages: {pages}")
    
    client.close()

def wipe_tenant_data(tenant_id):
    """Deletes all records for a specific tenant."""
    col, client = get_collection()
    print(f"⚠️ Wiping all data for tenant: {tenant_id}")
    result = col.delete_many({"tenant_id": tenant_id})
    print(f"✅ Deleted {result.deleted_count} records.")
    client.close()

if __name__ == "__main__":
    # Example usage for CLI
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        tenant = sys.argv[2] if len(sys.argv) > 2 else "tenant_123"
        
        if cmd == "verify":
            verify_tenant_data(tenant)
        elif cmd == "wipe":
            wipe_tenant_data(tenant)
