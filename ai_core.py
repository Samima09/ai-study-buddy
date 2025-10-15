import nltk
import random
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Ensure punkt is downloaded (works on Streamlit Cloud)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# --- Summarization using TextRank ---
def generate_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join(str(sentence) for sentence in summary)

# --- Question Generation ---
def generate_questions(text, num_questions=3):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    answers = random.sample(sentences, min(num_questions, len(sentences)))
    questions = [{'answer': ans} for ans in answers]
    return questions

# --- Flashcards ---
def generate_flashcards(text, num_flashcards=5):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    selected = random.sample(sentences, min(num_flashcards, len(sentences)))
    flashcards = [{'question': f"What is this about?\n{sent[:50]}...", 'answer': sent} for sent in selected]
    return flashcards
