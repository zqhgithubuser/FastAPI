import logging
from os import getpid

from fastapi import FastAPI

logger = logging.getLogger("uvicorn")
app = FastAPI(title="FastAPI Live Application")


@app.get("/")
def read_root():
    logger.info(f"Processd by worker {getpid()}")
    return {"Hello": "World"}
