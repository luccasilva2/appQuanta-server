import os
from supabase import create_client, Client
from datetime import datetime
from typing import Optional, List
from models.app import AppResponse, AppCreateRequest, AppUpdateRequest

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_anon_key or not supabase_service_role_key:
    print("Warning: Supabase environment variables are not set. Skipping Supabase initialization for testing.")
    supabase: Optional[Client] = None
    supabase_auth: Optional[Client] = None
else:
    try:
        supabase = create_client(supabase_url, supabase_service_role_key)  # For DB operations
        supabase_auth = create_client(supabase_url, supabase_anon_key)  # For auth verification
        print("Supabase clients initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
        supabase = None
        supabase_auth = None

class SupabaseService:
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        if not supabase_auth:
            print("Supabase auth not initialized - returning test user for development")
            return "test_user_id"  # Return a test user ID for development
        try:
            response = supabase_auth.auth.get_user(token)
            return response.user.id if response.user else None
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None

    @staticmethod
    def get_user_apps(user_id: str) -> List[AppResponse]:
        if not supabase:
            print("Supabase not initialized - returning mock apps for development")
            # Return some mock apps for development
            from models.app import AppResponse
            import uuid
            from datetime import datetime
            mock_apps = [
                AppResponse(
                    id=str(uuid.uuid4()),
                    name="Mock App 1",
                    description="First mock app",
                    status="active",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    user_id=user_id,
                    apk_url=None
                ),
                AppResponse(
                    id=str(uuid.uuid4()),
                    name="Mock App 2",
                    description="Second mock app",
                    status="active",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    user_id=user_id,
                    apk_url=None
                )
            ]
            return mock_apps

        try:
            response = supabase.table('apps').select('*').eq('user_id', user_id).execute()
            apps = []
            for item in response.data:
                app = AppResponse(**item)
                apps.append(app)
            return apps
        except Exception as e:
            print(f"Failed to get user apps: {e}")
            return []

    @staticmethod
    def get_app(app_id: str, user_id: str) -> Optional[AppResponse]:
        if not supabase:
            return None
        try:
            response = supabase.table('apps').select('*').eq('id', app_id).eq('user_id', user_id).execute()
            if response.data:
                return AppResponse(**response.data[0])
            return None
        except Exception as e:
            print(f"Failed to get app: {e}")
            return None

    @staticmethod
    def create_app(user_id: str, app_data: AppCreateRequest) -> AppResponse:
        if not supabase:
            print("Supabase not initialized - creating mock app for development")
            # Create a mock response for development
            import uuid
            now = datetime.utcnow().isoformat()
            mock_app = {
                'id': str(uuid.uuid4()),
                'name': app_data.name,
                'description': app_data.description,
                'status': app_data.status,
                'created_at': now,
                'updated_at': now,
                'user_id': user_id,
                'apk_url': None
            }
            return AppResponse(**mock_app)

        now = datetime.utcnow().isoformat()
        app_dict = {
            'name': app_data.name,
            'description': app_data.description,
            'status': app_data.status,
            'created_at': now,
            'updated_at': now,
            'user_id': user_id,
            'apk_url': None
        }
        try:
            response = supabase.table('apps').insert(app_dict).execute()
            if response.data:
                return AppResponse(**response.data[0])
            else:
                raise Exception("Failed to create app")
        except Exception as e:
            print(f"Failed to create app: {e}")
            raise

    @staticmethod
    def update_app(app_id: str, user_id: str, app_data: AppUpdateRequest) -> Optional[AppResponse]:
        if not supabase:
            raise Exception("Supabase not initialized")
        try:
            # First check if app exists and belongs to user
            existing = SupabaseService.get_app(app_id, user_id)
            if not existing:
                return None

            update_data = {k: v for k, v in app_data.dict().items() if v is not None}
            update_data['updated_at'] = datetime.utcnow().isoformat()

            response = supabase.table('apps').update(update_data).eq('id', app_id).eq('user_id', user_id).execute()
            if response.data:
                return AppResponse(**response.data[0])
            return None
        except Exception as e:
            print(f"Failed to update app: {e}")
            raise

    @staticmethod
    def upload_apk(app_id: str, file) -> str:
        if not supabase:
            raise Exception("Supabase not initialized")
        try:
            # Read file content
            file_content = file.file.read()
            file_name = f"{app_id}.apk"

            # Upload to Supabase Storage
            bucket_name = 'apks'  # Make sure this bucket exists in your Supabase project
            response = supabase.storage.from_(bucket_name).upload(
                path=file_name,
                file=file_content,
                file_options={"content-type": "application/vnd.android.package-archive"}
            )

            # Get public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
            return public_url
        except Exception as e:
            print(f"Failed to upload APK: {e}")
            raise

    @staticmethod
    def delete_app(app_id: str, user_id: str) -> bool:
        if not supabase:
            raise Exception("Supabase not initialized")
        try:
            # First check if app exists and belongs to user
            existing = SupabaseService.get_app(app_id, user_id)
            if not existing:
                return False

            response = supabase.table('apps').delete().eq('id', app_id).eq('user_id', user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Failed to delete app: {e}")
            raise
