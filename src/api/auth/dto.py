from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    organization_name: str


class RegisterResponse(BaseModel):
    user_id: int


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    access_token_expires_at: int
    refresh_token: str
    refresh_token_expire_at: int
