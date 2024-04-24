from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extract the question from the form data
    question = request.form.get('question')

    # Extract the uploaded files from the form data
    uploaded_files = request.files.getlist('file_upload')

    # Save the uploaded files to a local directory
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))

    # Extract the URLs from the form data
    urls = request.form.get('call_logs').split(',')

    # TODO: Fetch the files from the URLs

    # TODO: Process the question and call logs using an LLM

    # TODO: Extract the facts from the call logs

    # TODO: Render the output screen with the extracted facts
    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True)
