@echo OFF
ECHO Activating virtual environment...
REM Corrected the path to your specific virtual environment name
CALL ml-service.venv\Scripts\activate

ECHO.
ECHO =================================
ECHO  Starting Model Training
ECHO =================================
python train_model.py

ECHO.
ECHO =================================
ECHO  Starting FastAPI Server
ECHO =================================
uvicorn model_server:app --reload --port 5000
