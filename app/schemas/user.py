from pydantic import BaseModel, ConfigDict, EmailStr

# Define the ConfigDict once
common_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = common_config


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserInDB(User):
    hashed_password: str
