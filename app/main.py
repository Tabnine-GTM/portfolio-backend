from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, portfolio

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
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(portfolio.router, tags=["portfolio"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Portfolio Management API"}