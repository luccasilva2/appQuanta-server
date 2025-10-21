from fastapi import APIRouter, HTTPException, Depends
from models.app import AppCreateRequest, AppUpdateRequest, AppResponse
from services.firebase_service import FirebaseService
from routes.auth import get_current_user
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/apps", response_model=dict)
async def get_user_apps(user_id: str = Depends(get_current_user)):
    try:
        apps = FirebaseService.get_user_apps(user_id)
        return {
            "success": True,
            "message": "Apps retrieved successfully.",
            "data": [app.dict() for app in apps]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve apps: {str(e)}")

@router.post("/apps/create", response_model=dict)
async def create_app(app_data: AppCreateRequest, user_id: str = Depends(get_current_user)):
    try:
        new_app = FirebaseService.create_app(user_id, app_data)
        return {
            "success": True,
            "message": "App created successfully.",
            "data": new_app.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create app: {str(e)}")

@router.put("/apps/{app_id}", response_model=dict)
async def update_app(app_id: str, app_data: AppUpdateRequest, user_id: str = Depends(get_current_user)):
    try:
        updated_app = FirebaseService.update_app(app_id, user_id, app_data)
        if not updated_app:
            raise HTTPException(status_code=404, detail="App not found or access denied")
        return {
            "success": True,
            "message": "App updated successfully.",
            "data": updated_app.dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update app: {str(e)}")

@router.delete("/apps/{app_id}", response_model=dict)
async def delete_app(app_id: str, user_id: str = Depends(get_current_user)):
    try:
        success = FirebaseService.delete_app(app_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="App not found or access denied")
        return {
            "success": True,
            "message": "App deleted successfully.",
            "data": None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete app: {str(e)}")
