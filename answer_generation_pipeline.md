from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

# ---- MongoDB Config ----
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")

# ---- Embeddings (FREE, local) ----
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ---- MongoDB Vector Store ----
client = MongoClient(MONGODB_URI)
collection = client[DB_NAME][COLLECTION_NAME]

db = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embedding_model,
    index_name=INDEX_NAME
)

# ---- User Query ----
query = "How much did Microsoft pay to acquire GitHub?"

retriever = db.as_retriever(search_kwargs={"k": 5})
docs = retriever.invoke(query)

# ---- Build RAG Prompt ----
context = "\n".join([doc.page_content for doc in docs])

prompt = f"""
You are a RAG assistant.

Answer the question using ONLY the context below.
If the answer is not present, say:
"I don't have enough information."

Context:
{context}

Question:
{query}
"""

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",  # recommended
    temperature=0
)

messages = [
    SystemMessage(content="You are a precise, factual assistant."),
    HumanMessage(content=prompt),
]

# ---- Generate Answer ----
response = llm.invoke(messages)

print("\n--- RAG Answer (Groq) ---")
print(response.content)
