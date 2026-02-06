import os
import argparse
import fitz  # PyMuPDF
import pymongo
import torch
import open_clip
import numpy as np
from dotenv import load_dotenv
from PIL import Image
from sentence_transformers import SentenceTransformer

load_dotenv()

class IngestionPipeline:
    """
    Multimodal Ingestion Pipeline for PDF documents.
    Extracts text and images, generates embeddings, and stores them in MongoDB.
    """
    def __init__(self):
        print("🧠 Initializing Ingestion Pipeline...")
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("DATABASE_NAME", "GenAi")
        self.collection_name = os.getenv("COLLECTION_NAME", "embeddings_rag")
        self.image_dir = "extracted_images"
        
        # Load Models
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.text_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.clip_model, _, self.clip_preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained="openai"
        )
        self.clip_model.to(self.device)
        print(f"✅ Models loaded on {self.device}")

    def _chunk_text(self, text, max_len=1000, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            chunk = text[start:start + max_len].strip()
            if len(chunk) > 30:
                chunks.append(chunk)
            start += max_len - overlap
        return chunks

    def _embed_text(self, text):
        emb = self.text_model.encode(text)
        return (emb / np.linalg.norm(emb)).tolist()

    def _embed_clip_image(self, image_path):
        image = self.clip_preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            emb = self.clip_model.encode_image(image)
            emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb[0].cpu().tolist()

    def run(self, file_path, tenant_id):
        if not os.path.exists(file_path):
            print(f"❌ PDF not found: {file_path}")
            return

        client = pymongo.MongoClient(self.mongo_uri)
        collection = client[self.db_name][self.collection_name]
        file_name = os.path.basename(file_path)

        print(f"\n🚀 Ingesting: {file_name} | Tenant: {tenant_id}")

        # Clean existing data for this file/tenant
        collection.delete_many({
            "tenant_id": tenant_id,
            "source_document": file_name
        })

        doc = fitz.open(file_path)
        records = []
        os.makedirs(os.path.join(self.image_dir, tenant_id), exist_ok=True)

        for page_index, page in enumerate(doc):
            page_number = page_index + 1
            print(f"📄 Processing Page {page_number}...")

            # Extract Text
            text = page.get_text()
            for chunk in self._chunk_text(text):
                records.append({
                    "tenant_id": tenant_id,
                    "type": "text",
                    "content": chunk,
                    "embedding_text": self._embed_text(chunk),
                    "page_number": page_number,
                    "source_document": file_name
                })

            # Extract Images
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                ext = base_image["ext"]
                image_name = f"{file_name}_p{page_number}_{img_index}.{ext}"
                image_path = os.path.join(self.image_dir, tenant_id, image_name)

                with open(image_path, "wb") as f:
                    f.write(base_image["image"])

                records.append({
                    "tenant_id": tenant_id,
                    "type": "image",
                    "content": f"Image from {file_name} page {page_number}",
                    "image_path": image_path,
                    "embedding_clip": self._embed_clip_image(image_path),
                    "page_number": page_number,
                    "source_document": file_name
                })

        if records:
            collection.insert_many(records)
            print(f"✅ Successfully inserted {len(records)} records")

        client.close()
        print("🎬 Ingestion completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Multimodal RAG Ingestion Pipeline")
    parser.add_argument("file_path", help="Path to the PDF file")
    parser.add_argument("--tenant", default="tenant_123", help="Tenant ID")
    args = parser.parse_args()

    pipeline = IngestionPipeline()
    pipeline.run(args.file_path, args.tenant)
