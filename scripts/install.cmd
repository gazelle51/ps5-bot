@REM Create a virtualenv if it doesn't exist 
IF NOT EXIST .venv\ (
  python -m venv .venv && ECHO "Virtual environment created"
) ELSE (
  ECHO "Virtual environment already exists"
)

@REM Activate the virtualenv
CALL .venv\Scripts\activate.bat
ECHO "Virtual environment activated"

@REM Update pip
python -m pip install --upgrade pip
ECHO "Upgraded pip"

@REM Install requirements
pip install -r ./requirements.txt
ECHO "Dependencies installed"