import random
import nltk
from transformers import pipeline

# Ensure NLTK tokenizer is ready
nltk.download('punkt')

# 1️⃣ Summarization function (lightweight for Streamlit Cloud)
def generate_summary(text, min_length=30, max_length=150):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")  # small and fast
    summary = summarizer(text, min_length=min_length, max_length=max_length)
    return summary[0].get('summary_text', '') if summary else "No summary generated."

# 2️⃣ Question generation function
def generate_questions(text, num_questions=3):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    answers = random.sample(sentences, min(num_questions, len(sentences)))
    questions = [{'answer': ans} for ans in answers]
    return questions

# 3️⃣ Flashcards function
def generate_flashcards(text, num_flashcards=5):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    selected = random.sample(sentences, min(num_flashcards, len(sentences)))
    flashcards = [
        {'question': f"What is this about?\n{sent[:50]}...", 'answer': sent}
        for sent in selected
    ]
    return flashcards
