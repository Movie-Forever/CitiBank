import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise SystemExit("MONGODB_URI is not set. Add it to BankAPI/.env first.")

try:
    print("Testing MongoDB connection from MONGODB_URI...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("[OK] Connection successful!")
    client.close()
except Exception as exc:
    print(f"[ERROR] Connection failed: {exc}")
