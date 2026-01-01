import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re
import nltk
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from typing import Dict, List

class SuperchargedNoLLMRAGEvaluator:
    def __init__(self):
        print("Loading SUPERCHARGED models...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        nltk.download('punkt', quiet=True)
        self.stemmer = SnowballStemmer('english')
        print("Supercharged evaluator ready!")
    
    def super_faithfulness(self, text1: str, text2: str) -> float:
        def stem_words(text):
            words = nltk.word_tokenize(text.lower())
            return [self.stemmer.stem(w) for w in words if len(w) > 2]
        
        stemmed1 = ' '.join(stem_words(text1))
        stemmed2 = ' '.join(stem_words(text2))
        
        vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        tfidf_matrix = vectorizer.fit_transform([stemmed1, stemmed2])
        tfidf_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        phrases1 = set(re.findall(r'\b\w+\s+\w+\b', text1.lower()))
        phrases2 = set(re.findall(r'\b\w+\s+\w+\b', text2.lower()))
        phrase_boost = len(phrases1 & phrases2) / max(len(phrases1), len(phrases2), 1)
        
        return min(1.0, 0.7 * tfidf_sim + 0.3 * phrase_boost)
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.model.encode([text1])
        emb2 = self.model.encode([text2])
        return float(cosine_similarity(emb1, emb2)[0][0])
    
    def context_coverage(self, answer: str, contexts: List[str]) -> float:
        answer_emb = self.model.encode([answer])
        context_embs = self.model.encode(contexts)
        similarities = [cosine_similarity(answer_emb, [c])[0][0] for c in context_embs]
        return float(np.mean(similarities))
    
    def evaluate(self, data: Dict) -> Dict:
        questions = data['question']
        answers = data['answer']
        contexts = data['contexts']
        ground_truths = data['ground_truth']
        
        print(f"SUPERCHARGED Evaluation: {len(questions)} questions...")
        start_time = time.time()
        
        faithfulness_scores = [self.super_faithfulness(a, gt) for a, gt in zip(answers, ground_truths)]
        relevancy_scores = [self.semantic_similarity(a, gt) for a, gt in zip(answers, ground_truths)]
        coverage_scores = [self.context_coverage(a, ctx) for a, ctx in zip(answers, contexts)]
        
        results = {
            'super_faithfulness': np.mean(faithfulness_scores),
            'semantic_relevancy': np.mean(relevancy_scores),
            'context_coverage': np.mean(coverage_scores),
            'detailed_results': pd.DataFrame({
                'question': questions,
                'faithfulness': faithfulness_scores,
                'relevancy': relevancy_scores,
                'coverage': coverage_scores
            })
        }
        
        elapsed = time.time() - start_time
        print(f"Supercharged complete in {elapsed:.1f}s!")
        return results


data = {
    "question": [
        "What are the steps for fraud detection?",
        "What documents are required for merchant onboarding?",
        "How are sanctions lists checked?",
        "What is the daily transaction limit for low-risk merchants?",
        "Who approves high-risk merchant applications?",
        "What triggers manual transaction review?",
        "What is KYC in merchant onboarding?",
        "What are PEP lists?",
        "How often are velocity checks performed?",
        "What happens when chargeback ratio exceeds 1%?",
        "What is AML reporting requirement?",
        "How are unusual transaction patterns detected?",
        "What documents prove beneficial ownership?",
        "What is the compliance officer's role?",
        "How are document frauds detected?"
    ],
    "answer": [
        "Steps include monitoring transaction velocity, checking unusual activity, validating documents, cross-checking sanctions lists.",
        "Required documents: KYC, proof of funds, beneficial ownership declaration, compliance officer approval.",
        "Sanctions lists checked using OFAC and FATF databases.",
        "Low-risk merchants: $50,000/day, maximum 1000 transactions/day.",
        "High-risk applications require compliance officer approval.",
        "Manual review triggered by automated AI alerts on suspicious patterns.",
        "KYC is identity verification with government ID and address proof.",
        "PEP lists are Politically Exposed Persons requiring enhanced scrutiny.",
        "Velocity checks performed daily across all risk levels.",
        "Chargeback ratio >1% triggers immediate account freeze and investigation.",
        "AML suspicious activity reports filed within 24 hours to RBI.",
        "Unusual patterns detected via AI models and data visualization dashboards.",
        "Beneficial ownership proven by shareholder registry and declaration forms.",
        "Compliance officer reviews high-risk cases and approves/rejects.",
        "Document frauds detected via authenticity scans and manual validation."
    ],
    "contexts": [
        ["## Verification Process: 1.Receive docs 2.Check completeness 3.Validate authenticity 4.Sanctions check 5.Risk assessment 6.Decision"],
        ["## Merchant Onboarding: KYC docs, proof of funds, ownership declaration, compliance approval"],
        ["## Sanctions Lists: Checked using OFAC and FATF databases"],
        ["## Daily Velocity Limits | Low-risk: $50,000 | 1000 txns/day"],
        ["## High-risk approval: Compliance officer mandatory review"],
        ["## Automated Alerts: AI flags → Manual review queue"],
        ["## KYC Process: ID verification + address proof"],
        ["## PEP Lists: Enhanced due diligence required"],
        ["## Velocity Monitoring: Daily checks all risk levels"],
        ["## Chargeback Policy: >1% = freeze + investigate"],
        ["## AML Reporting: Suspicious Activity Report to RBI in 24h"],
        ["## Pattern Detection: AI models + visualization dashboards"],
        ["## Beneficial Ownership: Shareholder registry + declaration"],
        ["## Compliance Officer: Reviews/approves high-risk merchants"],
        ["## Document Fraud: Authenticity scans + manual checks"]
    ],
    "ground_truth": [
        "Steps: monitor velocity, validate docs, sanctions check.",
        "Docs: KYC, proof of funds, ownership declaration, compliance approval.",
        "Sanctions: OFAC, FATF databases.",
        "Low-risk: $50k/day, 1000 txns.",
        "High-risk: compliance officer approval.",
        "Triggers: AI automated alerts.",
        "KYC: ID + address verification.",
        "PEP: politically exposed persons.",
        "Velocity: daily checks.",
        "Chargeback >1%: freeze account.",
        "AML: SAR to RBI within 24h.",
        "Patterns: AI models + dashboards.",
        "Ownership: shareholder registry + declaration.",
        "Compliance officer: high-risk review.",
        "Doc fraud: authenticity scans."
    ]
}

if __name__ == "__main__":
    evaluator = SuperchargedNoLLMRAGEvaluator()
    results = evaluator.evaluate(data)
    
    print("\n" + "="*60)
    print("SUPERCHARGED RESULTS (Faithfulness FIXED!)")
    print("="*60)
    for metric, score in results.items():
        if isinstance(score, (int, float)):
            print(f"{metric:20}: {score:.3f} ⭐")
    
    print("\n Per-Question Breakdown:")
    print(results['detailed_results'].round(3))

    






