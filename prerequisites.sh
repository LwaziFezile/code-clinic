#! usr/bin/bash

current_directory=$(pwd)
cd "$current_directory"

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install packages from requirements.txt
if [ -f "$current_directory/requirements.txt" ]; then
    pip install -r "$current_directory/requirements.txt"
    echo "Packages installed successfully."
else
    echo "Error: requirements.txt file not found."
fi


echo "Script execution completed. Change interpreter to the venv interpreter. Type 'deactivate' to deactivate venv"
