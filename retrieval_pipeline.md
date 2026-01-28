from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# ---- MongoDB Config ----
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")

# ---- Embedding Model (MUST match ingestion model) ----
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ---- Connect to MongoDB ----
client = MongoClient(MONGODB_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# ---- Load Vector Store from MongoDB ----
db = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embedding_model,
    index_name=INDEX_NAME
)

# ---- User Query ----
query = "How much did Microsoft pay to acquire GitHub?"

# ---- Retriever (Top-K Similarity Search) ----
retriever = db.as_retriever(
    search_kwargs={"k": 1}
)

# ---- Retrieve Documents ----
relevant_docs = retriever.invoke(query)

print(f"User Query: {query}")
print("--- Context ---")

for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}:\n{doc.page_content}\n")
