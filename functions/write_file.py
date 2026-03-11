import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    '''
    Writes data to the given file

        Parameters:
            Working_directory (str): The permitted working directory
            file_path (str): The path to the file to alter
            content (str): The content to overwrite the file with

        Return:
            Returns a string with a success or failure message
    '''
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(abs_file_path) is True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    if os.path.exists(abs_file_path) is False:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    
    with open(abs_file_path, "w") as file:
        try:
            l = file.write(content)
            return f'Successfully wrote to "{file_path}" ({l} characters written)'
        except:
            return f'Error: Cannot read {file_path}'