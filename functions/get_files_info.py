import os

def get_files_info(working_directory, directory="."):
    working_path = os.path.join(working_directory, directory)

    if not os.path.abspath(working_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{working_path}" as it is outside the permitted working directory'
    if not os.path.isdir(working_path):
        return f'Error: "{directory}" is not a directory'

    retstr = ''
    for file in os.listdir(working_path):
        path = f"{working_path}/{file}"
        retstr += f'- {file}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n'
    return retstr
