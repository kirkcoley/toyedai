import os

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is ouside the permitted working directory'
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.path.makedirs(os.path.dirname(path))
        except Exception as e:
            return f'Error: {e}'

    try:
        file = open(path, "w")
    except Exception as e:
        return f"Error: {e}"
    else:
        with file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

