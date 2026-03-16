import os
import pathlib
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(abs_file_path) is False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if pathlib.Path(abs_file_path).suffix != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", abs_file_path]

    if args != None:
        command.extend(args)

    completed_process = subprocess.run(args=command, cwd=abs_working_dir, text=True, timeout=30, capture_output=True)

    oStr = ""
    try:
        if completed_process.returncode != 0:
            oStr += f'Error: Process exited with code {completed_process.returncode}\n'
    
        if completed_process.stderr and completed_process.stdout is False:
            oStr += f'No output produced'
        else:
            oStr += f'STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'
        return oStr
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the provided python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the python file to be executed",
            ),
            "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="Optional list of string arguments to pass to the Python script",
            ),
        },
    ),
)