# app.py
import streamlit as st
from ai_core import generate_summary, generate_questions, generate_flashcards

# Set page config
st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("📚 AI Study Buddy")
st.write("Automatically generate summaries, questions, and flashcards from your study material.")

# Input text area
text = st.text_area("Paste your study material here:")

# Options sidebar
st.sidebar.header("Options")
num_summary_sentences = st.sidebar.slider("Summary length (sentences)", min_value=1, max_value=10, value=3)
num_questions = st.sidebar.slider("Number of questions", min_value=1, max_value=10, value=3)
num_flashcards = st.sidebar.slider("Number of flashcards", min_value=1, max_value=10, value=5)

# Buttons for actions
if st.button("Generate Summary"):
    if text.strip():
        try:
            result = generate_summary(text, num_sentences=num_summary_sentences)
            st.subheader("Summary")
            st.write(result.get("summary", "No summary available."))
        except Exception as e:
            st.error(f"Error generating summary: {e}")
    else:
        st.warning("Please enter some text to summarize.")

if st.button("Generate Questions"):
    if text.strip():
        try:
            questions = generate_questions(text, num_questions=num_questions)
            if questions:
                st.subheader("Questions")
                for idx, q in enumerate(questions, 1):
                    st.write(f"**Q{idx}:** {q['question']}")
                    st.write(f"**A{idx}:** {q['answer']}")
            else:
                st.info("No questions could be generated from this text.")
        except Exception as e:
            st.error(f"Error generating questions: {e}")
    else:
        st.warning("Please enter some text to generate questions.")

if st.button("Generate Flashcards"):
    if text.strip():
        try:
            flashcards = generate_flashcards(text, num_flashcards=num_flashcards)
            if flashcards:
                st.subheader("Flashcards")
                for idx, f in enumerate(flashcards, 1):
                    st.write(f"**Q{idx}:** {f['question']}")
                    st.write(f"**A{idx}:** {f['answer']}")
            else:
                st.info("No flashcards could be generated from this text.")
        except Exception as e:
            st.error(f"Error generating flashcards: {e}")
    else:
        st.warning("Please enter some text to generate flashcards.")
