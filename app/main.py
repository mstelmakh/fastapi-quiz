import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import settings

app = FastAPI(
    title=settings.title
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0"
    )
