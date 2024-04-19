"""cpeq-infolettre-automatique REST API."""

import logging

import coloredlogs
from decouple import config
from fastapi import FastAPI
from fastapi.responses import JSONResponse


webscraper_io_api_token = config("WEBSCRAPER_IO_API_KEY", default="")

app = FastAPI()


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()


@app.get("/")
def read_root() -> str:
    """Read root."""
    return "Hello world"


@app.get("/get-articles")
def get_articles_from_scraper() -> str:
    """Read root."""
    # Appeler l'API de webscraper.io, appeler SharePoint, enlever les doublons, et retourner les articles en json
    return JSONResponse(content={"articles": []})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=str(config("DEVLOCAL_HOST", "localhost")),
        port=int(config("DEVLOCAL_PORT", 8001)),
    )
