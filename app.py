from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extract the question and call logs from the form data
    question = request.form.get('question')
    call_logs = request.form.get('call_logs')

    # TODO: Process the question and call logs using an LLM

    # TODO: Extract the facts from the call logs

    # TODO: Render the output screen with the extracted facts
    return render_template('output.html')

if __name__ == '__main__':
    app.run(debug=True)
