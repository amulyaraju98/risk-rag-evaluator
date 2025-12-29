FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir sentence-transformers nltk scikit-learn pandas numpy datasets
RUN python -c "import nltk; nltk.download('punkt_tab')"
COPY evaluate_rag.py .
CMD ["python", "evaluate_rag.py"]
