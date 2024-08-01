
# Using llama3 as llm at local server


### Deploy local api services using [ollama](#https://github.com/ollama/ollama/tree/main)


1. install ollama

   ```
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. start Ollama serve

   ```
   ollama serve 
   ```

3. Run or pull the model

   ```
   ollama run/pull llama3
   ```

### Test llama3 api services


```
python examples/LLAMA3/test_llama3.py
```


### Modify env to set the default model to llama3

```
MODEL_NAME="llama3"
MODEL_TYPE="OLLAMA"
MODEL_SERVER="http://localhost:11434"
EMBED_MODEL_TYPE="OLLAMA"
EMBED_MODEL_NAME="nomic-embed-text"
```

If the api cannot be linked in the script, run the following command to resolve the problem
```
export NO_PROXY=localhost,127.0.0.1 
```

#### Test_script

```
python quick_start.py
```