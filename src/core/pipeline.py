import os
from dotenv import load_dotenv
from groq import Groq
import requests

from src.core.retriever import Retriever

load_dotenv()


# --------------------------------------------------
# LLM Wrapper
# --------------------------------------------------
class LLMNode:
    def __init__(self, provider="ollama", api_key=None):
        self.provider = provider
        self.api_key = api_key

    def generate(self, messages, model=None, temperature=0.2):
        if self.provider == "groq":
            return self._call_groq(messages, model or "llama-3.1-8b-instant", temperature)
        elif self.provider == "openai":
            return self._call_openai(messages, model or "gpt-3.5-turbo", temperature)
        else:
            # Flatten messages for simple ollama interface if needed, or keep chat format
            prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            return self._call_ollama(prompt, model or "llama2")

    def _call_groq(self, messages, model, temperature):
        client = Groq(api_key=self.api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def _call_openai(self, messages, model, temperature):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        res = requests.post(url, headers=headers, json=data)
        return res.json()["choices"][0]["message"]["content"].strip()

    def _call_ollama(self, prompt, model):
        url = "http://localhost:11434/api/generate"
        data = {"model": model, "prompt": prompt, "stream": False}
        res = requests.post(url, json=data)
        return res.json().get("response", "").strip()


# --------------------------------------------------
# RAG Pipeline (Multi-Tenant + Strict)
# --------------------------------------------------
class RAGPipeline:
    def __init__(self):
        print("Initializing RAG Pipeline (Multi-Tenant Production Mode)...")

        self.retriever = Retriever()
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.api_key = (
            os.getenv("GROQ_API_KEY")
            if self.provider == "groq"
            else os.getenv("OPENAI_API_KEY")
        )

        self.llm = LLMNode(provider=self.provider, api_key=self.api_key)

    # --------------------------------------------------
    # Query Rewriting
    # --------------------------------------------------
    def rewrite_query(self, query):
        """
        Rewrite user queries to improve retrieval (expand synonyms, domain terms).
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a query optimizer for a furniture catalogue search engine.\n"
                    "Rewrite the user's query to include domain terms (dimensions, materials, etc.) "
                    "and handle synonyms. output ONLY the rewritten query."
                )
            },
            {"role": "user", "content": f"Rewrite this query: {query}"}
        ]
        # Use a faster/cheaper call if possible, or same LLM
        try:
             # simple pass-through if LLM call fails or for speed; 
             # ideally we'd call the LLM here.
             # rewritten = self.llm.generate(messages, temperature=0.1)
             # return rewritten
             pass
        except:
            pass
        
        return query


    # --------------------------------------------------
    # Visual Intent Detection
    # --------------------------------------------------
    def detect_visual_intent(self, query):
        keywords = [
            "image",
            "diagram",
            "picture",
            "photo",
            "illustration",
            "show",
            "visual",
            "look like"
        ]
        return any(k in query.lower() for k in keywords)

    # --------------------------------------------------
    # Main Run
    # --------------------------------------------------
    def run(self, query, tenant_id):
        if not tenant_id:
            return {"answer": "Error: Tenant ID is missing."}

        # 0. Query Expansion (Optional/Simple)
        # query = self.rewrite_query(query)

        # 1. Retrieval (Scoped by Tenant)
        text_results = self.retriever.search_text(query, tenant_id=tenant_id, top_k=5)
        
        image_results = []
        if self.detect_visual_intent(query):
            image_results = self.retriever.search_images(query, tenant_id=tenant_id, top_k=3)
            print(f"DEBUG: Found {len(image_results)} images for query '{query}'")

        # 2. Check Retrieval
        if not text_results and not image_results:
             return {
                "answer": "This information is not available in the uploaded catalogues.",
                "text_sources": [],
                "image_sources": [],
            }
        
        if not text_results and image_results:
             # Only images found (e.g. valid for visual queries on image-only PDFs)
             return {
                 "answer": "I found some relevant images, but no text descriptions were available.",
                 "text_sources": [],
                 "image_sources": image_results
             }

        # 3. Build Context
        context_blocks = []
        for doc in text_results:
            content = doc.get("content", "")
            source = doc.get("source_document", "Unknown")
            page = doc.get("page_number", "?")
            context_blocks.append(f"[Source: {source}, Page: {page}]\n{content}")
        
        # Add Image Metadata to Context so LLM knows what images are shown
        if image_results:
            image_meta_list = []
            for img in image_results:
                src = img.get("source_document", "Unknown")
                pg = img.get("page_number", "?")
                desc = img.get("content", "Product Image")
                image_meta_list.append(f"[Visual Source: {src}, Page: {pg}] - Description: {desc}")
            
            image_context = "The following images have been retrieved and are displayed to the user:\n" + "\n".join(image_meta_list)
            context_blocks.append(image_context)
        
        context_text = "\n\n".join(context_blocks)

        # 4. Generate Answer
        system_prompt = (
            "You are a production-grade RAG assistant for furniture catalogues.\n"
            "STRICT RULES:\n"
            "1. Answer ONLY using the provided Context.\n"
            "2. The Context includes both text chunks and descriptions of retrieved images.\n"
            "3. If the user asks for a picture or image and relevant visual sources are in the context, explicitly mention that you are showing those images from the specific page.\n"
            "4. If the exact answer is not in the Context, say exactly: 'This information is not available in the uploaded catalogues.'\n"
            "5. Do NOT hallucinate.\n"
            "6. Include citations using the format [Source Name, Page X].\n"
            "7. Treat model numbers and specifications as high priority."
        )

        user_prompt = f"""
Context:
{context_text}

Question:
{query}

Answer:
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        answer = self.llm.generate(messages)

        # 5. Filter Sources based on Answer
        # 5. Filter Sources (Modified: Always return relevant chunks for visibility)
        final_text_sources = []
        
        # Check for citations first
        import re
        citations = re.findall(r'\[(.*?),\s*Page\s*(\d+)\]', answer, re.IGNORECASE)
        
        if citations:
            cited_set = {(c[0].strip(), str(c[1]).strip()) for c in citations}
            for doc in text_results:
                doc_source = doc.get("source_document", "").strip()
                doc_page = str(doc.get("page_number", "")).strip()
                if (doc_source, doc_page) in cited_set:
                    final_text_sources.append(doc)
        
        # Fallback: If no citations or negative answer, still show top retrieved chunks
        # so user can see what was found.
        if not final_text_sources:
            final_text_sources = text_results

        return {
            "answer": answer,
            "text_sources": final_text_sources,
            "image_sources": image_results,
        }

    def close(self):
        self.retriever.close()