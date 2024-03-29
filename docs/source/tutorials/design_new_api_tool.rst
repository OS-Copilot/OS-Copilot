Designing New API Tools
==================================

After deploying existing API services as described in the previous section, this part will focus on how to develop and deploy a new API service for FRIDAY. By creating custom API tools, you can extend FRIDAY's capabilities to suit your specific needs.

Creating a New API Tool
-----------------------

1. **Setting Up the API Tool**:

   Begin by creating a new folder for your API tool within `oscopilot/tool_repository/api_tools`. Inside this folder, create your tool file and write the API tool code. You can refer to the FastAPI documentation (https://fastapi.tiangolo.com/reference/fastapi/) and examples in the `oscopilot/tool_repository/api_tools` directory for guidance on coding your API tool.

   Consider the following example when designing your API endpoint:

   .. code-block:: python

      @router.get("/tools/bing/searchv2", summary="Execute Bing Search - returns top web snippets related to the query. Avoid using complex filters like 'site:'. For detailed page content, further use the web browser tool.")
      async def bing_search_v2(item: QueryItemV2):
          try:
              if item.top_k == None:
                  item.top_k = 5
              search_results = bing_api_v2.search(item.query, item.top_k)
          except RuntimeError as e:
              raise HTTPException(status_code=500, detail=str(e))
          return search_results

   Ensure to include the `summary` parameter in `router.get`, providing a detailed description of the API tool's functionality, which FRIDAY will use to determine the tool's applicability for tasks.

Integrating the API Tool
------------------------

2. **Registering the New API Tool**:

   Update `oscopilot/tool_repository/manager/api_server.py` with the new API tool's information. Add import statements and update the `services` and `server_list` accordingly.

   Example code snippet:

   .. code-block:: python

      from oscopilot.tool_repository.api_tools.new_api.new_api_service import router as new_api_router
      
      services = {
          "bing": bing_router,  # bing_search, image_search, and web_loader
          "audio2text": audio2text_router,
          "image_caption": image_caption_router,
          "wolfram_alpha": wolfram_alpha_router,
          "new_api": new_api_router
      }
      
      server_list = ["bing", "new_api"]

Launching the Service
---------------------

3. **Starting the API Service**:

   Run the `api_server.py` file to launch the service:

   .. code-block:: shell

      python oscopilot/tool_repository/manager/api_server.py

   Successful launch messages should resemble the following:

   .. code-block:: text

      INFO:     Started server process [17709]
      INFO:     Waiting for application startup.
      INFO:     Application startup complete.
      INFO:     Uvicorn running on http://0.0.0.0:8079 (Press CTRL+C to quit)

Updating OpenAPI Documentation
-------------------------------

4. **Updating API Documentation**:

   Navigate to `http://localhost:8079/openapi.json` (adjust the IP if necessary) and overwrite the content in `oscopilot/tool_repository/manager/openapi.json` with the content from this URL.

Verifying the API Tool
----------------------

5. **Testing the API Tool**:

   Verify the new API tool's functionality by executing a test query with `run.py`:

   .. code-block:: shell

      python quick_start.py --query 'Your test query here'

Conclusion
----------

By following these steps, you have successfully designed, integrated, and deployed a new API tool for FRIDAY. This customization allows FRIDAY to perform tasks tailored to your specific requirements, enhancing its overall utility.

