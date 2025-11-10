from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from models.app import AppCreateRequest, AppUpdateRequest, AppResponse
from services.supabase_service import SupabaseService
from typing import List

router = APIRouter()

def get_current_user(request: Request) -> str:
    user_id = getattr(request.state, 'user', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id

@router.get("/apps", response_model=dict)
async def get_user_apps(request: Request):
    user_id = get_current_user(request)
    try:
        print(f"Getting apps for user {user_id}")
        apps = SupabaseService.get_user_apps(user_id)
        print(f"Retrieved {len(apps)} apps")
        return {
            "success": True,
            "message": "Apps retrieved successfully.",
            "data": [app.dict() for app in apps]
        }
    except Exception as e:
        print(f"Error getting apps: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve apps: {str(e)}")

@router.get("/apps/{app_id}", response_model=dict)
async def get_app(app_id: str, request: Request):
    user_id = get_current_user(request)
    try:
        app = SupabaseService.get_app(app_id, user_id)
        if not app:
            raise HTTPException(status_code=404, detail="App not found or access denied")
        return {
            "success": True,
            "message": "App retrieved successfully.",
            "data": app.dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve app: {str(e)}")

@router.post("/apps/create", response_model=dict)
async def create_app(app_data: AppCreateRequest, request: Request):
    user_id = get_current_user(request)
    try:
        print(f"Creating app for user {user_id}: {app_data.dict()}")
        new_app = SupabaseService.create_app(user_id, app_data)
        print(f"App created successfully: {new_app.dict()}")
        return {
            "success": True,
            "message": "App created successfully.",
            "data": new_app.dict()
        }
    except Exception as e:
        print(f"Error creating app: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create app: {str(e)}")

@router.put("/apps/{app_id}", response_model=dict)
async def update_app(app_id: str, app_data: AppUpdateRequest, request: Request):
    user_id = get_current_user(request)
    try:
        updated_app = SupabaseService.update_app(app_id, user_id, app_data)
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

@router.post("/apps/{app_id}/upload-apk", response_model=dict)
async def upload_apk(app_id: str, file: UploadFile = File(...), request: Request = None):
    user_id = get_current_user(request)
    try:
        apk_url = SupabaseService.upload_apk(app_id, file)
        return {
            "success": True,
            "message": "APK uploaded successfully.",
            "data": {"apk_url": apk_url}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload APK: {str(e)}")

@router.delete("/apps/{app_id}", response_model=dict)
async def delete_app(app_id: str, request: Request):
    user_id = get_current_user(request)
    try:
        success = SupabaseService.delete_app(app_id, user_id)
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
