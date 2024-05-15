from flask import Flask
import os
from transformers import pipeline

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
    models = ['distilbert-base-cased-distilled-squad', 'bert-large-uncased-whole-word-masking-finetuned-squad']

    # Define the list of call log files
    call_log_files = ['logs_input/call_log_fdadweq.txt','logs_input/call_log_gfsfdfd.txt','logs_input/call_log_sdfqwer.txt']

    # Open the log file for writing
    with open('results.log', 'w') as log_file:
        # Iterate over each question
        for question in questions:
            # Iterate over each model
            for model_name in models:
                # Check if the model is available locally
                model_path = os.path.join(MODELS_FOLDER, model_name)
                if not os.path.exists(model_path):
                    # Download the model
                    try:
                        model = pipeline('question-answering', model=model_name)
                        model.save_pretrained(model_path)
                    except Exception as e:
                        log_entry = f"Error downloading model '{model_name}': {str(e)}\n"
                        log_entry += "-" * 50 + "\n"
                        log_file.write(log_entry)
                        continue

                # Load the model from the file path
                qa_pipeline = pipeline('question-answering', model=model_path)

                # Iterate over each call log file
                for call_log_file in call_log_files:
                    # Read the call log text
                    with open(call_log_file, 'r') as file:
                        call_log_text = file.read()

                    # Extract facts using the model
                    result = qa_pipeline(question=question, context=call_log_text)
                    extracted_fact = result['answer']

                    # Log the results
                    log_entry = f"Question: {question}\n"
                    log_entry += f"Model: {model_name}\n"
                    log_entry += f"Call Log File: {call_log_file}\n"
                    log_entry += f"Generated Answer: {extracted_fact}\n"
                    log_entry += "-" * 50 + "\n"
                    log_file.write(log_entry)

if __name__ == "__main__":
    test_models()