from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from transformers import pipeline

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def input_screen():
    if request.method == 'POST':
        question = request.form['question']
        urls = request.form['urls'].split('\n')
        # Process the question and URLs here
        return redirect(url_for('output_screen'))
    return render_template('input.html')

@app.route('/output')
def output_screen():
    # Retrieve the extracted facts and render the output screen
    return render_template('output.html', facts=facts)

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.get_json()
    question = data['question']
    documents = data['documents']
    # Process the question and documents here
    return jsonify({'message': 'Question and documents submitted successfully'})

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    # Retrieve the question, extracted facts, and status
    response = {
        'question': question,
        'facts': facts,
        'status': status
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
