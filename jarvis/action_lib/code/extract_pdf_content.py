from jarvis.action.base_action import BaseAction
import PyPDF2
import os

class extract_pdf_content(BaseAction):
    def __init__(self):
        self._description = "Extract the text content from a specified PDF file."

    def __call__(self, pdf_file_path, *args, **kwargs):
        """
        Extract the text content from the specified PDF file and return its content.

        Args:
            pdf_file_path (str): The absolute path to the PDF file to be read.

        Returns:
            str: The text content of the PDF file.
        """
        try:
            # Ensure the PDF file exists
            if not os.path.isfile(pdf_file_path):
                print(f"The PDF file {pdf_file_path} does not exist.")
                return
            
            # Open the PDF file
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = ''
                
                # Iterate through each page and extract text
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text()
            
            print(f"Task execution complete. Content of the PDF file {pdf_file_path} extracted successfully.")
            return text_content
        except FileNotFoundError:
            print(f"The PDF file {pdf_file_path} does not exist.")
        except PyPDF2.errors.PdfReadError as e:
            print(f"An error occurred while reading the PDF file {pdf_file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Example of how to use the class (this should be in the comments):
# extractor = extract_pdf_content()
# content = extractor(pdf_file_path='/home/heroding/.cache/huggingface/datasets/downloads/9f3ace58caffc356d97dd86ada4e266d2054f59dad0950f287f9791ddcff64fa.pdf')
