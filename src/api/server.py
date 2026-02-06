import os
import sys
import json
from bson import ObjectId

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.core.pipeline import RAGPipeline
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define Data Directory
# We are in project/src/api/server.py, so we need to go up 3 levels to reach project/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Point to actual extraction folder
IMAGES_DIR = os.path.join(BASE_DIR, "extracted_images")
DOCS_DIR = os.path.join(BASE_DIR, "data")
print(f"DEBUG: IMAGES_DIR set to: {IMAGES_DIR}")
print(f"DEBUG: DOCS_DIR set to: {DOCS_DIR}")

# Custom JSON Encoder for ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json_encoder = JSONEncoder

# Initialize RAG Pipeline
try:
    print("Starting RAG Server...")
    rag = RAGPipeline()
except Exception as e:
    print(f"Failed to initialize RAG Pipeline: {e}")
    rag = None

def serialize_mongo_doc(doc):
    """Recursively convert ObjectId to str in a document/dict."""
    if isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    if isinstance(doc, dict):
        return {k: serialize_mongo_doc(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc

@app.route('/')
def root():
    return jsonify({
        "status": "running",
        "service": "RAG Backend API",
        "endpoints": {
            "query": "/api/rag/query",
            "login": "/api/auth/login",
            "documents": "/api/documents/list",
            "serve_doc": "/api/documents/serve/<filename>"
        }
    })

# Serve images recursively from the extracted_images folder
@app.route('/api/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

# Serve PDF documents
@app.route('/api/documents/serve/<path:filename>')
def serve_document(filename):
    # Check if file exists in root of data
    if os.path.exists(os.path.join(DOCS_DIR, filename)):
        return send_from_directory(DOCS_DIR, filename)
    
    # Check "original" folder fallback
    if os.path.exists(os.path.join(DOCS_DIR, "original", filename)):
         return send_from_directory(os.path.join(DOCS_DIR, "original"), filename)
         
    return jsonify({"error": "File not found"}), 404

@app.route('/api/rag/query', methods=['POST'])
def query_rag():
    if not rag:
        return jsonify({"error": "RAG system not initialized"}), 500

    data = request.json
    query_text = data.get('query')
    tenant_id = request.headers.get('X-Tenant-ID', 'tenant_123')
    if not tenant_id or tenant_id == 'undefined' or tenant_id == 'null':
        tenant_id = 'tenant_123'

    if not query_text:
        return jsonify({"error": "No query provided"}), 400

    print(f"Processing query: {query_text} for tenant: {tenant_id}")
    
    try:
        result = rag.run(query_text, tenant_id=tenant_id)
        
        def inject_pdf_url(item):
            src_doc = item.get("source_document")
            page_num = item.get("page_number")
            if src_doc:
                url = f"{request.host_url}api/documents/serve/{src_doc}"
                if page_num:
                    url += f"#page={page_num}"
                item["pdf_url"] = url
        
        # Inject Image URLs & PDF Links
        if result.get("image_sources"):
            for img in result["image_sources"]:
                # DB path: extracted_images\tenant_123\file.jpg
                raw_path = img.get("image_path", "")
                
                # Normalize path separators
                raw_path = raw_path.replace("\\", "/")
                
                # We want the part after "extracted_images/"
                if "extracted_images/" in raw_path:
                    relative_path = raw_path.split("extracted_images/")[-1]
                    img["url"] = f"{request.host_url}api/images/{relative_path}"
                else:
                    img["url"] = f"{request.host_url}api/images/{os.path.basename(raw_path)}"
                
                # Inject PDF URL
                inject_pdf_url(img)

        # Inject PDF Links for Text Sources
        if result.get("text_sources"):
            for txt in result["text_sources"]:
                inject_pdf_url(txt)

        # Manually serialize result to ensure clean JSON
        clean_result = serialize_mongo_doc(result)
        print(f"DEBUG: Internal result keys: {result.keys()}")
        print(f"DEBUG: Sending response to frontend. Answer length: {len(clean_result.get('answer', ''))}")
        print(f"DEBUG: Sample Answer: {clean_result.get('answer', '')[:50]}...")
        return jsonify(clean_result)
    except Exception as e:
        print(f"Error processing query: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', 'admin@example.com')
    return jsonify({
        "token": "mock_token_xyz",
        "tenant_id": "tenant_123",
        "user": {"email": email, "name": "Admin User"}
    })

@app.route('/api/documents/list', methods=['GET'])
def list_documents():
    return jsonify([
        {"id": "1", "name": "20558_Schrankinnenausstattung_Katalog_2025_EN_2008_300dpi.pdf", "upload_date": "2025-02-01"}
    ])

if __name__ == '__main__':
    # Use 0.0.0.0 to ensure it's accessible externally if needed
    # and debug=True to see errors in the terminal
    print("\n" + "="*50)
    print("RAG API SERVER STARTING")
    print("Port: 5000")
    print("Endpoints:")
    print("  - POST /api/rag/query")
    print("  - POST /api/auth/login")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
