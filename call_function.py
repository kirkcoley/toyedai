from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info

from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content

from functions.write_file import schema_write_file
from functions.write_file import write_file

from functions.run_python_file import schema_run_python_file
from functions.run_python_file import run_python_file

available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
            ]
        )

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    arg_dict = function_call_part.args
    arg_dict["working_directory"] = "./calculator"

    function_lookup = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python_file": run_python_file,
            }

    if function_call_part.name in function_lookup:
        cap = function_lookup[function_call_part.name](**arg_dict)
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": cap},
                        )
                    ],
                )
    else:
        return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                ],
                )

    #match function_call_part.name:
    #    case 'get_files_info':
    #        # call get_files_info
    #        get_files_info(working_dir, **function_call_part.args)

    #    case 'get_file_content':
            # call get_file_content
    #        get_file_content(working_dir, **function_call_part.args)
    #    case 'write_file':
            # call write_file
    #        write_file()
    #    case 'run_python_file':
            # cal run_python_file
    #        run_python_file()
    #    case _:
    #        return types.Content(
    #                role="tool",
    #                parts=[
    #                types.Part.from_function_response(
    #                    name=function_name,
    #                    response={"error": f"Unknown function: {function_name}"},
    #                    )
    #                ],
    #                )
