# app.py
import streamlit as st
from ai_core import generate_summary, generate_questions, generate_flashcards

st.set_page_config(page_title="AI Study Buddy", layout="wide")
st.title("AI Study Buddy 📚")

# Sidebar options
st.sidebar.header("Options")
action = st.sidebar.radio(
    "Choose an action",
    ("Summarize", "Generate Questions", "Generate Flashcards")
)

text = st.text_area("Paste your study material here:", height=250)

# Optionally adjust parameters
if action == "Summarize":
    num_sentences = st.sidebar.slider("Number of sentences in summary:", 1, 10, 3)
elif action in ["Generate Questions", "Generate Flashcards"]:
    num_items = st.sidebar.slider(
        f"Number of {'questions' if action=='Generate Questions' else 'flashcards'}:", 1, 10, 3
    )

# Process input when button clicked
if st.button("Process"):
    if not text.strip():
        st.warning("Please enter some text to process.")
    else:
        if action == "Summarize":
            result = generate_summary(text, num_sentences=num_sentences)
            st.subheader("Summary")
            st.write(result.get("summary", "No summary generated."))
        
        elif action == "Generate Questions":
            questions = generate_questions(text, num_questions=num_items)
            st.subheader("Generated Questions")
            if questions:
                for idx, q in enumerate(questions, start=1):
                    st.markdown(f"**Q{idx}:** {q['question']}")
                    st.markdown(f"**A{idx}:** {q['answer']}")
            else:
                st.write("No questions could be generated.")

        elif action == "Generate Flashcards":
            flashcards = generate_flashcards(text, num_flashcards=num_items)
            st.subheader("Flashcards")
            if flashcards:
                for idx, f in enumerate(flashcards, start=1):
                    st.markdown(f"**Card {idx} Question:** {f['question']}")
                    st.markdown(f"**Card {idx} Answer:** {f['answer']}")
            else:
                st.write("No flashcards could be generated.")
