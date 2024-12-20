"""
This module initializes the FastAPI application and configures middleware and routing.

The application includes CORS middleware for handling cross-origin requests and 
registers API endpoints related to books under the `/api/books` prefix.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import routers


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(routers.endPoints, prefix="/api/books")
