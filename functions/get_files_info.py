import os

def get_files_info(working_directory: str, directory=".") -> str:
    '''
    Get the info of files within given directory

        Parameters:
            working_directory (str): The working directory
            directory (str): the target directory

        Returns:
            result (str): Returns an error or the requested file information

    '''
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_dir_target = os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs

    if valid_dir_target is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(target_dir) is False:
        return f'Error: "{directory}" is not a directory'
    
    final_str = ""
    for item in os.listdir(target_dir):
        try:
            item_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            final_str += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
            return final_str
        except:
            return f'Error: Failed to get the file information in the "{target_dir}" directory'