from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"  # active, inactive, etc.

class AppUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class AppResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    apk_url: Optional[str] = None
