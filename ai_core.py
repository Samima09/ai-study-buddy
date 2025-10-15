# ai_core.py
import random
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Download NLTK punkt tokenizer once
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


# ---------------------------
# 1️⃣ Summarization function
# ---------------------------
def generate_summary(text, num_sentences=3):
    """
    Generates a summary of the input text using TextRank (Sumy library).
    Returns a dictionary with 'summary' key.
    """
    if not text.strip():
        return {"summary": "No text provided."}
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    summary_text = " ".join([str(sentence) for sentence in summary_sentences])
    return {"summary": summary_text if summary_text else "No summary available."}


# ---------------------------
# 2️⃣ Question generation function
# ---------------------------
def generate_questions(text, num_questions=3):
    """
    Generates questions by randomly picking sentences from the text.
    Returns a list of dictionaries with 'question' and 'answer'.
    """
    if not text.strip():
        return []
    
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []

    selected_answers = random.sample(sentences, min(num_questions, len(sentences)))
    questions = [
        {
            "question": f"What is this about?\n{answer[:50]}...",  # first 50 chars for preview
            "answer": answer
        }
        for answer in selected_answers
    ]
    return questions


# ---------------------------
# 3️⃣ Flashcards function
# ---------------------------
def generate_flashcards(text, num_flashcards=5):
    """
    Generates flashcards by randomly picking sentences.
    Returns a list of dictionaries with 'question' and 'answer'.
    """
    if not text.strip():
        return []

    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []

    selected_sentences = random.sample(sentences, min(num_flashcards, len(sentences)))
    flashcards = [
        {
            "question": f"Define / explain:\n{sentence[:50]}...",  # first 50 chars
            "answer": sentence
        }
        for sentence in selected_sentences
    ]
    return flashcards
