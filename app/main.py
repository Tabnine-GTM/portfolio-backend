from fastapi import FastAPI
import uvicorn
from app.routers import auth, portfolio
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(portfolio.router, tags=["portfolio"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Portfolio Management API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
