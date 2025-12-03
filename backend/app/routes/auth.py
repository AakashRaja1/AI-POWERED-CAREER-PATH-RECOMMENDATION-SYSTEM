from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None
    token: Optional[str] = None


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Simple admin login endpoint
    """
    admin_email = os.getenv("ADMIN_EMAIL", "admin@careerpath.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    if request.email == admin_email and request.password == admin_password:
        return LoginResponse(
            success=True,
            message="Login successful",
            user={
                "email": admin_email,
                "role": "admin",
                "name": "Admin"
            },
            token="admin_token_" + admin_email
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.post("/logout")
async def logout():
    """
    Logout endpoint
    """
    return {"success": True, "message": "Logged out successfully"}
