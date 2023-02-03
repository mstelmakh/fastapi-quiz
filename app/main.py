import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import settings
from app.quiz.endpoints import router as quiz_router
from app.questions.endpoints import router as questions_router
from app.users.endpoints import router as users_router

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

app.include_router(quiz_router, prefix=settings.api_prefix)
app.include_router(questions_router, prefix=settings.api_prefix)
app.include_router(users_router)


@app.get('/')
def root():
    return {"message": "Hello"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True
    )
