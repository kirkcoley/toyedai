import os
from functions.config import * 
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        file = open(path, "r")
    except Exception as e:
        return f"Error: {e}"
    else:
        with file:
            file_con_str = file.read(MAX_CHARS)
            if not file.read(1):
                return file_con_str
            else:
                return f'{file_con_str} [...File "{file_path}" truncated at 10000 characters]'

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Print the contents of the specified file up to 10000 characters, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="A file, relative to the working directory, the contents of which will be printed.",
                    ),
                },
            ),
        )
