import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        return RuntimeError("Api key is missing")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


    args = parser.parse_args()
    user_prompt = args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    generated_content = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    meta_data = generated_content.usage_metadata
    if meta_data == None:
        return RuntimeError("No meta data available, potential failed API call")
    
    if args.verbose:
        print("User prompt: {0}\nPrompt tokens: {1}\nResponse tokens: {2}\n".format(user_prompt, meta_data.prompt_token_count, meta_data.candidates_token_count))
    print("Response:\n{0}".format(generated_content.text))
if __name__ == "__main__":
    main()
