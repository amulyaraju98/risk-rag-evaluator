FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir sentence-transformers nltk scikit-learn pandas numpy datasets flask

COPY evaluate_rag.py .
RUN python -c "import nltk; nltk.download('punkt_tab')"

# Web wrapper: Run eval + serve HTML results
COPY app.py .
CMD ["python", "app.py"]
