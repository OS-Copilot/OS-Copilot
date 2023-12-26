
from jarvis.action.base_action import BaseAction
import os
import requests

class download_file(BaseAction):
    def __init__(self):
        self._description = "Download a file from a provided URL to a specified directory."

    def __call__(self, download_url, file_name, working_directory=None, *args, **kwargs):
        """
        Download a file from the specified URL and save it to the given directory with the provided file name.

        Args:
            download_url (str): The URL from which the file will be downloaded.
            file_name (str): The name to save the file as.
            working_directory (str, optional): The directory where the file will be saved.
                If not provided, the current working directory will be used.

        Returns:
            str: The absolute path to the downloaded file.
        """
        # If a working directory is provided, change to that directory
        if working_directory:
            os.chdir(working_directory)
        else:
            # Use the current working directory if none is provided
            working_directory = os.getcwd()

        # The full path to where the file will be saved
        file_path = os.path.join(working_directory, file_name)

        # Download the file
        try:
            response = requests.get(download_url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded file saved to {file_path}")
            return file_path
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the file from {download_url}: {e}")

# Example of how to use the class (this should be in the comments and not executed):
# downloader = download_file()
# downloader(download_url='https://example.com/image.jpg', file_name='image.jpg', working_directory='/path/to/directory')
