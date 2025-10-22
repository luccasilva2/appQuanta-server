from fastapi import APIRouter

router = APIRouter()

# Authentication is handled client-side with Supabase Auth
# No server-side register/login routes needed
# Users authenticate via Supabase SDK in the Flutter app
