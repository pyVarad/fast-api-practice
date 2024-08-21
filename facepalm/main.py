from contextlib import asynccontextmanager

from fastapi import FastAPI

from facepalm.database import database
from facepalm.logging_config import configure_logging
from facepalm.router.post import router as post_router

# logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    # logger.info("Hello World")
    await database.connect()
    yield
    await database.disconnect()

app =FastAPI(lifespan=lifespan)
app.include_router(post_router, prefix="/posts")