# app.py
import streamlit as st
from ai_core import generate_summary, generate_questions, generate_flashcards

st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("AI Study Buddy")
st.write("Paste your text and choose an action to generate a summary, questions, or flashcards.")

text = st.text_area("Enter your text here:", height=200)
action = st.selectbox("Choose an action:", ["Summarize", "Generate Questions", "Generate Flashcards"])

if st.button("Run"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        if action == "Summarize":
            result = generate_summary(text)
            st.subheader("Summary")
            st.write(result)
        elif action == "Generate Questions":
            questions = generate_questions(text)
            st.subheader("Questions")
            for idx, q in enumerate(questions, 1):
                st.write(f"Q{idx}: {q['question']}")
                st.write(f"A{idx}: {q['answer']}")
        elif action == "Generate Flashcards":
            flashcards = generate_flashcards(text)
            st.subheader("Flashcards")
            for idx, f in enumerate(flashcards, 1):
                st.write(f"Flashcard {idx}:")
                st.write(f"Q: {f['question']}")
                st.write(f"A: {f['answer']}")
