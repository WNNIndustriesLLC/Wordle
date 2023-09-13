from flask import Flask, render_template, request, session
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # replace 'your_secret_key' with your own secret key

WORDS = {
    3: ['cat', 'dog', 'car', 'run', 'sun', 'hot', 'fun', 'rat', 'bat', 'man'],
    4: ['blue', 'mild', 'wild', 'jazz', 'buzz', 'word', 'bold', 'cold', 'warm', 'zone'],
    5: ['apple', 'brave', 'chair', 'brush', 'clock', 'stand', 'sweet', 'check', 'ghost', 'table'],
    6: ['beauty', 'belief', 'castle', 'charge', 'dollar', 'effort', 'finish', 'forest', 'coffee', 'market']
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    word_length = int(request.form['length'])
    secret_word = choice(WORDS[word_length])
    session['secret_word'] = secret_word
    session['guesses'] = ['_' for _ in secret_word]
    session['attempts'] = 0
    return render_template('index.html')


@app.route('/check_word', methods=['POST'])
def check_word():
    guessed_word = request.form['word'].lower()
    secret_word = session['secret_word']
    guesses = session['guesses']
    attempts = session['attempts']
    response = ''

    if attempts < 5:
        if guessed_word == secret_word:
            response = 'Congratulations! You guessed the word correctly!'
            guesses = list(secret_word)
        else:
            for i, letter in enumerate(secret_word):
                if letter == guessed_word[i]:
                    guesses[i] = letter
            response = 'Sorry, your guess is incorrect.'
            attempts += 1
        session['guesses'] = guesses
        session['attempts'] = attempts
    else:
        response = f'Game Over. The correct word was {secret_word}.'

    return render_template('index.html', response=response, guesses=guesses, attempts=attempts)


if __name__ == '__main__':
    app.run(debug=True)
