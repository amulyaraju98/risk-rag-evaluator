FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir pandas nltk scikit-learn sentence-transformers
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY evaluate_rag.py .

CMD ["python", "-u", "evaluate_rag.py"]
