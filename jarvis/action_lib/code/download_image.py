
from jarvis.action.base_action import BaseAction
import requests
import os

class download_image(BaseAction):
    def __init__(self):
        self._description = "Download an image from a provided URL to the local system."

    def __call__(self, image_url, image_name, save_directory, *args, **kwargs):
        """
        Download the image from the specified URL and save it to the given directory with the provided image name.

        Args:
            image_url (str): The URL of the image to be downloaded.
            image_name (str): The name to save the image as.
            save_directory (str): The directory where the image will be saved.
            
        Returns:
            str: The absolute path to the downloaded image.
        """
        # Ensure the save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        # If the image name does not contain an extension, add '.jpg'
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_name += '.jpg'
        
        # Construct the full path for the image
        image_path = os.path.join(save_directory, image_name)
        
        # Download the image
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            
            # Write the image to a file
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully and saved as {image_path}.")
            
            return image_path
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while downloading the image: {e}")
            return None

# Example of how to use the class (this should be in the comments and not executed):
# downloader = download_image()
# image_path = downloader(image_url='https://example.com/image.jpg', image_name='downloaded_image', save_directory='/path/to/save')
