# Create a virtualenv if it doesn't exist 
if [ ! -e .venv ]; then
  python3 -m venv .venv
fi

# Activate the virtualenv
source .venv/bin/activate 

# Update pip
python -m pip install --upgrade pip

# Install requirements
pip3 install -r ./requirements.txt 