# ai_core.py
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from collections import Counter
import spacy
import os

# --- NLTK Data Download (if not already present) ---
# These checks prevent re-downloading if already done
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')

# --- spaCy Model Loading ---
# This model will be loaded once when the Flask app starts.
# We'll use a robust check for it.
try:
    nlp_model = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Attempting to download...")
    try:
        # Use spacy's CLI download directly
        spacy.cli.download("en_core_web_sm")
        nlp_model = spacy.load("en_core_web_sm")
        print("SpaCy model 'en_core_web_sm' downloaded and loaded successfully.")
    except Exception as e:
        print(f"Failed to download spaCy model: {e}. Please ensure you have internet and sufficient disk space.")
        print("You can try downloading manually by running 'python -m spacy download en_core_web_sm' in your terminal.")
        nlp_model = None # Set to None if download fails


# --- Initialize Hugging Face Pipelines (Global for Flask to load once) ---
print("Loading AI models... This may take a moment.")
# Summarization Pipeline
# For a faster but potentially less nuanced summary, distilbart is good.
# For better quality, consider 'facebook/bart-large-cnn' (larger download)
try:
    summarizer_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("Summarization model loaded.")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer_pipeline = None

# Question Generation Model
# This model is specifically fine-tuned for QG
try:
    qg_tokenizer = AutoTokenizer.from_pretrained("t5-small")
    qg_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    print("Question Generation model loaded.")
except Exception as e:
    print(f"Error loading Question Generation model: {e}")
    qg_tokenizer = None
    qg_model = None

# --- Functions ---

def generate_summary(text: str, max_length: int = 150, min_length: int = 30) -> str:
    """Generates a summary of the input text."""
    if not text.strip():
        return "Please provide text to summarize."
    if summarizer_pipeline is None:
        return "Summarization model not loaded. Please check logs for errors."
    try:
        summary = summarizer_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error generating summary: {e}"

def generate_questions(text: str, num_questions: int = 3) -> list:
    """Generates multiple-choice or open-ended questions from the text."""
    if not text.strip():
        return ["Please provide text to generate questions."]
    if qg_tokenizer is None or qg_model is None:
        return ["Question Generation model not loaded. Please check logs for errors."]
    if nlp_model is None:
        return ["SpaCy model not loaded, cannot identify answers for questions."]
    
    questions = []
    sentences = sent_tokenize(text)
    
    for i, sentence in enumerate(sentences):
        if len(sentence.split()) < 10: # Skip very short sentences
            continue
        
        input_text = f"question generation: {sentence}"
        
        try:
            input_ids = qg_tokenizer.encode(input_text, return_tensors="pt")
            output_ids = qg_model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
            question = qg_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Error generating question for sentence '{sentence[:50]}...': {e}")
            question = "" # Skip if question generation fails

        doc = nlp_model(sentence) # Use the global nlp_model
        answer = ""
        # Try to find a good answer (e.g., a prominent noun phrase or entity)
        for chunk in doc.noun_chunks:
            answer = chunk.text
            break # Take the first significant noun chunk as a potential answer
        
        # Fallback for entities if no noun chunk is found quickly
        if not answer and doc.ents:
            answer = doc.ents[0].text
        
        if question and answer and question.lower() != "no question" and answer != "":
            questions.append({"question": question, "answer": answer})
        
        if len(questions) >= num_questions:
            break
            
    if not questions:
        return ["Could not generate specific questions from the text. Try different text."]
    
    return questions

def generate_flashcards(text: str, num_flashcards: int = 5) -> list:
    """Generates flashcards (term and definition) from the text."""
    if not text.strip():
        return ["Please provide text to generate flashcards."]
    if nlp_model is None:
        return ["SpaCy model not loaded, cannot identify terms for flashcards."]

    flashcards = []
    
    doc = nlp_model(text) # Use the global nlp_model
    
    potential_terms = []
    # Extract noun chunks and named entities as potential terms
    for chunk in doc.noun_chunks:
        potential_terms.append(chunk.text)
    for ent in doc.ents:
        potential_terms.append(ent.text)

    stop_words = set(stopwords.words('english'))
    filtered_terms = [
        term.lower() for term in potential_terms
        if term.lower() not in stop_words and len(term.split()) > 1 and len(term) > 3 # Filter short or common terms
    ]
    
    # Get the most common unique terms
    term_counts = Counter(filtered_terms)
    # Prioritize terms that are longer and more likely to be concepts
    sorted_unique_terms = sorted(term_counts.keys(), key=lambda x: (term_counts[x], len(x)), reverse=True)
    
    sentences = sent_tokenize(text)
    
    for term_raw in sorted_unique_terms:
        # Find a sentence that defines or best describes the term
        definition = ""
        for sentence in sentences:
            if term_raw.lower() in sentence.lower():
                # Prefer sentences that seem like definitions
                if any(kw in sentence.lower() for kw in ["is a", "refers to", "means", "defined as"]):
                    definition = sentence.strip()
                    break
                elif len(definition) == 0: # Take the first one if no explicit definition found yet
                    definition = sentence.strip()
        
        if definition:
            flashcards.append({"term": term_raw.capitalize(), "definition": definition})
        
        if len(flashcards) >= num_flashcards:
            break

    if not flashcards:
        return ["Could not generate specific flashcards from the text. Try different text."]

    return flashcards