from flask import Flask
import os
from transformers import pipeline
import uuid

app = Flask(__name__)

# Configure the models folder
MODELS_FOLDER = 'models'
app.config['MODELS_FOLDER'] = MODELS_FOLDER

def test_models():
    # Read the questions from the file
    with open('questions.txt', 'r') as file:
        questions = file.readlines()
    
    # Strip any whitespace from the questions
    questions = [question.strip() for question in questions]
    
    # Define the list of models to test
    models = ['distilbert-base-cased-distilled-squad', 'bert-large-uncased-whole-word-masking-finetuned-squad', 'roberta-base-squad2']
    
    # Define the list of call log files
    call_log_files = ['logs_input/call_log_1.txt', 'logs_input/call_log_2.txt', 'logs_input/call_log_3.txt']
    
    # Iterate over each model
    for model_name in models:
        # Load the model from the file path
        model_path = os.path.join(MODELS_FOLDER, model_name)
        qa_pipeline = pipeline('question-answering', model=model_path)
        
        # Iterate over each question
        for question in questions:
            # Generate a unique folder for each question
            question_folder = str(uuid.uuid4())
            os.makedirs(question_folder, exist_ok=True)
            
            # Iterate over each call log file
            for call_log_file in call_log_files:
                # Read the call log text
                with open(call_log_file, 'r') as file:
                    call_log_text = file.read()
                
                # Extract facts using the model
                result = qa_pipeline(question=question, context=call_log_text)
                extracted_fact = result['answer']
                
                # Save the extracted fact to a file in the question folder
                fact_file = os.path.join(question_folder, f"{os.path.basename(call_log_file)}_fact.txt")
                with open(fact_file, 'w') as file:
                    file.write(extracted_fact)
            
            # Log the results for the question
            log_results(question, model_name, question_folder)

def log_results(question, model_name, question_folder):
    log_entry = f"Question: {question}\n"
    log_entry += f"Model Used: {model_name}\n"
    
    # Read the extracted facts from the question folder
    fact_files = [file for file in os.listdir(question_folder) if file.endswith('_fact.txt')]
    for fact_file in fact_files:
        with open(os.path.join(question_folder, fact_file), 'r') as file:
            extracted_fact = file.read()
        log_entry += f"Extracted Fact ({os.path.basename(fact_file)}): {extracted_fact}\n"
    
    log_entry += "-" * 50 + "\n"
    
    with open('results.log', 'a') as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    test_models()