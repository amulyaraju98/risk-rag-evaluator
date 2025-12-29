FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir ragas==0.1.11 pandas nltk transformers sentence-transformers
COPY evaluate_rag.py .
RUN python -c "import nltk; nltk.download('punkt_tab')"
CMD ["python", "evaluate_rag.py"]
