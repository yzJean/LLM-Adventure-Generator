from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import story, job
from db.database import create_tables

create_tables() # create tables in the database when the application starts. This ensures that the necessary tables are available for storing and retrieving data related to story generation jobs. By calling this function at the start of the application, we can ensure that the database schema is set up correctly before any operations are performed on it.

# API for backend
app = FastAPI(
    title="Choose Your Own Adventure API",
    description="api to generate cool stories",
    version="0.1.0", # version of the API
    docs_url="/docs", # FastAPI automatically generates interactive API documentation at this URL. We can view it on the web broweser
    redoc_url="/redoc", # FastAPI also provides an alternative documentation interface called ReDoc, which is available at this URL. ReDoc offers a different layout and style for the API documentation, and some developers prefer it over the default Swagger UI provided at /docs. By specifying both docs_url and redoc_url, we can provide users with the option to choose their preferred documentation interface when accessing the API documentation.
)

"""
For security reasons, we should specify the allowed origins, methods, and headers for CORS.
Origin: The domain (or URL) from which the services are running on, e.g., http://localhost:3000 for local development.
For example, frontend is making requests on localhost port 5173, but the backend is running on localhost port 8000. They won't allow to communicate with anything that is not on the same origin, so we need to allow requests from http://localhost:5173 by adding CORS (Cross Origin Resource Sharing) middleware to the FastAPI application. This will allow the frontend to make requests to the backend without any CORS issues. This is a security feature implemented by web browsers to prevent malicious websites from making unauthorized requests to other websites on behalf of the user. By configuring CORS, we can specify which origins are allowed to access our API, which HTTP methods are permitted, and which headers can be included in the requests. In this example, we are allowing all origins, methods, and headers for simplicity, but in a production environment, you should restrict these settings to enhance security.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, # allow all requests
    allow_credentials=True,
    allow_methods=["*"], # allow all HTTP methods (GET, POST, PUT etc.)
    allow_headers=["*"], # allow all headers which are additional information you can send with the request, e.g., Content-Type, Authorization etc.
)

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn # web server for running FastAPI applications
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # run the FastAPI application using Uvicorn ASGI server. The app will be accessible at http://localhost:8000. The reload=True option enables auto-reloading of the server when code changes are detected, which is useful during development.