import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from typing import Optional, Dict, Any
from models.user import UserResponse
from models.app import AppResponse, AppCreateRequest, AppUpdateRequest

# Initialize Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token",
})

firebase_admin.initialize_app(cred)
db = firestore.client()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

class FirebaseService:
    @staticmethod
    def create_user(email: str, password: str, display_name: Optional[str] = None) -> UserResponse:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name
        )

    @staticmethod
    def verify_user(email: str, password: str) -> Optional[UserResponse]:
        try:
            user = auth.get_user_by_email(email)
            # Note: Firebase Admin SDK doesn't verify passwords directly
            # Password verification should be done on client-side with Firebase Auth SDK
            # For server-side, we'd need to use Firebase Auth REST API
            return UserResponse(
                uid=user.uid,
                email=user.email,
                display_name=user.display_name
            )
        except auth.UserNotFoundError:
            return None

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            uid: str = payload.get("sub")
            if uid is None:
                return None
            return uid
        except JWTError:
            return None

    @staticmethod
    def get_user_apps(user_id: str) -> list[AppResponse]:
        apps_ref = db.collection('apps').where('user_id', '==', user_id)
        apps = apps_ref.stream()
        return [FirebaseService._doc_to_app(doc) for doc in apps]

    @staticmethod
    def create_app(user_id: str, app_data: AppCreateRequest) -> AppResponse:
        now = datetime.utcnow()
        app_ref = db.collection('apps').document()
        app_dict = {
            'id': app_ref.id,
            'name': app_data.name,
            'description': app_data.description,
            'status': app_data.status,
            'created_at': now,
            'updated_at': now,
            'user_id': user_id
        }
        app_ref.set(app_dict)
        return AppResponse(**app_dict)

    @staticmethod
    def update_app(app_id: str, user_id: str, app_data: AppUpdateRequest) -> Optional[AppResponse]:
        app_ref = db.collection('apps').document(app_id)
        doc = app_ref.get()
        if not doc.exists or doc.to_dict()['user_id'] != user_id:
            return None

        update_data = {k: v for k, v in app_data.dict().items() if v is not None}
        update_data['updated_at'] = datetime.utcnow()
        app_ref.update(update_data)

        updated_doc = app_ref.get()
        return FirebaseService._doc_to_app(updated_doc)

    @staticmethod
    def delete_app(app_id: str, user_id: str) -> bool:
        app_ref = db.collection('apps').document(app_id)
        doc = app_ref.get()
        if not doc.exists or doc.to_dict()['user_id'] != user_id:
            return False
        app_ref.delete()
        return True

    @staticmethod
    def _doc_to_app(doc) -> AppResponse:
        data = doc.to_dict()
        return AppResponse(**data)
