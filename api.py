# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from ai_core import generate_summary, generate_questions, generate_flashcards
import nltk

nltk.download("punkt")

app = FastAPI(title="AI Study Buddy API")

class TextRequest(BaseModel):
    text: str
    action: str
    options: dict = {}

def process_text(text, action, options={}):
    sentences = nltk.sent_tokenize(text)

    if action == "Generate Questions":
        raw_results = generate_questions(text, num_questions=options.get("num_questions", 3))
        results = []
        for item in raw_results:
            answer = item.get("answer", "")
            match = next((s for s in sentences if answer.lower() in s.lower()), answer)
            results.append({"question": f"What is '{answer}'?", "answer": match})
        return results

    elif action == "Summarize":
        min_len = options.get("summary_min_len", 30)
        max_len = options.get("summary_max_len", 150)
        return generate_summary(text, min_length=min_len, max_length=max_len)

    elif action == "Generate Flashcards":
        num_flashcards = options.get("num_flashcards", 5)
        return generate_flashcards(text, num_flashcards=num_flashcards)

    return None

@app.post("/process")
def process(request: TextRequest):
    return {"result": process_text(request.text, request.action, request.options)}
