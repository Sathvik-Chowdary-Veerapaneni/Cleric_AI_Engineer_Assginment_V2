#!/bin/bash

# Change to the project directory

# cd cleric-ai-engineer-assignment

# Create a new Python virtual environment
python -m venv Cleric

# Activate the virtual environment
source Cleric/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Start the Flask application
python app.py