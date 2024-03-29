Deploying API Services
=================================

This tutorial guides you through deploying API services that FRIDAY can utilize to enhance its functionality. We provide several API tools, including audio2text, bing search, image search, web_loader, image_caption, and wolfram_alpha, all located within `oscopilot/tool_repository/api_tools`.

Configuring the Environment
----------------------------

1. **.env File Configuration**:

   Your `.env` file contains essential configurations for the API services. The following variables must be set:

   - ``MODEL_NAME``: Should already be set during the installation process. Example: ``"gpt-4-0125-preview"``.
   - ``OPENAI_API_KEY`` and ``OPENAI_ORGANIZATION``: Also set during installation.
   - ``API_BASE_URL``: The deployment address of the API service. For local deployment, use ``"http://127.0.0.1:8079"``.
   - ``BING_SUBSCRIPTION_KEY`` and ``BING_SEARCH_URL``: Required for using bing search-related services. Example URL: ``"https://api.bing.microsoft.com/v7.0/search"``.
   - ``WOLFRAMALPHA_APP_ID``: Necessary if you intend to use the wolfram_alpha tool.

   Fill these in accordingly based on the services you plan to use.

Configuring API Tools
---------------------

2. **Selecting Required API Tools**:

   In the `oscopilot/tool_repository/manager/api_server.py` file, you will configure which API tools FRIDAY will utilize. This is done by setting up the `services` and `server_list` variables.

   - The ``services`` dictionary includes all available API tools that FRIDAY can use. Each key represents the service name, and the value is the corresponding router object.

   - The ``server_list`` array specifies which of these services you wish to activate for the current deployment. This allows for flexible configuration depending on the needs of your specific environment or application.

   Here is how you can specify your configuration:

   .. code-block:: python

      services = {
          "bing": bing_router,  # bing_search, image_search, and web_loader
          "audio2text": audio2text_router,
          "image_caption": image_caption_router,
          "wolfram_alpha": wolfram_alpha_router
      }

      server_list = ["bing"]

   In this example, we have included several services in the ``services`` dictionary, making them available for FRIDAY. However, by placing only "bing" in the ``server_list``, we are specifically activating the Bing services for use, including bing_search, image_search and web_loader. This demonstrates how to selectively enable certain API tools based on your requirements.


Launching the API Server
------------------------

3. **Starting the Service**:

   To start the API service, run the following command:

   .. code-block:: shell

      python oscopilot/tool_repository/manager/api_server.py

   Successful startup messages will look like this:

   .. code-block:: text

      INFO:     Started server process [17709]
      INFO:     Waiting for application startup.
      INFO:     Application startup complete.
      INFO:     Uvicorn running on http://0.0.0.0:8079 (Press CTRL+C to quit)
      Incoming request: GET http://127.0.0.1:8079/tools/bing/searchv2
      Outgoing response: 200
      INFO:     127.0.0.1:52324 - "GET /tools/bing/searchv2 HTTP/1.1" 200 OK

Updating API Documentation
--------------------------

4. **Update the OpenAPI Documentation**:

   After the service is running, navigate to `http://localhost:8079/openapi.json` in your web browser. This URL hosts the auto-generated OpenAPI documentation for your API services. (Remember to replace the IP address if your service is not deployed locally.)

   Here is an example of what the OpenAPI documentation might look like:

   .. image:: /_static/demo_openapi.png
      :align: center
      :width: 100%
      :alt: Example of OpenAPI Documentation

   Copy the content displayed at this URL to the `oscopilot/tool_repository/manager/openapi.json` file in your project directory. This step ensures that FRIDAY's API server has the latest documentation regarding the available API services.

Testing the API Tools
---------------------

5. **Verifying Functionality**:

   Test the deployed API tools by running a sample query with `run.py`. For example:

   .. code-block:: shell

      python quick_start.py --query 'Search the information of OpenAI'

   If everything is configured correctly, FRIDAY should utilize the deployed API services to complete the task.

Conclusion
----------

You have successfully deployed API services for FRIDAY, enhancing its capabilities with additional tools. By following these steps, you can integrate a wide range of functionalities into FRIDAY, making it an even more powerful assistant.
