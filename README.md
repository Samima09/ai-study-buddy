AI Study Buddy
AI Study Buddy is a Streamlit web app that generates summaries, questions, and flashcards from any study material to speed up learning and revision.

Features
AI-powered Summarization
Question Generation with answers
Flashcard Creation
Customizable options (number of questions/flashcards, summary length)
Secure backend processing

Tech Stack
Python, Streamlit
Hugging Face Transformers, NLTK
python-dotenv

Setup
git clone https://github.com/Samima09/ai-study-buddy.git
cd ai-study-buddy
python -m venv venv
# Activate environment
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt


Create a .env file:
SECRET_KEY="AIzSyD4xvB7Pq9kLmN0aR2sT3uVwXyZ"


Download NLTK tokenizer:
python -c "import nltk; nltk.download('punkt')"


Run the app:
streamlit run app.py

Deployment
https://ai-study-buddy-dcplyxeoput8uqqt4nz8br.streamlit.app/