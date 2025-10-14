An intelligent web application built with Flask and Python that automatically generates summaries, questions, and flashcards from any study material. This tool is designed to accelerate learning and make revision more efficient.

✨ Features
Automatic Summarization: Paste any text and get a concise, AI-generated summary.

Question Generation: Automatically create relevant questions and answers from your notes to test your knowledge.

Flashcard Creation: Generate key terms and definitions as flashcards for quick revision.

Customizable Options: Easily adjust the number of questions, flashcards, and the length of the summary.

Secure API: All AI processing is handled through a secure backend API.

🛠️ Tech Stack
Backend: Python, Flask

AI / NLP: Hugging Face Transformers, NLTK

Frontend: HTML, CSS, JavaScript

API Testing: Postman

Environment Management: python-dotenv

🚀 Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the Repository
git clone [https://github.com/Samima09/ai-study-buddy.git](https://github.com/Samima09/ai-study-buddy.git)
cd ai-study-buddy

2. Create and Activate a Virtual Environment
It's recommended to use a virtual environment to manage project dependencies.

On Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

pip install -r requirements.txt

(Note: You will need to create a requirements.txt file first. See the note below.)

4. Set Up Environment Variables
Create a file named .env in the root of your project folder and add your secret key.

SECRET_KEY="your-own-secret-key-here"

5. Download NLTK Data
The application requires the punkt package from NLTK. Run the following command in a Python shell:

python -c "import nltk; nltk.download('punkt')"

6. Run the Application
Start the Flask server with the following command:

python app.py

The application will be running at http://127.0.0.1:5000.

※ Creating the requirements.txt file
If you don't have this file yet, you can create it easily. In your terminal (with your virtual environment active), run this command. It will automatically save a list of all the libraries you used into a new file.

pip freeze > requirements.txt

Usage
Open your web browser and navigate to http://127.0.0.1:5000.

Paste your study material into the main text box.

Use the sliders on the right to adjust the options as needed.

Click "Summarize", "Generate Questions", or "Generate Flashcards" to process the text.

The results will appear in the "Results" section at the bottom.