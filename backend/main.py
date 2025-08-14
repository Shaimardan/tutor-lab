import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from logging_setup import logging_setting
from src.routes.api import api_router, tags_metadata
from src.routes.errors import base_http_exception_handler


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncIterator[None]:
    logging.info("Start Tutor Lab")
    yield
    logging.info("Stop Tutro Lab")


app = FastAPI(
    title="tutor-lab",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.openapi_tags = tags_metadata
app.add_exception_handler(HTTPException, base_http_exception_handler)
logging_setting()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None, reload=False)
