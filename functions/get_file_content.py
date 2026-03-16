
import os
import config
from google.genai import types

def get_file_content(working_directory: str, file_path: str) -> str:
    '''
    Get the contents of a given file

        Parameters:
            working_directory (str): The current working directory
            file_path (str): Path to the file of which to retrieve the contents

        Returns:
            Contents of the given file or error string
    '''
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    
    if os.path.isfile(abs_file_path) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(abs_file_path, "r") as file:
        try:
            content = file.read(config.MAX_CHARACTERS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARACTERS} characters]'
            return content
        except:
            return f'Error: Cannot read {file_path}'
        

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file information in the specified file relative to the working directory, providing the content of the files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to show contents from, relative to the working directory",
            ),
        },
    ),
)