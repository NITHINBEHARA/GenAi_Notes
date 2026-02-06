import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.pipeline import RAGPipeline


def main():
    print("Initializing RAG System...")

    current_tenant_id = "tenant_123"

    try:
        rag = RAGPipeline()
    except Exception as e:
        print(f"❌ Failed to initialize RAG Pipeline: {e}")
        return

    print("\n=== RAG System Ready ===")
    print(f"Active Tenant: {current_tenant_id}")
    print("Type 'exit' or 'quit' to stop.")
    print("Ask a question about your documents!")

    while True:
        try:
            query = input("\nMy Question: ").strip()

            if query.lower() in ("exit", "quit"):
                break
            if not query:
                continue

            print(f"\nThinking (Tenant: {current_tenant_id})...\n")
            result = rag.run(query, tenant_id=current_tenant_id)

            # ---------------- ANSWER ----------------
            print("=" * 60)
            print("ANSWER:\n")
            print(result.get("answer", "No answer generated."))
            print("=" * 60)

            # ---------------- TEXT SOURCES ----------------
            text_sources = result.get("text_sources", [])

            if text_sources:
                print("\nTEXT SOURCES:")
                seen = set()

                for doc in text_sources:
                    src_doc = doc.get("source_document")
                    pg_num = doc.get("page_number")

                    key = (src_doc, pg_num)
                    if key in seen:
                        continue
                    seen.add(key)

                    score = doc.get("score")
                    score_str = ""
                    if score is not None:
                        try:
                            score_str = f" | Score: {float(score):.4f}"
                        except Exception:
                            pass

                    print(f"- {src_doc} | Page {pg_num}{score_str}")
            else:
                print("\nNo strong textual sources found.")

            # ---------------- IMAGE SOURCES ----------------
            image_sources = result.get("image_sources", [])

            if image_sources:
                print(f"\nIMAGE SOURCES ({len(image_sources)} found):")
                for img in image_sources:
                    src_doc = img.get("source_document")
                    pg_num = img.get("page_number")
                    image_path = img.get("image_path")
                    # Debug print
                    # print(f"DEBUG IMG DOC: {img}")

                    print(f"- {src_doc} | Page {pg_num}")
                    print(f"  Image Path: {image_path}")
            else:
                print("\nNo relevant images found.")

        except KeyboardInterrupt:
            print("\nUser interrupted.")
            break
        except Exception as e:
            print(f"❌ Error during query processing: {e}")
            import traceback
            traceback.print_exc()

    print("\nClosing RAG System...")
    rag.close()


if __name__ == "__main__":
    main()
