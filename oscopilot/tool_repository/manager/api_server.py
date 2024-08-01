import os
import dotenv

from fastapi import FastAPI
from oscopilot.utils.server_config import ConfigManager
dotenv.load_dotenv(dotenv_path='.env', override=True)
app = FastAPI()

# Import your services
from oscopilot.tool_repository.api_tools.bing.bing_service import router as bing_router
from oscopilot.tool_repository.api_tools.audio2text.audio2text_service import router as audio2text_router
from oscopilot.tool_repository.api_tools.image_caption.image_caption_service import router as image_caption_router
from oscopilot.tool_repository.api_tools.wolfram_alpha.wolfram_alpha import router as wolfram_alpha_router

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Incoming request: {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Request error: {str(e)}")
            raise e from None
        else:
            print(f"Outgoing response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

# Create a dictionary that maps service names to their routers
services = {
    "bing": bing_router, # bing_search, image_search and web_loader
    "autio2text": audio2text_router,
    "image_caption": image_caption_router,
    "wolfram_alpha": wolfram_alpha_router
}

server_list = ["bing", "autio2text", "image_caption"]

# Include only the routers for the services listed in server_list
for service in server_list:
    if service in services:
        app.include_router(services[service])

# proxy_manager = ConfigManager()
# proxy_manager.apply_proxies()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8079)
