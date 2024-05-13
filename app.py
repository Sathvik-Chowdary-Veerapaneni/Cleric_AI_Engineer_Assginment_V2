from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from transformers import pipeline

app = Flask(__name__)

# Load the pre-trained model
qa_pipeline = pipeline('question-answering')

@app.route('/', methods=['GET', 'POST'])
def input_screen():
    if request.method == 'POST':
        question = request.form['question']
        file_names = request.form['file_names'].split('\n')

        # Process the question and file names
        facts = extract_facts(question, file_names)

        # Store the question, facts, and status in a database or session
        store_facts(question, facts)

        return redirect(url_for('output_screen'))

    return render_template('input.html')

@app.route('/output')
def output_screen():
    # Retrieve the extracted facts from the database or session
    question, facts = retrieve_facts()
    return render_template('output.html', question=question, facts=facts)

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.get_json()
    question = data['question']
    file_names = data['documents']

    # Process the question and file names
    facts = extract_facts(question, file_names)

    # Store the question, facts, and status in a database or session
    store_facts(question, facts)

    return jsonify({'message': 'Question and documents submitted successfully'})

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    # Retrieve the question, extracted facts, and status from the database or session
    question, facts = retrieve_facts()

    response = {
        'question': question,
        'facts': facts,
        'status': 'done'
    }

    return jsonify(response)

def extract_facts(question, file_names):
    facts = []

    for file_name in file_names:
        # Read the call log file from the local directory
        file_path = os.path.join('logs_input', file_name.strip())
        with open(file_path, 'r') as file:
            call_log_text = file.read()

        # Extract facts using the question-answering model
        result = qa_pipeline(question=question, context=call_log_text)
        extracted_fact = result['answer']

        # Process the extracted fact based on document ordering and fact modifications
        # ...

        facts.append(extracted_fact)

    return facts

def store_facts(question, facts):
    # Store the question and facts in a database or session
    # Implement the logic based on your chosen storage mechanism
    pass

def retrieve_facts():
    # Retrieve the question and facts from the database or session
    # Implement the logic based on your chosen storage mechanism
    # Return the retrieved question and facts
    pass

if __name__ == '__main__':
    app.run(debug=True)
