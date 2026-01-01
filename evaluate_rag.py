import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from typing import Dict, List, Union

class RiskRAGEvaluator:
    def __init__(self):
        print("Initializing Risk RAG Evaluator (v2.0 - Interactive)...")
        # Load the model once
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        nltk.download('punkt', quiet=True)
        self.stemmer = SnowballStemmer('english')
        
        self.knowledge_base = []
        self.kb_embeddings = None

    def _preprocess(self, text: str) -> str:
        words = nltk.word_tokenize(text.lower())
        return ' '.join([self.stemmer.stem(w) for w in words if len(w) > 2])

    def calculate_faithfulness(self, answer: str, context: str) -> float:
        stemmed_ans = self._preprocess(answer)
        stemmed_ctx = self._preprocess(context)
        
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([stemmed_ans, stemmed_ctx])
            return float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        except:
            return 0.0

    def calculate_relevancy(self, answer: str, ground_truth: str) -> float:
        embs = self.model.encode([answer, ground_truth])
        return float(cosine_similarity([embs[0]], [embs[1]])[0][0])

    def calculate_coverage(self, query: str, context: str) -> float:
        embs = self.model.encode([query, context])
        return float(cosine_similarity([embs[0]], [embs[1]])[0][0])

    def load_knowledge_base(self, contexts: List[List[str]]):
        self.knowledge_base = list(set([item for sublist in contexts for item in sublist]))
        print(f"Loading {len(self.knowledge_base)} SOP chunks into Vector DB...")
        self.kb_embeddings = self.model.encode(self.knowledge_base)

    def ask_question(self, user_query: str) -> Dict:
        if self.kb_embeddings is None:
            return {"error": "Knowledge base not loaded."}

        # 1. RETRIEVAL 
        query_emb = self.model.encode([user_query])
        sims = cosine_similarity(query_emb, self.kb_embeddings)[0]
        best_idx = np.argmax(sims)
        retrieved_context = self.knowledge_base[best_idx]

        # 2. GENERATION 
        generated_answer = f"According to the policy: {retrieved_context}"

        # 3. EVALUATION 
        faith = self.calculate_faithfulness(generated_answer, retrieved_context)
        coverage = self.calculate_coverage(user_query, retrieved_context)
        
        return {
            "Question": user_query,
            "Answer": generated_answer,
            "Retrieved_SOP": retrieved_context,
            "Faithfulness": round(faith, 3),
            "Context_Coverage": round(coverage, 3)
        }

# DATA
data = {
    "question": [
        "What are the document requirements for a High Risk merchant?",
        "What are the daily transaction limits for a Medium Risk merchant?",
        "What triggers a Tier 3 Red response in transaction monitoring?",
        "How long must merchant records be kept according to guidelines?",
        "What is the required reporting deadline for a sanctions list match?",
        "What is considered a 'Velocity Spike' red flag?",
        "Who has the final authority to approve high-risk merchant applications?",
        "What action is taken if a merchant is from a FATF 'Critical' jurisdiction?",
        "How often are High Risk merchants re-screened?",
        "What are the specific rejection reasons for an application?",
        "What is the maximum transaction count per day for Low Risk?",
        "When is Enhanced Due Diligence (EDD) triggered?",
        "What constitutes a 'Geo Anomaly' in fraud detection?",
        "What lists are used for sanctions screening?",
        "Can a rejected merchant re-apply, and if so, when?"
    ],
    "answer": [
        "High Risk docs include Medium Risk files plus source-of-funds proof, beneficial ownership declaration, and compliance officer approval.",
        "Medium Risk limits are $100,000 max value per day and 2000 max transactions per day.",
        "Tier 3 is triggered by critical fraud; actions include immediate transaction holds and full investigation.",
        "All merchant records must be kept for 5 years per RBI guidelines.",
        "A sanctions match must be reported within 24 hours to FIU-IND or the relevant body.",
        "A Velocity Spike is flagged when activity is >150% of the 30-day average.",
        "The compliance officer must provide mandatory review and final approval for high-risk applications.",
        "Merchants from critical jurisdictions like Iran or North Korea are blocked and reported.",
        "High Risk merchants are re-screened on a monthly basis.",
        "Rejection reasons include fake docs, sanctions/PEP matches, high-risk jurisdictions, or opaque ownership.",
        "Low Risk merchants are limited to 1000 transactions per day.",
        "EDD is triggered by PEP findings, high-risk country association, or suspicious transaction patterns.",
        "A Geo Anomaly involves sudden logins or transactions from multiple countries.",
        "Screening uses OFAC (US), UN, EU, FATF, and RBI lists.",
        "Yes, they may re-apply within 30 days after fixing the identified deficiencies."
    ],
    "contexts": [
        ["## High Risk Docs: Medium Risk + Source-of-funds + Beneficial ownership declaration + Compliance approval"],
        ["## Daily Velocity Limits | Medium Risk: $100,000 | 2000 txns/day"],
        ["## Response Tier 3: Immediate hold + Executive review + Full investigation"],
        ["## Appeal & Retention: Records kept for 5 years per RBI guidelines"],
        ["## Sanctions Actions: Exact match = immediate freeze + Report within 24h to FIU-IND"],
        ["## Red Flag Indicators: Velocity Spike >150% of 30-day avg"],
        ["## High Risk – Enhanced Check: Requires Beneficial ownership declaration + Compliance officer approval"],
        ["## Jurisdiction Review: Critical (Iran, N. Korea) = Block + Report"],
        ["## Ongoing Monitoring: High Risk merchants re-screened Monthly"],
        ["## Rejection Reasons: Fake docs, Sanctions/PEP match, Opaque ownership, Failed background check"],
        ["## Daily Velocity Limits | Low Risk: $50,000 | 1000 txns/day"],
        ["## EDD Triggers: PEP found / High-Risk Country / Suspicious Transaction"],
        ["## Red Flag Indicators: Geo Anomaly (sudden multi-country logins or TXNs)"],
        ["## Sanctions List Checks: Lists used: OFAC (US), UN, EU, FATF, RBI"],
        ["## Appeal Procedure: Rejected merchants may re-apply within 30 days after fixing deficiencies"]
    ],
    "ground_truth": [
        "Docs: Medium Risk docs + source of funds + ownership declaration + compliance approval.",
        "Limits: $100,000 and 2000 transactions per day.",
        "Tier 3: Immediate transaction hold and full fraud investigation.",
        "Retention: 5 years per RBI guidelines.",
        "Deadline: Within 24 hours to FIU-IND.",
        "Spike: Activity exceeding 150% of the 30-day average.",
        "Authority: Compliance officer sign-off is mandatory.",
        "Action: Block the merchant and file a report.",
        "Frequency: Monthly re-screening for High Risk.",
        "Reasons: Fraudulent documents, sanctions matches, or hidden ownership.",
        "Count: 1000 max transactions per day.",
        "Triggers: PEP match, high-risk jurisdiction, or suspicious flags.",
        "Anomaly: Sudden multi-country logins or transaction activity.",
        "Lists: OFAC, UN, EU, FATF, and RBI.",
        "Re-apply: Yes, within 30 days after fixing issues."
    ]
}


if __name__ == "__main__":
    evaluator = RiskRAGEvaluator()
    evaluator.load_knowledge_base(data['contexts'])

    print("\n" + "="*50)
    print("APEXPAY RISK AUDITOR (Interactive Mode)")
    print("Type your question below or type 'exit' to quit.")
    print("="*50)

    while True:
        user_input = input("\n Query: ")
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Shutting down...")
            break
            
        res = evaluator.ask_question(user_input)
        
        print(f"\n AI Answer: {res['Answer']}")
        print(f"Source:    {res['Retrieved_SOP']}")
        print("-" * 30)
        print(f"Faithfulness Score:   {res['Faithfulness']}")
        print(f" Context Coverage:      {res['Context_Coverage']}")
        print("-" * 30)

