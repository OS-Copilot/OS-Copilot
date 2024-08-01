# FRIDAY Front

## Usage

Suppose `cwd` to be the root path of OS-Copilot project. To run front-end application, execute either set of the following instructions:

1. For developers, make sure Node.js (as well as npm) is installed:

    ```shell
    cd front/
    npm install
    npm start
    ```

2. For deployer, also make sure Node.js (as well as npm) is installed:

    ```shell
    cd front/
    npm install
    npm run build
    cp .env.dist dist/.env
    ```

## .env Config

- `REACT_APP_PATH` (**required**): absolute/relative path of backend directory;
- `REACT_APP_CONDA` (optional): conda environment name if exists;
- `REACT_APP_PROXY` (optional): proxy URL used when executing python scripts, needed if remote LLM service is censored and blocked;
- `REACT_APP_MIRROR` (optional): mirror site of Hugging Face.

## Prompts Examples

- Copy any text file located in the working_dir/document directory that contains the word 'agent' to a new folder named 'agents'.
