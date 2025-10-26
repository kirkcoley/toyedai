import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found'
    if not path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    arg_list = ['python', os.path.abspath(path)] + args

    try:
        comp_proc = subprocess.run(arg_list, capture_output=True, cwd=os.path.abspath(working_directory), text=True, timeout=30)
    except Exception as e:
        return f'Error: executing Python file: {e}\nsubprocess called with {args}, in {working_directory}'

    if comp_proc.returncode != 0:
        return f'STDOUT: {comp_proc.stdout}\nSTDERR: {comp_proc.stderr}\nProcess exited with code {comp_proc.returncode}'
    if comp_proc.stdout == None and comp_proc.stderr == None:
        return "No output produced."
    else:
        return f'STDOUT: {comp_proc.stdout}\nSTDERR: {comp_proc.stderr}'

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Run a Python file at the specified location, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the target file.",
                    ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="A list of arguments to be provided to the target python file.",
                    ),
                },
            ),
        )

