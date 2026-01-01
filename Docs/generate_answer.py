import chromadb
import os
from openai import OpenAI

CHROMA_DIR = "chroma_data"
COLLECTION_NAME = "risk_fraud_sops"
<<<<<<< HEAD
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
=======
OPENAI_API_KEY = ("OPENAI_API_KEY")
>>>>>>> 63648b42d9795ec062193e48be30c6b4c1f74ef2

def main():
    if not os.path.exists(CHROMA_DIR):
        print(f"Chroma directory not found: {CHROMA_DIR}")
        return

    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        return

    query = input("Enter your question: ").strip()
    if not query:
        print("No query entered.")
        return

    try:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        context = "\n\n".join(results["documents"][0])
        prompt = f"Based on the following SOP chunks, answer the question: {query}\n\nSOP chunks:\n{context}"

       
        print("\n--- LLM Prompt ---")
        print(prompt)

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")

if __name__ == "__main__":
    main()
