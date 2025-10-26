import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions
from call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) == 1 or sys.argv[1] == '--verbose':
        raise Exception("prompt required")

    system_prompt = '''
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    '''
    user_prompt = sys.argv[1]

    messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
    limit = 0

    while limit < 20:
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                    ),
                )
            
            for cand in response.candidates:
                messages.append(cand.content)

            if response.function_calls:
                for c in response.function_calls:
                    call = call_function(c)
                    if not call.parts[0].function_response.response:
                        raise Exception('No response in Content object')
                    if "--verbose" in sys.argv:
                        print(f"-> {call.parts[0].function_response.response}")
                    messages.append(types.Content(role="user", parts=[types.Part(text=call.parts[0].function_response.response['result'])]))
                    #print(call.parts[0].function_response.response['result'])
        except Exception as e:
            print(f'Error: {e}')

        if response.text and not response.function_calls:
            print(response.text)
            break
        limit += 1
            


    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")




if __name__ == "__main__":
    main()
