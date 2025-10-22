from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.auth import router as auth_router
from routes.apps import router as apps_router
from middleware.auth_middleware import AuthMiddleware
import os
from dotenv import load_dotenv

# Load .env file only if it exists and is readable
try:
    if os.path.exists('.env'):
        load_dotenv(encoding='utf-8')
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

app = FastAPI(
    title="AppQuanta API",
    description="Backend API for AppQuanta application management with Supabase",
    version="1.0.0"
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(apps_router, prefix="/api/v1", tags=["Apps"])

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "data": None
        }
    )

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "AppQuanta API with Supabase is running.",
        "data": None
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
