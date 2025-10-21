from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserRegisterRequest, UserLoginRequest, TokenResponse
from services.firebase_service import FirebaseService
from typing import Optional

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=dict)
async def register_user(user: UserRegisterRequest):
    try:
        new_user = FirebaseService.create_user(
            email=user.email,
            password=user.password,
            display_name=user.display_name
        )
        return {
            "success": True,
            "message": "User registered successfully.",
            "data": new_user.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=dict)
async def login_user(user: UserLoginRequest):
    try:
        db_user = FirebaseService.verify_user(user.email, user.password)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = FirebaseService.create_access_token(data={"sub": db_user.uid})
        return {
            "success": True,
            "message": "Login successful.",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": db_user.dict()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    user_id = FirebaseService.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user_id
