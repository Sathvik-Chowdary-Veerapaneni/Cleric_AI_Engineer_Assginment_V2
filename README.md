# Cleric AI Engineer Assignment

## Introduction

This project is an implementation of the Cleric AI Engineer Assignment, which involves creating a web application that processes and extracts information from a set of call logs using a Language Model (LLM). The application allows users to provide a single question along with a list of call logs, and it extracts and presents a final list of facts relevant to the question.

## Assignment Requirements

The key requirements of the assignment are as follows:

1. Develop a web application with two main screens:
   - Input Screen: Allows users to submit a question and a list of call logs by providing one or more URLs.
   - Output Screen: Displays the final list of extracted facts.

2. Process the call log documents to extract facts relevant to the question, considering document ordering and fact modifications.

3. Optimize the application for accuracy and use a pre-trained LLM (GPT-4 or a model with comparable performance).

4. Provide API endpoints for submitting questions and documents, and retrieving question and facts.

5. Implement error handling and ensure the application can handle common errors gracefully.

## Implementation Details

The application is built using Flask, a Python web framework, and utilizes the Hugging Face Transformers library for natural language processing tasks. The key components of the implementation include:

1. Flask application structure with routes for the Input Screen, Output Screen, and API endpoints.

2. Integration of pre-trained LLMs from Hugging Face for fact extraction and question-answering tasks.

3. Document processing logic to handle call log files, extract relevant facts, and consider document ordering and fact modifications.

4. API endpoints for submitting questions and documents, and retrieving question and facts.

5. Error handling and logging functionality to handle common errors and log application events.

6. User interface improvements, including styling, clear instructions, and dropdown menus for model selection.

## Usage

To run the application locally, follow these steps:

1. Clone the project repository:
   ```
   git clone https://github.com/your-username/cleric-ai-engineer-assignment.git
   ```
2. Create a environment using Python
   ```
   python -m venv Celric
   ```
3. Activate the environment
   ```
   source Celric/bin/activate
   ```
   
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the Flask application:
   ```
   python app.py
   ```

6. Access the application in your web browser at your `local host`.

## Evaluation and Testing

The application has been tested using a set of predefined questions and call log files. The performance of different pre-trained models (distilbert-base-cased-distilled-squad and bert-large-uncased-whole-word-masking-finetuned-squad) has been evaluated, and the results are stored in the `results.log` file.

To further evaluate the application, you can:

1. Modify the `questions.txt` file to include additional test questions.

2. Place the corresponding call log files in the `logs_input` directory.

3. Run the `test_models()` function in `auto_test.py` to process the questions and generate the `results.log` file.

4. Review the `results.log` file to assess the performance of the models and the accuracy of the extracted facts.

## Future Enhancements

Some potential enhancements to the application include:

1. Fine-tuning the pre-trained models on a dataset specifically designed for fact extraction from conversation logs to improve accuracy.

2. Implementing additional error handling and validation mechanisms to ensure robustness.

3. Enhancing the user interface with more interactive features and visualizations.

4. Integrating additional LLMs or exploring ensemble techniques to improve fact extraction performance.

## Conclusion

This project demonstrates the implementation of a web application that processes call logs and extracts relevant facts based on user-provided questions using pre-trained Language Models. It fulfills the key requirements of the Cleric AI Engineer Assignment and provides a foundation for further enhancements and improvements.

For any questions or inquiries, please contact Sathvik Veerapaneni at sathvikveerapaneni@gmail.com
