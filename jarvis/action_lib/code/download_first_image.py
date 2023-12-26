
from jarvis.action.base_action import BaseAction
import os
import requests

class download_first_image(BaseAction):
    def __init__(self):
        self._description = "Download the first image from the search results and save it in the current working directory."

    def __call__(self, image_url, save_path='image1.jpg', working_directory=None, *args, **kwargs):
        """
        Download the first image from the search results and save it as image1.jpg in the current working directory.

        Args:
            image_url (str): The URL of the image to be downloaded.
            save_path (str): The filename to save the downloaded image as. Default is 'image1.jpg'.
            working_directory (str, optional): The working directory where the file will be saved.
                If not provided, the current working directory will be used.

        Returns:
            None
        """
        # If a working directory is provided, change to that directory
        if working_directory:
            os.chdir(working_directory)
        else:
            # Use the current working directory if none is provided
            working_directory = os.getcwd()

        # Download the image
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

            # Save the image
            with open(os.path.join(working_directory, save_path), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded the image successfully and saved as {save_path} in {working_directory}.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the image: {e}")

# Example of how to use the class (this should be in the comments and not executed):
# downloader = download_first_image()
# downloader(image_url='https://example.com/image.jpg', save_path='image1.jpg', working_directory='/home/heroding/桌面/Jarvis/working_dir')
