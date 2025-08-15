# oscopilot/tool_repository/manager/tool_manager.py

import os
import sys
import re
import json
import argparse

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)

# --- Embeddings imports with compatibility for old/new LangChain layouts ---
try:
    # Old(er) LangChain (e.g., langchain==0.0.349)
    from langchain.embeddings.openai import OpenAIEmbeddings  # type: ignore
except Exception:
    # Newer split package
    from langchain_openai import OpenAIEmbeddings  # type: ignore

try:
    from langchain_community.embeddings import OllamaEmbeddings  # type: ignore
except Exception:
    OllamaEmbeddings = None  # Graceful fallback if community package not present

# Vector store
from langchain.vectorstores import Chroma  # type: ignore

# Optionally force pysqlite3 -> sqlite3 if needed for Chroma (leave commented unless required)
# __import__('pysqlite3')
# import sys as _sys
# _sys.modules['sqlite3'] = _sys.modules.pop('pysqlite3')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')

# Embedding selection via env (optional)
EMBED_MODEL_TYPE = os.getenv('MODEL_TYPE', '').strip()       # "OpenAI" or "OLLAMA"
EMBED_MODEL_NAME = os.getenv('MODEL_NAME', '').strip()       # e.g., "nomic-embed-text" for Ollama

def print_error_and_exit(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


class Tool_Manager:
    """
    Manages tools (code + description) and a Chroma vector DB for similarity lookup.
    Compatible with FridayAgent expectations.
    """

    def __init__(self, generated_tool_repo_path: str, embedding_function=None, *args, **kwargs):
        # Store path
        self.generated_tool_repo_dir = generated_tool_repo_path

        # Load or initialize tool registry
        generated_json_path = os.path.join(self.generated_tool_repo_dir, "generated_tools.json")
        if os.path.exists(generated_json_path):
            with open(generated_json_path, "r") as f:
                self.generated_tools = json.load(f)
        else:
            # Create a minimal, empty registry if missing
            os.makedirs(self.generated_tool_repo_dir, exist_ok=True)
            os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_code"), exist_ok=True)
            os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_description"), exist_ok=True)
            self.generated_tools = {}
            with open(generated_json_path, "w") as f:
                json.dump(self.generated_tools, f, indent=4)

        # Directories
        self.vectordb_path = os.path.join(self.generated_tool_repo_dir, "vectordb")
        os.makedirs(self.vectordb_path, exist_ok=True)
        os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_code"), exist_ok=True)
        os.makedirs(os.path.join(self.generated_tool_repo_dir, "tool_description"), exist_ok=True)

        # --- Embedding selection/fallbacks ---
        if embedding_function is None:
            if EMBED_MODEL_TYPE.upper() == "OLLAMA":
                if OllamaEmbeddings is None:
                    print("\033[33m[Tool_Manager] OllamaEmbeddings not available; falling back to OpenAIEmbeddings.\033[0m")
                    embedding_function = OpenAIEmbeddings(
                        openai_api_key=OPENAI_API_KEY,
                        openai_organization=OPENAI_ORGANIZATION,
                    )
                else:
                    model_name = EMBED_MODEL_NAME or "nomic-embed-text"
                    embedding_function = OllamaEmbeddings(model=model_name)
            else:
                # Default: OpenAI embeddings (works with both legacy and split packages)
                embedding_function = OpenAIEmbeddings(
                    openai_api_key=OPENAI_API_KEY,
                    openai_organization=OPENAI_ORGANIZATION,
                )

        # Initialize Chroma
        self.vectordb = Chroma(
            collection_name="tool_vectordb",
            embedding_function=embedding_function,
            persist_directory=self.vectordb_path,
        )

        # --- Ensure vector DB is in sync with generated_tools.json ---
        self._ensure_vectordb_synced()

    # ----- Internal helpers -----
    def _ensure_vectordb_synced(self):
        """Rebuilds vectordb from generated_tools if counts are off."""
        current_count = self.vectordb._collection.count()
        expected_count = len(self.generated_tools)
        if current_count != expected_count:
            print(
                f"\033[33m[Tool_Manager] Rebuilding vectordb "
                f"(found {current_count}, expected {expected_count}).\033[0m"
            )
            # Easiest rebuild: delete all then re-add
            if current_count:
                # Chroma Lite: no truncate; delete by ids we know
                all_ids = []
                for name in self.generated_tools.keys():
                    all_ids.append(name)
                # Try delete any possible residuals
                try:
                    self.vectordb._collection.delete(where={})  # wipe if supported
                except Exception:
                    # Fall back to delete by ids we know
                    try:
                        self.vectordb._collection.delete(ids=all_ids)
                    except Exception:
                        pass

            # Re-add everything
            if self.generated_tools:
                texts = []
                ids = []
                metas = []
                for name, entry in self.generated_tools.items():
                    texts.append(entry.get("description", ""))
                    ids.append(name)
                    metas.append({"name": name})
                self.vectordb.add_texts(texts=texts, ids=ids, metadatas=metas)
                self.vectordb.persist()

        # Final sanity check
        final_count = self.vectordb._collection.count()
        assert final_count == len(self.generated_tools), (
            "Tool Manager's vectordb is not synced with generated_tools.json.\n"
            f"There are {final_count} tools in vectordb but "
            f"{len(self.generated_tools)} tools in generated_tools.json.\n"
        )

    # ----- Public properties -----
    @property
    def programs(self) -> str:
        return "\n\n".join(entry["code"] for _, entry in self.generated_tools.items())

    @property
    def descriptions(self) -> dict:
        return {tool_name: entry["description"] for tool_name, entry in self.generated_tools.items()}

    @property
    def tool_names(self):
        return self.generated_tools.keys()

    # ----- CRUD -----
    def get_tool_code(self, tool_name: str) -> str:
        return self.generated_tools[tool_name]["code"]

    def add_new_tool(self, info: dict) -> None:
        program_name = info["task_name"]
        program_code = info["code"]
        program_description = info["description"]

        print(f"\033[33m {program_name}:\n{program_description}\033[0m")

        # If exists, delete then rewrite
        if program_name in self.generated_tools:
            print(f"\033[33mTool {program_name} already exists. Rewriting!\033[0m")
            try:
                self.vectordb._collection.delete(ids=[program_name])
            except Exception:
                pass

        # Add to vectordb & memory
        self.vectordb.add_texts(
            texts=[program_description],
            ids=[program_name],
            metadatas=[{"name": program_name}],
        )
        self.generated_tools[program_name] = {
            "code": program_code,
            "description": program_description,
        }

        # Persist files
        with open(os.path.join(self.generated_tool_repo_dir, "tool_code", f"{program_name}.py"), "w") as fa:
            fa.write(program_code)
        with open(os.path.join(self.generated_tool_repo_dir, "tool_description", f"{program_name}.txt"), "w") as fb:
            fb.write(program_description)
        with open(os.path.join(self.generated_tool_repo_dir, "generated_tools.json"), "w") as fc:
            json.dump(self.generated_tools, fc, indent=4)

        self.vectordb.persist()
        self._ensure_vectordb_synced()

    def exist_tool(self, tool: str) -> bool:
        return tool in self.tool_names

    def retrieve_tool_name(self, query: str, k: int = 10):
        k = min(self.vectordb._collection.count(), k)
        if k == 0:
            return []
        print(f"\033[33mTool Manager retrieving for {k} Tools\033[0m")
        docs_and_scores = self.vectordb.similarity_search_with_score(query, k=k)
        print(
            f"\033[33mTool Manager retrieved tools: "
            f"{', '.join([doc.metadata['name'] for doc, _ in docs_and_scores])}\033[0m"
        )
        return [doc.metadata["name"] for doc, _ in docs_and_scores]

    def retrieve_tool_description(self, tool_name_list):
        return [self.generated_tools[name]["description"] for name in tool_name_list]

    def retrieve_tool_code(self, tool_name_list):
        return [self.generated_tools[name]["code"] for name in tool_name_list]

    def delete_tool(self, tool: str) -> None:
        # vectordb
        try:
            self.vectordb._collection.delete(ids=[tool])
            print(f"\033[33m delete {tool} from vectordb successfully! \033[0m")
        except Exception:
            pass

        # JSON
        generated_json_path = os.path.join(self.generated_tool_repo_dir, "generated_tools.json")
        if os.path.exists(generated_json_path):
            with open(generated_json_path, "r") as file:
                tool_infos = json.load(file)
            if tool in tool_infos:
                del tool_infos[tool]
                with open(generated_json_path, "w") as file:
                    json.dump(tool_infos, file, indent=4)
                self.generated_tools = tool_infos
                print(f"\033[33m delete {tool} info from JSON successfully! \033[0m")

        # code + description files
        code_path = os.path.join(self.generated_tool_repo_dir, "tool_code", f"{tool}.py")
        if os.path.exists(code_path):
            os.remove(code_path)
            print(f"\033[33m delete {tool} code successfully! \033[0m")

        description_path = os.path.join(self.generated_tool_repo_dir, "tool_description", f"{tool}.txt")
        if os.path.exists(description_path):
            os.remove(description_path)
            print(f"\033[33m delete {tool} description txt successfully! \033[0m")

        self.vectordb.persist()
        self._ensure_vectordb_synced()


# Backward-compat alias (some modules import ToolManager)
class ToolManager(Tool_Manager):
    pass


def add_tool(toolManager: Tool_Manager, tool_name: str, tool_path: str) -> None:
    with open(tool_path, 'r') as file:
        code = file.read()

    pattern = r'"""\s*\n\s*(.*?)[\.\n]'
    match = re.search(pattern, code)
    if match:
        description = match.group(1)
        info = {
            "task_name": tool_name,
            "code": code,
            "description": description
        }
        toolManager.add_new_tool(info)
        print(f"Successfully add the tool: {tool_name} with path: {tool_path}")
    else:
        print_error_and_exit("No description found")


def delete_tool(toolManager: Tool_Manager, tool_name: str) -> None:
    toolManager.delete_tool(tool_name)
    print(f"Successfully Delete the tool: {tool_name}")


def get_open_api_doc_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'openapi.json')


def get_open_api_description_pair() -> dict:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    open_api_path = os.path.join(script_dir, 'openapi.json')
    with open(open_api_path, 'r') as file:
        open_api_json = json.load(file)
    open_api_dict = open_api_json['paths']
    out = {}
    for name, value in open_api_dict.items():
        if 'post' in value:
            out[name] = value['post']['summary']
        else:
            out[name] = value['get']['summary']
    return out


def main():
    parser = argparse.ArgumentParser(description='Manage generated tools for FRIDAY')
    parser.add_argument('--generated_tool_repo_path', type=str,
                        default='oscopilot/tool_repository/generated_tools',
                        help='generated tool repo path')

    parser.add_argument('--add', action='store_true', help='Flag to add a new tool')
    parser.add_argument('--delete', action='store_true', help='Flag to delete a tool')
    parser.add_argument('--tool_name', type=str, help='Name of the tool to be added or deleted')
    parser.add_argument('--tool_path', type=str, help='Path of the tool to be added',
                        required='--add' in sys.argv)

    args = parser.parse_args()

    toolManager = Tool_Manager(generated_tool_repo_path=args.generated_tool_repo_path)

    if args.add:
        add_tool(toolManager, args.tool_name, args.tool_path)
    elif args.delete:
        delete_tool(toolManager, args.tool_name)
    else:
        print_error_and_exit("Please specify an operation type (add or del)")


if __name__ == "__main__":
    main()
