#!/bin/bash

# Function to create and activate virtual environment
ve() {
    local py_version=$(python --version | awk '{print $2}' | cut -d'.' -f1-2)
    local py="python${py_version}"
    local venv="Cleric"

    local bin="${venv}/bin/activate"

    # If not already in virtualenv
    if [ -z "${VIRTUAL_ENV}" ]; then
        if [ ! -d ${venv} ]; then
            echo "Creating and activating virtual environment ${venv}"
            ${py} -m venv ${venv} --system-site-package
            source ${bin}
            echo "Upgrading pip"
            ${py} -m pip install --upgrade pip
        else
            echo "Virtual environment ${venv} already exists, activating..."
            source ${bin}
        fi
    else
        echo "Already in a virtual environment!"
    fi
}

# Change to the project directory
cd cleric-ai-engineer-assignment

# Create and activate the virtual environment
ve

# Install the required dependencies
pip install -r requirements.txt

# Start the Flask application
python app.py