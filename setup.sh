#!/bin/bash

relPath="`dirname $0`"
cd $relPath
PYTHONPATH="$relPath/docked_env/bin/python"
if [ ! -f $PYTHONPATH ]; then
    python -m venv "$relPath/docked_env"
    source "$relPath/docked_env/bin/activate"
    pip install -r "$relPath/requirements.txt"
fi 
$PYTHONPATH "$relPath/docked.py"