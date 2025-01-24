from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from app.crud.user import get_user_by_username, create_user
from app.database import get_db
from app.schemas.user import UserCreate, User
from app.security import verify_password, manager

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(form_data.username, db)

    if user is None:
        raise InvalidCredentialsException
    
    if not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": user.username})
    manager.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "Bearer"}

@router.post("/logout")
def logout(response: Response):
    manager.set_cookie(response, "")
    return {"message": "Logged out successfully"}

@router.post("/register")
def register(response: Response, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = create_user(db, user)

    # Generate access token
    access_token = manager.create_access_token(data={"sub": db_user.username})

    # Set the token in a cookie
    manager.set_cookie(response, access_token)

    return {
        "message": "User registered and logged in successfully",
        "user": db_user,
        "access_token": access_token,
        "token_type": "Bearer"
    }

@router.get("/user", response_model=User)
def get_current_user(user: User = Depends(manager)):
    return user