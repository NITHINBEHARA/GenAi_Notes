from dotenv import load_dotenv
import os

from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# Embeddings (FREE, local)
# --------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# --------------------------------------------------
# MongoDB Vector Store
# --------------------------------------------------
client = MongoClient(MONGODB_URI)
collection = client[DB_NAME][COLLECTION_NAME]

db = MongoDBAtlasVectorSearch(
    collection=collection,
    embedding=embeddings,
    index_name=INDEX_NAME
)

# --------------------------------------------------
# LLM (Groq – fast & cheap)
# --------------------------------------------------
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# --------------------------------------------------
# Conversation memory
# --------------------------------------------------
chat_history = []

# --------------------------------------------------
# Ask Question (History-Aware RAG)
# --------------------------------------------------
def ask_question(user_question):
    print(f"\n--- You asked: {user_question} ---")

    # STEP 1: Rewrite question using history (history-aware)
    if chat_history:
        rewrite_messages = [
            SystemMessage(
                content="Given the chat history, rewrite the new question into a standalone question. Return ONLY the rewritten question."
            ),
            *chat_history,
            HumanMessage(content=user_question)
        ]

        rewritten = model.invoke(rewrite_messages)
        search_question = rewritten.content.strip()
        print(f"🔍 Rewritten question: {search_question}")
    else:
        search_question = user_question

    # STEP 2: Retrieve relevant docs from MongoDB
    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(search_question)

    print(f"📄 Found {len(docs)} documents")

    # STEP 3: Build context
    context = "\n".join(doc.page_content for doc in docs)

    final_prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say:
"I don't have enough information."

Context:
{context}

Question:
{user_question}
"""

    # STEP 4: Generate answer (history + context)
    messages = [
        SystemMessage(content="You are a precise RAG assistant."),
        *chat_history,
        HumanMessage(content=final_prompt)
    ]

    response = model.invoke(messages)
    answer = response.content

    # STEP 5: Save history
    chat_history.append(HumanMessage(content=user_question))
    chat_history.append(AIMessage(content=answer))

    print(f"\n✅ Answer:\n{answer}")
    return answer

# --------------------------------------------------
# Chat loop
# --------------------------------------------------
def start_chat():
    print("Ask questions (type 'quit' to exit)")
    while True:
        q = input("\nYour question: ")
        if q.lower() == "quit":
            print("Goodbye 👋")
            break
        ask_question(q)

if __name__ == "__main__":
    start_chat()
