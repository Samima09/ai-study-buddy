import random
import nltk
from transformers import pipeline
import os

# Download NLTK punkt tokenizer
nltk.download('punkt')

# Load Hugging Face API token from environment
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize summarization pipeline using Hugging Face API
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    use_auth_token=HF_TOKEN,
    device=-1  # CPU
)

def generate_summary(text, min_length=30, max_length=150):
    summary = summarizer(text, min_length=min_length, max_length=max_length)
    return summary[0].get('summary_text', '')

def generate_questions(text, num_questions=3):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    answers = random.sample(sentences, min(num_questions, len(sentences)))
    questions = [{'answer': ans} for ans in answers]
    return questions

def generate_flashcards(text, num_flashcards=5):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    selected = random.sample(sentences, min(num_flashcards, len(sentences)))
    flashcards = [{'question': f"What is this about?\n{sent[:50]}...", 'answer': sent} for sent in selected]
    return flashcards
