from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"  # active, inactive, etc.
    icon: Optional[str] = None
    color: Optional[str] = None
    screens: Optional[list] = None
    type: Optional[str] = None

class AppUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class AppResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    icon: Optional[str] = None
    color: Optional[str] = None
    screens: Optional[list] = None
    type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_id: str
    apk_url: Optional[str] = None
