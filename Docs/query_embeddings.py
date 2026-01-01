import chromadb
import os
from rank_bm25 import BM25Okapi
from openai import OpenAI

CHROMA_DIR = "chroma_data"
COLLECTION_NAME = "risk_fraud_sops"
OPENAI_API_KEY = ("OPENAI_API_KEY")

from nltk.corpus import wordnet

def expand_query(query):
    expanded = set(query.split())
    for word in query.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name())
    return " ".join(expanded)

def create_bm25_index(chunks):
    tokenized_chunks = [chunk.split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_chunks)
    return bm25

def get_bm25_scores(bm25, query):
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    return scores

def main():
    if not os.path.exists(CHROMA_DIR):
        print(f"Chroma directory not found: {CHROMA_DIR}")
        return

query = input("Enter your question: ").strip()
query = expand_query(query)  # Add this line


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
      
        vector_results = collection.query(
            query_texts=[query],
            n_results=20,
            include=["documents", "metadatas", "distances"]
        )

       
        chunks = vector_results["documents"][0]
        bm25 = create_bm25_index(chunks)
        bm25_scores = get_bm25_scores(bm25, query)

       
        combined = list(zip(chunks, bm25_scores))
        combined.sort(key=lambda x: x[1], reverse=True)

       
        prompt = f"Score each chunk for relevance to the question: '{query}'.\n\nChunks:\n"
        for i, (chunk, score) in enumerate(combined):
            prompt += f"{i+1}. {chunk}\n\n"
        prompt += "Return the chunk numbers in order of relevance."

        
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        
        response_text = response.choices[0].message.content
        ordered_indices = [int(x.strip()) - 1 for x in response_text.split(",")]
        reranked_combined = [combined[i] for i in ordered_indices if i < len(combined)]

        
        print("\n--- Top 3 Reranked Chunks ---")
        for i, (chunk, score) in enumerate(reranked_combined[:3]):
            print(f"\n--- Result {i+1} (BM25 Score: {score:.3f}) ---")
            print(chunk)

    except Exception as e:
        print(f"Error querying ChromaDB: {e}")

if __name__ == "__main__":
    main()
