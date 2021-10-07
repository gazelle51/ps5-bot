@REM Create a virtualenv if it doesn't exist 
if not exist .venv\ (
  python -m venv .venv  &
  echo "Virtual environment created"
) &

@REM Activate the virtualenv
.venv\Scripts\activate.bat &

@REM Update pip
python -m pip install --upgrade pip &

@REM Install requirements
pip install -r ./requirements.txt  &

echo "Dependencies installed"