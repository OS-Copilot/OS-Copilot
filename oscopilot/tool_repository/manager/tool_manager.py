# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
import argparse
import json
import sys
import os
import re
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')

EMBED_MODEL_TYPE = os.getenv('MODEL_TYPE')
EMBED_MODEL_NAME = os.getenv('MODEL_NAME')

class ToolManager:
    """
    Manages tools within a repository, including adding, deleting, and retrieving tool information.

    The `ToolManager` class provides a comprehensive interface for managing a collection
    of tools, where each tool is associated with its code, description, and other metadata.
    It supports operations such as adding new tools, checking for the existence of tools,
    retrieving tool names, descriptions, and codes, and deleting tools from the collection.
    It leverages a vector database for efficient retrieval of tools based on similarity searches.

    Attributes:
        generated_tools (dict): Stores the mapping relationship between tool names and their
                                information (code, description).
        generated_tool_repo_dir (str): The directory path where the tools' information is stored,
                                       including code files, description files, and a JSON file
                                       containing the tools' metadata.
        vectordb_path (str): The path to the vector database used for storing and retrieving
                             tool descriptions based on similarity.
        vectordb (Chroma): An instance of the Chroma class for managing the vector database.

    Note:
        The class uses OpenAI's `text-embedding-ada-002` model by default for generating embeddings
        via the `OpenAIEmbeddings` wrapper. Ensure that the `OPENAI_API_KEY` and `OPENAI_ORGANIZATION`
        are correctly set for OpenAI API access.

    This class is designed to facilitate the management of a dynamic collection of tools, providing
    functionalities for easy addition, retrieval, and deletion of tools. It ensures that the tools'
    information is synchronized across a local repository and a vector database for efficient
    retrieval based on content similarity.
    """

    def __init__(self, generated_tool_repo_dir=None):
        # generated_tools: Store the mapping relationship between descriptions and tools (associated through task names)
        self.generated_tools = {}
        self.generated_tool_repo_dir = generated_tool_repo_dir
        
        with open(f"{self.generated_tool_repo_dir}/generated_tools.json") as f2:
            self.generated_tools = json.load(f2)
        self.vectordb_path = f"{generated_tool_repo_dir}/vectordb"

        if not os.path.exists(self.vectordb_path):
            os.makedirs(self.vectordb_path)
        os.makedirs(f"{generated_tool_repo_dir}/tool_code", exist_ok=True)
        os.makedirs(f"{generated_tool_repo_dir}/tool_description", exist_ok=True)
        # Utilize the Chroma database and employ OpenAI Embeddings for vectorization (default: text-embedding-ada-002)
        
        if EMBED_MODEL_TYPE == "OpenAI":
            embedding_function = OpenAIEmbeddings(
                openai_api_key=OPENAI_API_KEY,
                openai_organization=OPENAI_ORGANIZATION,
            )
        elif EMBED_MODEL_TYPE == "OLLAMA":
            embedding_function = OllamaEmbeddings(model=EMBED_MODEL_NAME)
        
        self.vectordb = Chroma(
            collection_name="tool_vectordb",
            embedding_function=embedding_function,
            persist_directory=self.vectordb_path,
        )
        assert self.vectordb._collection.count() == len(self.generated_tools), (
            f"Tool Manager's vectordb is not synced with generated_tools.json.\n"
            f"There are {self.vectordb._collection.count()} tools in vectordb but {len(self.generated_tools)} tools in generated_tools.json.\n"
        )


    @property
    def programs(self):
        """
        Retrieve all the code from the code repository as a single string.

        This property concatenates the code of all tools stored in the generated_tools
        dictionary, separating each tool's code with two newlines.

        Returns:
            str: A string containing the code of all tools, each separated by two newlines.
        """
        programs = ""
        for _, entry in self.generated_tools.items():
            programs += f"{entry['code']}\n\n"
        return programs
    

    @property
    def descriptions(self):
        """
        Retrieve the descriptions of all tools in a dictionary.

        This property constructs a dictionary where each key is a tool name and its value
        is the description of that tool, extracted from the generated_tools dictionary.

        Returns:
            dict: A dictionary mapping each tool name to its description.
        """
        descriptions = {}
        for tool_name, entry in self.generated_tools.items():
            descriptions.update({tool_name: entry["description"]})
        return descriptions
    

    @property
    def tool_names(self):
        """
        Retrieve all tool class names from the generated tools.

        This property provides access to the names of all tools stored in the
        generated_tools dictionary, facilitating enumeration over tool names.

        Returns:
            KeysView[str]: A view of the dictionary's keys which are the names of the tools.
        """
        return self.generated_tools.keys()
    

    def get_tool_code(self, tool_name):
        """
        Retrieve the code of a specific tool by its name.

        Given a tool name, this method fetches and returns the code associated with
        that tool from the generated_tools dictionary. If the tool does not exist,
        a KeyError will be raised.

        Args:
            tool_name (str): The name of the tool for which the code is requested.

        Returns:
            str: The code of the specified tool.

        Raises:
            KeyError: If the tool_name does not exist in the generated_tools dictionary.
        """
        code = self.generated_tools[tool_name]['code']
        return code    


    def add_new_tool(self, info):
        """
        Adds a new tool to the tool manager, including updating the vector database
        and tool repository with the provided information.

        This method processes the given tool information, which includes the task name,
        code, and description. It prints out the task name and description, checks if
        the tool already exists (rewriting it if so), and updates both the vector
        database and the tool dictionary. Finally, it persists the new tool's code and
        description in the repository and ensures the vector database is synchronized
        with the generated tools.

        Args:
            info (dict): A dictionary containing the tool's information, which must
                         include 'task_name', 'code', and 'description'.

        Raises:
            AssertionError: If the vector database's count does not match the length
                            of the generated_tools dictionary after adding the new tool,
                            indicating a synchronization issue.
        """
        program_name = info["task_name"]
        program_code = info["code"]
        program_description = info["description"]
        print(
            f"\033[33m {program_name}:\n{program_description}\033[0m"
        )
        # If this task code already exists in the tool library, delete it and rewrite
        if program_name in self.generated_tools:
            print(f"\033[33mTool {program_name} already exists. Rewriting!\033[0m")
            self.vectordb._collection.delete(ids=[program_name])
        # Store the new task code in the vector database and the tool dictionary
        self.vectordb.add_texts(
            texts=[program_description],
            ids=[program_name],
            metadatas=[{"name": program_name}],
        )
        self.generated_tools[program_name] = {
            "code": program_code,
            "description": program_description,
        }
        assert self.vectordb._collection.count() == len(
            self.generated_tools
        ), "vectordb is not synced with generated_tools.json"
        # Store the new task code and description in the tool repo, and enter the mapping relationship into the dictionary
        with open(f"{self.generated_tool_repo_dir}/tool_code/{program_name}.py", "w") as fa:
            fa.write(program_code)
        with open(f"{self.generated_tool_repo_dir}/tool_description/{program_name}.txt", "w") as fb:
            fb.write(program_description)
        with open(f"{self.generated_tool_repo_dir}/generated_tools.json", "w") as fc:
            json.dump(self.generated_tools,fc,indent=4)
        self.vectordb.persist()
        # with open(f"{self.generated_tool_repo_dir}/generated_tools.json") as f2:
        #     self.generated_tools = json.load(f2)


    def exist_tool(self, tool):
        """
        Checks if a tool exists in the tool manager based on the tool name.

        Args:
            tool (str): The name of the tool to check.

        Returns:
            bool: True if the tool exists, False otherwise.
        """
        if tool in self.tool_names:
            return True
        return False


    def retrieve_tool_name(self, query, k=10):
        """
        Retrieves related tool names based on a similarity search against a query.

        This method performs a similarity search in the vector database for the given
        query and retrieves the names of the top `k` most similar tools. It prints the
        number of tools being retrieved and their names.

        Args:
            query (str): The query string to search for similar tools.
            k (int, optional): The maximum number of similar tools to retrieve.
                               Defaults to 10.

        Returns:
            list[str]: A list of tool names that are most similar to the query,
                       up to `k` tools. Returns an empty list if no tools are found
                       or if `k` is 0.

        """
        k = min(self.vectordb._collection.count(), k)
        if k == 0:
            return []
        print(f"\033[33mTool Manager retrieving for {k} Tools\033[0m")
        # Retrieve descriptions of the top k related tasks.
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
        print(
            f"\033[33mTool Manager retrieved tools: "
            f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
        )
        tool_name = []
        for doc, _ in docs_and_scores:
            tool_name.append(doc.metadata["name"])
        return tool_name
    

    def retrieve_tool_description(self, tool_name):
        """
        Returns the descriptions of specified tools based on their names.

        This method iterates over a list of tool names and retrieves the description
        for each tool from the generated_tools dictionary. It compiles and returns
        a list of these descriptions.

        Args:
            tool_name (list[str]): A list of tool names for which descriptions are requested.

        Returns:
            list[str]: A list containing the descriptions of the specified tools.
        """
        tool_description = []
        for name in tool_name:
            tool_description.append(self.generated_tools[name]["description"])
        return tool_description    


    def retrieve_tool_code(self, tool_name):
        """
        Returns the code of specified tools based on their names.

        Similar to retrieving tool descriptions, this method iterates over a list
        of tool names and retrieves the code for each tool from the generated_tools
        dictionary. It then compiles and returns a list of these codes.

        Args:
            tool_name (list[str]): A list of tool names for which code snippets are requested.

        Returns:
            list[str]: A list containing the code of the specified tools.
        """
        tool_code = []
        for name in tool_name:
            tool_code.append(self.generated_tools[name]["code"])
        return tool_code


    def delete_tool(self, tool):
        """
        Deletes all information related to a specified tool from the tool manager.

        This method removes the tool's information from the vector database, the
        generated_tools.json file, and also deletes the tool's code and description
        files from the repository. It performs the deletion only if the tool exists
        in the respective storage locations and provides console feedback for each
        successful deletion action.

        Args:
            tool (str): The name of the tool to be deleted.

        Note:
            This method assumes that the tool's information is stored in a structured
            manner within the tool manager's repository, including a separate code file
            (.py), a description text file (.txt), and an arguments description text file
            (.txt), all named after the tool.
        """
        if tool in self.generated_tools:
            self.vectordb._collection.delete(ids=[tool])
            print(
            f"\033[33m delete {tool} from vectordb successfully! \033[0m"
            )              
        # Delete the task from generated_tools.json
        with open(f"{self.generated_tool_repo_dir}/generated_tools.json", "r") as file:
            tool_infos = json.load(file)
        if tool in tool_infos:
            del tool_infos[tool]
        with open(f"{self.generated_tool_repo_dir}/generated_tools.json", "w") as file:
            json.dump(tool_infos, file, indent=4)
            print(
            f"\033[33m delete {tool} info from JSON successfully! \033[0m"
            )            
        # del code
        code_path = f"{self.generated_tool_repo_dir}/tool_code/{tool}.py"
        if os.path.exists(code_path):
            os.remove(code_path)
            print(
            f"\033[33m delete {tool} code successfully! \033[0m"
            )
        # del description
        description_path = f"{self.generated_tool_repo_dir}/tool_description/{tool}.txt"
        if os.path.exists(description_path):
            os.remove(description_path)
            print(
            f"\033[33m delete {tool} description txt successfully! \033[0m"
            )   
        # del args description
        # args_path = f"{self.generated_tool_repo_dir}/args_description/{tool}.txt"
        # if os.path.exists(args_path):
        #     os.remove(args_path)
        #     print(
        #     f"\033[33m delete {tool} args description txt successfully! \033[0m"
        #     )                
    

def print_error_and_exit(message):
    """
    Prints an error message to standard output and exits the program with a status code of 1.

    This function is typically used to handle critical errors from which the program cannot
    recover. It ensures that the error message is visible to the user before the program
    terminates.

    Args:
        message (str): The error message to be printed.
    """
    print(f"Error: {message}")
    sys.exit(1)


def add_tool(toolManager, tool_name, tool_path):
    """
    Adds a new tool to the tool manager with the given name and code loaded from the specified path.

    This function reads the tool's code from a file, extracts a description from the code using
    a predefined pattern, and then adds the tool to the tool manager using the extracted information.
    If the tool's description is not found within the code, the function will print an error message
    and exit.

    Args:
        toolManager (ToolManager): The instance of ToolManager to which the tool will be added.
        tool_name (str): The name of the tool to be added.
        tool_path (str): The file system path to the source code of the tool.

    Note:
        The function expects the tool's code to contain a description defined as a string literal
        assigned to `self._description` within the code. The description must be enclosed in double
        quotes for it to be successfully extracted.
    """
    with open(tool_path, 'r') as file:
        code = file.read()
    
    pattern = r'"""\s*\n\s*(.*?)[\.\n]'
    match = re.search(pattern, code)
    if match:
        description = match.group(1)
        # print(description)
        # print(type(description))
        info = {
            "task_name" : tool_name,
            "code" : code,
            "description" : description
        }
        toolManager.add_new_tool(info)
        print(f"Successfully add the tool: {tool_name} with path: {tool_path}")
    else:
        print_error_and_exit("No description found")


def delete_tool(toolManager, tool_name):
    """
    Deletes a tool from the tool manager and prints a success message.

    This function calls the `delete_tool` method of the given ToolManager instance
    to remove the specified tool. Upon successful deletion, it prints a message
    indicating the operation was successful.

    Args:
        toolManager (ToolManager): An instance of the ToolManager class.
        tool_name (str): The name of the tool to be deleted.
    """
    toolManager.delete_tool(tool_name)
    print(f"Successfully Delete the tool: {tool_name}")


def get_open_api_doc_path():
    """
    Determines the file system path to the 'openapi.json' file located in the same directory as this script.

    Returns:
        str: The absolute path to the 'openapi.json' file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    open_api_path = os.path.join(script_dir, 'openapi.json')
    return open_api_path


def get_open_api_description_pair():
    """
    Extracts and returns a mapping of OpenAPI path names to their descriptions.

    This function loads the OpenAPI specification from a 'openapi.json' file located
    in the same directory as this script. It then iterates over the paths defined
    in the OpenAPI specification, creating a dictionary that maps each path name
    to its description (summary). If a path supports both 'get' and 'post' operations,
    the description for the 'post' operation is preferred.

    Returns:
        dict: A dictionary mapping OpenAPI path names to their summary descriptions.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    open_api_path = os.path.join(script_dir, 'openapi.json')
    with open(open_api_path, 'r') as file:
        open_api_json = json.load(file)
    open_api_dict = open_api_json['paths']
    open_api_description_pair = {}
    for name, value in open_api_dict.items():
        if 'post' in value:
            open_api_description_pair[name] = value['post']['summary']
        else:
            open_api_description_pair[name] = value['get']['summary']
    return open_api_description_pair


def main():
    """
    The main entry point for managing generated tools for the FRIDAY project.

    This function sets up a command-line interface for adding or deleting tools
    within the FRIDAY project. It supports flags for adding a new tool, deleting
    an existing tool, and specifies the name and path of the tool for the
    respective operations. Based on the arguments provided, it initializes
    a ToolManager instance and performs the requested add or delete operation.

    The '--add' flag requires the '--tool_name' and '--tool_path' arguments to
    specify the name and the path of the tool to be added. The '--delete' flag
    requires only the '--tool_name' argument.

    Usage:
        python script.py --add --tool_name <name> --tool_path <path>
        python script.py --delete --tool_name <name>

    Raises:
        SystemExit: If no operation type is specified or required arguments are missing,
                    the program will print an error message and exit with a status code of 1.
    """
    parser = argparse.ArgumentParser(description='Manage generated tools for FRIDAY')
    
    parser.add_argument('--generated_tool_repo_path', type=str, default='oscopilot/tool_repository/generated_tools', help='generated tool repo path')

    parser.add_argument('--add', action='store_true',
                        help='Flag to add a new tool')
    parser.add_argument('--delete', action='store_true',
                        help='Flag to delete a tool')
    parser.add_argument('--tool_name', type=str,
                        help='Name of the tool to be added or deleted')
    parser.add_argument('--tool_path', type=str,
                        help='Path of the tool to be added', required='--add' in sys.argv)

    args = parser.parse_args()

    toolManager = ToolManager(generated_tool_repo_dir=args.generated_tool_repo_path)

    if args.add:
        add_tool(toolManager, args.tool_name, args.tool_path)
    elif args.delete:
        delete_tool(toolManager, args.tool_name)
    else:
        print_error_and_exit("Please specify an operation type (add or del)")


if __name__ == "__main__":
    main()

    # Retrieval
    # res = toolManager.retrieve_tool_name("Open the specified text file in the specified folder using the default text viewer on Ubuntu.")
    # print(res[0])

    # Delete
    # toolManager = ToolManager(generated_tool_repo_dir='oscopilot/tool_repository/generated_tools')
    # toolManager.delete_tool("implement_loop_progress")

    # Add
    # code = ''
    # with open("temp.py", 'r') as file:
    #     code = file.read()
    # info = {
    #     "task_name" : "XXX",
    #     "code" : code,
    #     "description" : "XXX"
    # }
    # toolManager.add_new_tool(info)
