import os
import pymongo
import torch

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import open_clip

load_dotenv()

# ---------------- CONFIG ----------------
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DATABASE_NAME", "GenAi")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "embeddings_rag")

TOP_K_TEXT = 5
TOP_K_IMAGE = 4

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class Retriever:
    def __init__(self):
        # MongoDB
        self.client = pymongo.MongoClient(MONGO_URI)
        self.collection = self.client[DB_NAME][COLLECTION_NAME]

        # Text embedding model
        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")

        # CLIP model for image retrieval
        self.clip_model, _, _ = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai"
        )
        self.clip_model = self.clip_model.to(DEVICE)
        self.clip_tokenizer = open_clip.get_tokenizer("ViT-B-32")

    # ---------------- UTILS ----------------
    @staticmethod
    def cosine_similarity(v1, v2):
        v1 = torch.tensor(v1)
        v2 = torch.tensor(v2)
        return torch.nn.functional.cosine_similarity(v1, v2, dim=0).item()

    # ---------------- TEXT SEARCH ----------------
    def search_text(self, query, tenant_id=None, top_k=TOP_K_TEXT):
        query_emb = self.text_model.encode(query)

        cursor = self.collection.find({
            "tenant_id": tenant_id,
            "type": "text"
        })

        # Keyword extract for boosting
        keywords = [word.lower() for word in query.split() if len(word) > 3]

        scored = []
        for doc in cursor:
            if "embedding_text" not in doc:
                continue
            
            # Vector Score
            vec_score = self.cosine_similarity(query_emb, doc["embedding_text"])
            
            # Keyword Boost
            content_lower = doc.get("content", "").lower()
            boost = 0
            for kw in keywords:
                if kw in content_lower:
                    boost += 0.15 # Strong boost for keyword matches
            
            total_score = vec_score + boost
            scored.append((total_score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        # Add score to each doc
        for s, d in scored:
            d["score"] = s
            
        return [d for _, d in scored[:top_k]]

    # ---------------- IMAGE SEARCH (TRUE MULTIMODAL) ----------------
    def search_images(self, query, tenant_id=None, top_k=TOP_K_IMAGE):
        tokens = self.clip_tokenizer([query]).to(DEVICE)
        with torch.no_grad():
            query_emb = self.clip_model.encode_text(tokens)[0].cpu().tolist()

        cursor = self.collection.find({
            "tenant_id": tenant_id,
            "type": "image"
        })

        scored = []
        for doc in cursor:
            if "embedding_clip" not in doc:
                continue
            score = self.cosine_similarity(query_emb, doc["embedding_clip"])
            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        # Add score to each doc
        for s, d in scored:
            d["score"] = s

        return [d for _, d in scored[:top_k]]

    # ---------------- HYBRID ----------------
    def search_hybrid(self, query, tenant_id=None):
        return {
            "text": self.search_text(query, tenant_id),
            "images": self.search_images(query, tenant_id)
        }

    def close(self):
        self.client.close()
