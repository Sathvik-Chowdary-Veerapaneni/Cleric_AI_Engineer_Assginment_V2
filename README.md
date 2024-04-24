# Call Log Fact Extractor

This project is a web application that processes and extracts information from a set of call logs using a Language Learning Model (LLM). The application allows users to submit a question and a list of call logs, and presents a final list of facts extracted from these call logs.

## Project Setup

- Create a virtual environment to avoid conflicts with other Python projects.
- Add a `.gitignore` file to exclude certain files/folders from version control.
- Install required dependencies from the project's `requirements.txt` file.

## Tech Stack

- **Python Flask**: Used to run the local server and handle HTTP requests.
- **JavaScript (JS)**: Used to handle API calls and client-side interactions.
- **HTML/CSS**: Used for the frontend of the web application.

## Application Structure

The application consists of two main parts:

1. **Frontend**: The frontend is built using HTML, CSS, and JS. It consists of two screens:
    - **Input Screen**: Allows users to submit a question and a list of call logs.
    - **Output Screen**: Displays the final list of facts extracted from the call logs.

2. **Backend**: The backend is built using Python Flask. It processes the question and call logs using an LLM and extracts the relevant facts.

## API

The application provides two API endpoints:

- `POST /submit_question_and_documents`: Accepts a JSON payload with a question and a list of documents.
- `GET /get_question_and_facts`: Responds with a JSON object containing the question, facts, and status.

- Error Handling
- Testing
    - Unit tests and integration tests are included in the `tests/` directory.

## Deployment

The application is deployed online. (Include the URL of your deployed application here)



## Steps
``` source Cleric/bin/activate ```
