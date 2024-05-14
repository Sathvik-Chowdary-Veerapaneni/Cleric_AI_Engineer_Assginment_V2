from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = 'your_secret_key'  # Set a secret key for session handling

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure the models folder
MODELS_FOLDER = 'models'
app.config['MODELS_FOLDER'] = MODELS_FOLDER

@app.route('/', methods=['GET', 'POST'])
def input_screen():
    if request.method == 'POST':
        question = request.form['question']
        model_name = request.form['model_name']
        uploaded_files = request.files.getlist('file_uploads')
        
        # Save the uploaded files
        file_names = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_names.append(file_path)
        
        # Download and save the selected model
        model_path = download_model(model_name)
        
        # Load the selected model
        qa_pipeline = pipeline('question-answering', model=model_path)
        
        try:
            facts = extract_facts(question, file_names, qa_pipeline)
            store_facts(question, facts, model_name)
            return redirect(url_for('output_screen'))
        except FileNotFoundError as e:
            error_message = f"File not found: {str(e)}"
            return render_template('error.html', error_message=error_message), 404
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('error.html', error_message=error_message), 500
    
    return render_template('input.html')

def download_model(model_name):
    model_path = os.path.join(app.config['MODELS_FOLDER'], model_name)
    
    if not os.path.exists(model_path):
        # Download and save the model
        model = pipeline('question-answering', model=model_name)
        model.save_pretrained(model_path)
    
    return model_path

@app.route('/output')
def output_screen():
    result = retrieve_facts()
    
    if result is None or len(result) != 3:
        return "Error: Unable to retrieve question, facts, and model name.", 500
    
    question, facts, model_name = result
    return render_template('output.html', question=question, facts=facts, model_name=model_name)

@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.get_json()
    question = data['question']
    model_name = data['model_name']
    file_names = data['documents']
    
    # Load the selected model
    qa_pipeline = pipeline('question-answering', model=model_name)
    
    facts = extract_facts(question, file_names, qa_pipeline)
    store_facts(question, facts, model_name)
    
    return '', 200

@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    result = retrieve_facts()
    
    if result is None or len(result) != 3:
        return jsonify({'error': 'Unable to retrieve question, facts, and model name'}), 500
    
    question, facts, model_name = result
    
    response = {
        'question': question,
        'facts': facts,
        'model_name': model_name,
        'status': 'done'
    }
    
    return jsonify(response), 200

def extract_facts(question, file_names, qa_pipeline):
    facts = []
    
    for file_name in file_names:
        with open(file_name, 'r') as file:
            call_log_text = file.read()
        
        result = qa_pipeline(question=question, context=call_log_text)
        extracted_fact = result['answer']
        facts.append(extracted_fact)
    
    return facts

def store_facts(question, facts, model_name):
    model_folder = os.path.join(app.config['MODELS_FOLDER'], model_name)
    os.makedirs(model_folder, exist_ok=True)
    
    question_file = os.path.join(model_folder, 'questions.txt')
    with open(question_file, 'a') as file:
        file.write(question + '\n')
    
    session['question'] = question
    session['facts'] = facts
    session['model_name'] = model_name

def retrieve_facts():
    question = session.get('question')
    facts = session.get('facts')
    model_name = session.get('model_name')
    
    if question and facts and model_name:
        return question, facts, model_name
    else:
        return None

if __name__ == "__main__":
    app.run(port=8000, debug=True)