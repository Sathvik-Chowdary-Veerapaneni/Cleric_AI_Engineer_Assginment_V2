from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from transformers import pipeline

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session handling

qa_pipeline = pipeline('question-answering')

import os
from werkzeug.utils import secure_filename

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def input_screen():
    if request.method == 'POST':
        question = request.form['question']
        uploaded_files = request.files.getlist('file_uploads')
        
        # Save the uploaded files
        file_names = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_names.append(file_path)
        
        print(f"Question: {question}")
        print(f"File Names: {file_names}")
        
        try:
            facts = extract_facts(question, file_names)
            store_facts(question, facts)
            return redirect(url_for('output_screen'))
        except FileNotFoundError as e:
            error_message = f"File not found: {str(e)}"
            return render_template('error.html', error_message=error_message), 404
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('error.html', error_message=error_message), 500
    
    return render_template('input.html')

@app.route('/output')
def output_screen():
    print("Retrieving facts...")
    result = retrieve_facts()
    print(f"Retrieved Result: {result}")
    
    if result is None or len(result) != 2:
        return "Error: Unable to retrieve question and facts.", 500
    
    question, facts = result
    return render_template('output.html', question=question, facts=facts)

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.get_json()
    question = data['question']
    file_names = data['documents']
    
    facts = extract_facts(question, file_names)
    store_facts(question, facts)
    
    return '', 200

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    result = retrieve_facts()
    
    if result is None or len(result) != 2:
        return jsonify({'error': 'Unable to retrieve question and facts'}), 500
    
    question, facts = result
    
    response = {
        'question': question,
        'facts': facts,
        'status': 'done'
    }
    
    return jsonify(response), 200
    

def extract_facts(question, file_names):
    facts = []
    
    for file_name in file_names:
        file_path = os.path.join('logs_input', file_name.strip())
        print(f"Reading file: {file_path}")
        
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue
        
        with open(file_path, 'r') as file:
            call_log_text = file.read()
        
        result = qa_pipeline(question=question, context=call_log_text)
        extracted_fact = result['answer']
        facts.append(extracted_fact)
    
    print(f"Extracted Facts: {facts}")
    return facts

def store_facts(question, facts):
    session['question'] = question
    session['facts'] = facts
    
    print(f"Stored Question: {question}")
    print(f"Stored Facts: {facts}")

def retrieve_facts():
    question = session.get('question')
    facts = session.get('facts')
    
    print(f"Retrieved Question: {question}")
    print(f"Retrieved Facts: {facts}")
    
    return question, facts

if __name__ == '__main__':
    app.run(debug=True)