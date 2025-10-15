# ai_core.py
import random
import nltk
from transformers import pipeline

# Download NLTK punkt tokenizer once
nltk.download('punkt')

# Summarization function
def generate_summary(text, min_length=30, max_length=150):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, min_length=min_length, max_length=max_length)
    return summary[0]['summary_text']  # Return the string directly

# Question generator
def generate_questions(text, num_questions=3):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    answers = random.sample(sentences, min(num_questions, len(sentences)))
    questions = [{'question': f"What is this about?\n{ans[:50]}...", 'answer': ans} for ans in answers]
    return questions

# Flashcards
def generate_flashcards(text, num_flashcards=5):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    selected = random.sample(sentences, min(num_flashcards, len(sentences)))
    flashcards = [{'question': f"What is this about?\n{sent[:50]}...", 'answer': sent} for sent in selected]
    return flashcards
