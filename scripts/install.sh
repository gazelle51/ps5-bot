# Create a virtualenv if it doesn't exist 
if [ ! -e .venv ]; 
then
  python3 -m venv .venv
  echo "Virtual environment created"
else
  echo "Virtual environment already exists"
fi

# Activate the virtualenv
source .venv/bin/activate 
echo "Virtual environment activated"

# Update pip
python -m pip install --upgrade pip
echo "Upgraded pip"

# Install requirements
pip3 install -r ./requirements.txt
echo "Dependencies installed"