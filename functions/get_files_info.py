import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_path = os.path.join(working_directory, directory)

    if not os.path.abspath(working_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{working_path}" as it is outside the permitted working directory'
    if not os.path.isdir(working_path):
        return f'Error: "{directory}" is not a directory'

    retstr = ''
    try:
        for file in os.listdir(os.path.abspath(working_path)):
            path = f"{working_path}/{file}"
            retstr += f'- {file}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n'
        return retstr
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                    ),
                },
            ),
        )
