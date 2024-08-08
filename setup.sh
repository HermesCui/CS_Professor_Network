#!/bin/bash

# Check if a virtual environment directory name was provided
if [ -z "$1" ]; then
  VENV_DIR="myenv"  # Default directory name is 'myenv' if none provided
else
  VENV_DIR="$1"
fi

# Create the virtual environment
echo "Creating virtual environment in directory: $VENV_DIR"
python3 -m venv "$VENV_DIR"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install the required Python packages
echo "Installing required Python packages..."
pip install --upgrade pip
pip install requests beautifulsoup4 networkx matplotlib

echo "Setup complete. The virtual environment '$VENV_DIR' is ready and the required packages are installed."
echo "To deactivate the virtual environment, run 'deactivate'."
