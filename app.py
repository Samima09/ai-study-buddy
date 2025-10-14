# app.py
from flask import Flask, render_template, request, jsonify
import nltk
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

from ai_core import generate_summary, generate_questions, generate_flashcards
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Load the secret key from the environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    """Renders the main page of the application."""
    return render_template('index.html')

def calculate_score(sentence, phrase):
    """
    Calculates a score for how 'definitional' a sentence is for a given phrase.
    A lower score is better.
    """
    lower_sentence = sentence.lower()
    lower_phrase = phrase.lower()
    
    # Base score is the position of the phrase. Lower is better.
    score = lower_sentence.find(lower_phrase)

    # Big penalty for sentences starting with action verbs (e.g., "Orbiting").
    first_word = sentence.split(' ')[0]
    if first_word.endswith('ing'):
        score += 100
        
    # Bonus for sentences that look like a definition (e.g., "The Sun is...").
    if f"{lower_phrase} is" in lower_sentence or f"{lower_phrase} are" in lower_sentence:
        score -= 20
    
    # Bigger bonus if the sentence starts with the key phrase.
    if lower_sentence.startswith(lower_phrase):
        score -= 30

    return score

@app.route('/api/process', methods=['POST'])
def process_api():
    """API endpoint to process text."""
    try:
        data = request.get_json()
        text = data.get('text')
        action = data.get('action')
        options = data.get('options', {})

        if not text or not action:
            return jsonify({"error": "Missing 'text' or 'action' in request"}), 400

        if action == 'generate_questions':
            num_questions = int(options.get('num_questions', 3))
            raw_results = generate_questions(text, num_questions=num_questions)
            
            sentences = nltk.sent_tokenize(text)
            
            if not raw_results:
                return jsonify({'questions': []})

            key_phrases = [item.get('answer', '') for item in raw_results if item.get('answer')]
            
            # --- Definitive Multi-Pass Assignment Logic for Best Unique Answers ---
            final_assignments = {}
            used_sentences = set()

            # 1. First Pass: For each phrase, find its single best sentence candidate.
            phrase_candidates = {}
            for phrase in key_phrases:
                potential_answers = [s for s in sentences if phrase.lower() in s.lower()]
                if potential_answers:
                    best_sentence = min(potential_answers, key=lambda s: calculate_score(s, phrase))
                    phrase_candidates[phrase] = best_sentence

            # 2. Conflict Resolution: Group phrases by their preferred sentence.
            sentence_to_phrases = {}
            for phrase, sentence in phrase_candidates.items():
                if sentence not in sentence_to_phrases:
                    sentence_to_phrases[sentence] = []
                sentence_to_phrases[sentence].append(phrase)

            # Assign sentences to the phrase that has the best score for it.
            for sentence, conflicting_phrases in sentence_to_phrases.items():
                if sentence in used_sentences: continue
                
                winner_phrase = min(conflicting_phrases, key=lambda p: calculate_score(sentence, p))
                final_assignments[winner_phrase] = sentence
                used_sentences.add(sentence)

            # 3. Second Pass: Find answers for any phrases that lost a conflict.
            unassigned_phrases = [p for p in key_phrases if p not in final_assignments]
            for phrase in unassigned_phrases:
                available_sentences = [s for s in sentences if s not in used_sentences]
                potential_answers = [s for s in available_sentences if phrase.lower() in s.lower()]
                if potential_answers:
                    best_answer = min(potential_answers, key=lambda s: calculate_score(s, phrase))
                    final_assignments[phrase] = best_answer
                    used_sentences.add(best_answer)

            # 4. Final Assembly: Build the results in the original order.
            processed_results = []
            for item in raw_results:
                key_phrase = item.get('answer', '')
                if not key_phrase: continue
                
                question = f"What is '{key_phrase}'?"
                answer = final_assignments.get(key_phrase, key_phrase) # Fallback to phrase itself
                processed_results.append({'question': question, 'answer': answer})
            
            return jsonify({'questions': processed_results})
        
        elif action == 'summarize':
            min_len = int(options.get('summary_min_len', 30))
            max_len = int(options.get('summary_max_len', 150))
            summary_result = generate_summary(text, min_length=min_len, max_length=max_len)
            
            summary_text = ""
            
            # Case 1: The result is a list (most common from Hugging Face pipelines)
            if isinstance(summary_result, list) and summary_result:
                first_item = summary_result[0]
                if isinstance(first_item, dict):
                    # Find the first string value in the dictionary, regardless of the key
                    for value in first_item.values():
                        if isinstance(value, str):
                            summary_text = value
                            break 
            
            # Case 2: The result is a dictionary itself
            elif isinstance(summary_result, dict):
                for value in summary_result.values():
                    if isinstance(value, str):
                        summary_text = value
                        break
            
            # Case 3: The result is just a plain string
            elif isinstance(summary_result, str):
                summary_text = summary_result

            if summary_text:
                return jsonify({'summary': summary_text})

            # If we still haven't found the text, log the format and return the error
            logging.error(f"Unexpected summary result format: {summary_result}")
            return jsonify({'error': 'Could not generate a summary due to an unexpected format.'}), 500
        
        elif action == 'generate_flashcards':
            num_flashcards = int(options.get('num_flashcards', 5))
            flashcards = generate_flashcards(text, num_flashcards=num_flashcards)
            return jsonify({'flashcards': flashcards})

        else:
            return jsonify({"error": "Invalid action specified"}), 400

    except Exception as e:
        logging.error(f"An error occurred during API processing: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=False)
























