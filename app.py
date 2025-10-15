# app.py
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Now you can use SECRET_KEY anywhere in your app
st.write("Secret key loaded successfully!")  # just to test

import nltk

from ai_core import generate_summary, generate_questions, generate_flashcards

# Ensure NLTK punkt tokenizer is downloaded
nltk.download('punkt')

st.set_page_config(page_title="AI Study Buddy", layout="wide")

st.title("AI Study Buddy")
st.write("Enter your text and choose an action to generate questions, summary, or flashcards.")

# --- Input Section ---
text = st.text_area("Enter your text here:", height=200)

action = st.selectbox(
    "Choose an action:",
    ["Generate Questions", "Summarize", "Generate Flashcards"]
)

options = {}
if action == "Generate Questions":
    options['num_questions'] = st.number_input("Number of Questions:", min_value=1, max_value=20, value=3)
elif action == "Summarize":
    options['summary_min_len'] = st.number_input("Summary Minimum Length:", min_value=10, max_value=100, value=30)
    options['summary_max_len'] = st.number_input("Summary Maximum Length:", min_value=50, max_value=500, value=150)
elif action == "Generate Flashcards":
    options['num_flashcards'] = st.number_input("Number of Flashcards:", min_value=1, max_value=20, value=5)

# --- Internal API-like function ---
def process_text(text, action, options={}):
    if action == "Generate Questions":
        raw_results = generate_questions(text, num_questions=options.get('num_questions', 3))
        sentences = nltk.sent_tokenize(text)

        # Map phrases to sentences
        results = []
        for item in raw_results:
            answer = item.get('answer', '')
            if answer:
                # Find first matching sentence
                match = next((s for s in sentences if answer.lower() in s.lower()), answer)
                results.append({"question": f"What is '{answer}'?", "answer": match})
        return results

    elif action == "Summarize":
        min_len = options.get('summary_min_len', 30)
        max_len = options.get('summary_max_len', 150)
        summary_result = generate_summary(text, min_length=min_len, max_length=max_len)
        # Extract string if returned as list/dict
        if isinstance(summary_result, list) and summary_result:
            first_item = summary_result[0]
            if isinstance(first_item, dict):
                for value in first_item.values():
                    if isinstance(value, str):
                        return value
        elif isinstance(summary_result, dict):
            for value in summary_result.values():
                if isinstance(value, str):
                    return value
        elif isinstance(summary_result, str):
            return summary_result
        return "No summary available."

    elif action == "Generate Flashcards":
        num_flashcards = options.get('num_flashcards', 5)
        return generate_flashcards(text, num_flashcards=num_flashcards)

    return None

# --- Run button ---
if st.button("Run"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        result = process_text(text, action, options)
        st.subheader("Results:")
        if action == "Generate Questions":
            for idx, item in enumerate(result, 1):
                st.write(f"Q{idx}: {item['question']}")
                st.write(f"A{idx}: {item['answer']}")
        elif action == "Summarize":
            st.write(result)
        elif action == "Generate Flashcards":
            for idx, card in enumerate(result, 1):
                st.write(f"Flashcard {idx}:")
                st.write(f"Q: {card['question']}")
                st.write(f"A: {card['answer']}")
