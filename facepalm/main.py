from fastapi import FastAPI

from facepalm.router.post import router as post_router

app =FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

app.include_router(post_router, prefix="/posts")