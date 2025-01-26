from fastapi import FastAPI, Depends
import uvicorn
from app.routers import auth, portfolio
from app.security import manager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React default port
    "http://localhost:5000",  # Another common frontend port
    "http://localhost:5173",
    # Add any other origins (frontend URLs) you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, tags=["auth"])
app.include_router(portfolio.router, tags=["portfolio"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Portfolio Management API"}


@app.get("/protected")
def protected_route(user=Depends(manager)):
    return {"message": f"Hello, {user.username}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
