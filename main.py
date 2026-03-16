import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ai_settings import (prompts, call_function)
import config

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Api key is missing")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_prompt = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for _ in range(config.MAX_ITERATIONS):
        generated_content = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(
                                                                                                    system_instruction=prompts.system_prompt,
                                                                                                    temperature=0,
                                                                                                    tools=[call_function.available_functions]))
        
        if generated_content.candidates:
            for candidate in generated_content.candidates:
                messages.append(candidate.content)

        meta_data = generated_content.usage_metadata
        if meta_data == None:
            raise RuntimeError("No meta data available, potential failed API call")
    
        function_responses = []

        if args.verbose:
            print("User prompt: {0}\nPrompt tokens: {1}\nResponse tokens: {2}\n".format(user_prompt, meta_data.prompt_token_count, meta_data.candidates_token_count))
        
        if not generated_content.function_calls:
            print(f"Final response: \n{generated_content.text}")
            return
        else:
            for call in generated_content.function_calls:
                function_call_result: types.Content = call_function.call_function(call, args.verbose)

                if not function_call_result.parts:
                    raise ValueError(f"Function call returned no parts for: {call.name}")

                function_call_response = function_call_result.parts[0].function_response
                if function_call_response is None:
                    raise ValueError(f"No function response in parts for: {call.name}")

                if function_call_response.response is None:
                    raise ValueError(f"Function response has no data for: {call.name}")
    
                function_responses.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_responses))

    print (f"Maximum iteration count ({config.MAX_ITERATIONS}) reached without a final response")
    sys.exit(1)
if __name__ == "__main__":
    main()
