from flask import Flask
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Run your evaluator
        result = subprocess.run([sys.executable, 'evaluate_rag.py'], 
                              capture_output=True, text=True, timeout=60)
        output = result.stdout if result.returncode == 0 else result.stderr
        return f"<pre>{output}</pre><hr><h3>🚀 Fraud RAG Evaluator Live!</h3>"
    except:
        return "<h1>Evaluating fraud RAG metrics...</h1><pre>Loading models (30s)...</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
