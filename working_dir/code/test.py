from jarvis.action.base_action import BaseAction
import os
import glob

class identify_ppt_file(BaseAction):
    def __init__(self):
        self._description = "Locate the PowerPoint file in the given path."

    def __call__(self, search_path, *args, **kwargs):
        """
        Locate the PowerPoint file in the given path.

        Args:
            search_path (str): The path where PowerPoint files will be searched.

        Returns:
            list: The paths of PowerPoint files found in the search path.
        """
        # List to store the paths of PowerPoint files
        ppt_files = []
        print(os.path.join(search_path, '*.ppt'))
        # Check if the search path exists
        if not os.path.exists(search_path):
            print(f"The search path {search_path} does not exist.")
            return ppt_files

        # Search for PowerPoint files with .ppt and .pptx extensions
        ppt_files.extend(glob.glob(os.path.join(search_path, '*.ppt')))
        ppt_files.extend(glob.glob(os.path.join(search_path, '*.pptx')))

        # Print the task execution completion message
        print(f"Task execution complete. Found {len(ppt_files)} PowerPoint files.")

        # Return the list of PowerPoint files
        return ppt_files

print(identify_ppt_file()(search_path='/home/heroding/.cache/huggingface/datasets/downloads/1f26582c64d2b6df0030f51c5e3a01a51014fca32537d95112fdda518e0861c9'))