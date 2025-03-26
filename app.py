from flask import Flask, render_template, request, jsonify
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from dotenv import load_dotenv

import psycopg2
import random
import os

load_dotenv()

app = Flask(__name__)

START_DATE = date(2025, 3, 2)


def get_current_word():
    """Retrieve the single word from `word_today` using psycopg."""
    conn = psycopg2.connect(  # ✅ Creates a new connection
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM word_today LIMIT 1;")
    word_entry = cursor.fetchone()

    cursor.close()
    conn.close()  # ✅ Closes only this request's connection

    return word_entry[0] if word_entry else "ERROR WORD"


def update_daily_word():
    """Replace the current word with a new one from `word_bank`."""

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM word_bank ORDER BY RANDOM() LIMIT 1;")
    new_word_entry = cursor.fetchone()

    if new_word_entry:
        new_word = new_word_entry[0]
        print(f"🔄 Updating daily word to: {new_word}")

        cursor.execute("DELETE FROM word_today;")
        cursor.execute("INSERT INTO word_today (word) VALUES (%s);", (new_word,))

        conn.commit()

    cursor.close()
    conn.close()  # ✅ Only closes this function's connection





def get_game_number():
    """Calculate the game number based on the days elapsed since START_DATE."""
    today = date.today()
    print(today, START_DATE)
    delta = (today - START_DATE).days
    return delta + 1  # Game #1 starts today

def convert_word_to_number(word):
    """Convert a 10-letter word or phrase into a number sequence based on the phone keypad."""
    keypad = {
        'a': '2', 'b': '2', 'c': '2',
        'd': '3', 'e': '3', 'f': '3',
        'g': '4', 'h': '4', 'i': '4',
        'j': '5', 'k': '5', 'l': '5',
        'm': '6', 'n': '6', 'o': '6',
        'p': '7', 'q': '7', 'r': '7', 's': '7',
        't': '8', 'u': '8', 'v': '8',
        'w': '9', 'x': '9', 'y': '9', 'z': '9',
        ' ': '0'  # Spaces are represented as 0
    }
    return ''.join(keypad[char] if char in keypad else '-' for char in word.lower())

scheduler = BackgroundScheduler()
scheduler.add_job(update_daily_word, 'cron', hour=0, minute=0)
scheduler.start()

@app.route('/')
def index():
    """Render the main game page with the game number and date."""
    word = get_current_word()
    number_code = convert_word_to_number(word) if word else "0000000000"

    # ✅ Get dynamic game number and formatted date
    game_number = get_game_number()
    current_date = date.today().strftime("%B %d, %Y")  # Example: February 27, 2025

    return render_template(
        'index.html',
        number_code=number_code,
        word=word,
        game_number=game_number,
        current_date=current_date
    )

@app.route('/guess', methods=['POST'])
def check_guess():
    """Check the user's guess against the correct word and track progress."""
    data = request.get_json()
    user_guess = data.get('guess', '').upper()
    correct_word = data.get('correct_word', '').upper()
    remaining_attempts = int(data.get('remaining_attempts', 3))
    guess_progress = data.get('guess_progress', [])
    
    correct = [user_guess[i] if user_guess[i] == correct_word[i] else "_" for i in range(10)]
    guess_progress.append(correct)
    
    if user_guess == correct_word:
        return jsonify({'result': 'correct', 'correct_word': correct_word, 'guess_progress': guess_progress})
    else:
        remaining_attempts -= 1
        if remaining_attempts == 0:
            return jsonify({'result': 'game_over', 'correct_word': correct_word, 'guess_progress': guess_progress})
        return jsonify({'result': 'incorrect', 'remaining_attempts': remaining_attempts, 'guess_progress': guess_progress})

if __name__ == '__main__':
    app.run(debug=True)