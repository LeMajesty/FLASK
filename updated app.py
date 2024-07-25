from flask import Flask, render_template, request, redirect, url_for, flash, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Predefined survey questions
questions = [
    "Do you like our product?",
    "Is our website easy to navigate?",
    "Would you recommend our service to others?",
    "Are you satisfied with our customer service?",
    "Do you find our prices reasonable?",
    "Is our product quality up to your expectations?",
    "Would you purchase from us again?",
    "Do you think our delivery time is satisfactory?"
]

# Shuffle questions to randomize
random.shuffle(questions)

@app.route('/')
def home():
    # Initialize session variables
    session['responses'] = []
    session['current_question'] = 0
    return redirect(url_for('question'))

@app.route('/question')
def question():
    current_question = session.get('current_question', 0)
    
    if current_question >= len(questions):
        return redirect(url_for('thank_you'))
    
    question_text = questions[current_question]
    return render_template('question.html', question=question_text, question_num=current_question)

@app.route('/answer', methods=['POST'])
def answer():
    selected_answer = request.form.get('answer')
    custom_answer = request.form.get('custom_answer', '')

    if not selected_answer:
        flash("You must select an answer!")
        return redirect(url_for('question'))

    # Append answer to session responses
    responses = session.get('responses', [])
    responses.append(custom_answer if selected_answer == 'custom' else selected_answer)
    session['responses'] = responses

    session['current_question'] += 1

    if session['current_question'] >= len(questions):
        return redirect(url_for('thank_you'))
    else:
        return redirect(url_for('question'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.errorhandler(404)
def page_not_found(e):
    flash("You're trying to access an invalid question.")
    return redirect(url_for('question'))

if __name__ == '__main__':
    app.run(debug=True)
