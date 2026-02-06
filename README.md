# Production-Ready Multimodal RAG System

A production-grade, multi-tenant Retrieval-Augmented Generation (RAG) system with support for text and image retrieval from PDF documents.

## 📁 Project Structure

```text
Rag_project/
├── src/
│   ├── ingest.py         # Data Ingestion Pipeline (Text & Images)
│   ├── retriever.py      # Search Engine (Hybrid Vector + Keyword Match)
│   ├── rag_pipeline.py   # RAG Orchestrator (LLM Logic + Citations)
│   ├── server.py         # Flask API Server for Web Frontend
│   ├── app.py            # CLI Application for Terminal Usage
│   └── utils/            # Maintenance & Debugging Tools
│       ├── verify_db.py     # Check database health
│       ├── wipe_db.py       # Clear tenant data
│       └── inspect_pdf.py   # Debug PDF text extraction
├── frontend/             # React (Vite) Search Interface
├── extracted_images/     # Local storage for extracted PDF images
└── data/                 # Source PDF documents
```

## 🚀 Quick Start

### 1. Backend Setup
1. **Environment**: Create a `.env` file in the root with:
   ```env
   MONGODB_URI="your_mongodb_uri"
   GROQ_API_KEY="your_api_key"
   LLM_PROVIDER="groq"
   ```
2. **Ingest Data**:
   ```bash
   python src/ingest.py data/your_catalog.pdf --tenant tenant_123
   ```
3. **Run Server**:
   ```bash
   python src/server.py
   ```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🛠 Features

- **Hybrid Search**: Combines vector embeddings with keyword boosting for high-precision results (e.g., finding specific product names like "Lario").
- **Multimodal**: Automatically extracts images from PDFs and allows users to search for visuals via CLIP embeddings.
- **Deep Linking**: Citations in the UI include direct links to the exact PDF page (`#page=N`).
- **Multi-Tenant**: Scoped retrieval using `tenant_id` headers.

## 🧪 Testing and Debugging
Use the scripts in `src/utils/` to verify your data:
```bash
python src/utils/verify_db.py  # Checks document counts and samples
```
