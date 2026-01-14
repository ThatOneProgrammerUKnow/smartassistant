import webbrowser, os
from subprocess import Popen
from pathlib import Path
from . import program

# Load programs
program.load()

# If program object exists
def exists(choice):
    if program.is_valid(choice):
        return True
    return False

# Open a program    
def open(choice):
    obj = program.find(choice)

    path = Path(obj.path)
    # If its a file 
    if path.is_file():
        os.startfile(path)

    # If its a computer program
    elif path.exists():
        Popen(obj.path)

    # Open website
    else:
        try:
            webbrowser.open(obj.path)
        except webbrowser.Error as e:
            raise RuntimeError(f"Failed to open website: {obj.path}") from e

# Get program name
def get_name(choice):
    obj = program.find(choice)
    return obj.name

# List all
def all_program_options():
    return program.all()


    