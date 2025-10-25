import os
from functions.config import * 

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
