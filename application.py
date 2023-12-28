import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


def start(http_port: int, log_level: str):
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=http_port,
        log_level=log_level,
    )
