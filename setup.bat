SET scriptDir=%~dp0

cd %scriptDir%


if NOT EXIST %scriptDir%docked\Scripts\python (
    CALL python -m venv %scriptDir%docked
    CALL %scriptDir%docked\Scripts\activate.bat
    CALL python -m pip install -r requirments.txt
) 

CALL %scriptDir%docked\Scripts\python %scriptDir%riffler.py
