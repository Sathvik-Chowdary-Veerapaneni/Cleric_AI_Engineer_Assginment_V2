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

    # Process the question and documents
    facts = extract_facts(question, documents)

    # Store the question, facts, and status
    # ...

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



def extract_facts(question, documents):
    # Load a pre-trained model for question-answering
    qa_pipeline = pipeline('question-answering')

    facts = []
    for document in documents:
        # Fetch the call log text from the URL
        response = requests.get(document)
        call_log_text = response.text

        # Extract facts using the question-answering model
        result = qa_pipeline(question=question, context=call_log_text)
        extracted_fact = result['answer']

        # Process the extracted fact based on document ordering and fact modifications
        # ...

        facts.append(extracted_fact)

    return facts


if __name__ == '__main__':
    app.run(debug=True)
