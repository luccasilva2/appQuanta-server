# TODO List for AppQuanta FastAPI Backend

## Step 1: Create main.py ✅
- Set up FastAPI app instance ✅
- Include CORS middleware ✅
- Register routes ✅
- Add JWT middleware for protected routes ✅
- Global error handling ✅

## Step 2: Create routes/auth.py ✅
- Implement /register endpoint (POST) ✅
- Implement /login endpoint (POST) ✅
- Use Firebase Auth for registration and login ✅
- Return JWT token on successful login ✅

## Step 3: Create routes/apps.py ✅
- Implement /apps endpoint (GET) - list user's apps ✅
- Implement /apps/create endpoint (POST) - create new app ✅
- Implement /apps/{id} endpoint (PUT) - update app ✅
- Implement /apps/{id} endpoint (DELETE) - delete app ✅
- Use JWT authentication for all these endpoints ✅
- Interact with Firestore for data operations ✅

## Step 4: Create models/user.py ✅
- Define Pydantic models for user registration/login requests and responses ✅

## Step 5: Create models/app.py ✅
- Define Pydantic models for app data (create, update, response) ✅

## Step 6: Create services/firebase_service.py ✅
- Initialize Firebase Admin SDK ✅
- Functions for user authentication (register, login) ✅
- Functions for Firestore operations (CRUD for apps) ✅

## Step 7: Create requirements.txt ✅
- List all dependencies: fastapi, uvicorn, python-jose, firebase-admin, pydantic, requests ✅

## Step 8: Create Procfile ✅
- Define command for Render: web: uvicorn main:app --host 0.0.0.0 --port 10000 ✅

## Step 9: Create .env.example ✅
- Provide template for environment variables: FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL, JWT_SECRET ✅
- Explain formatting for FIREBASE_PRIVATE_KEY ✅

## Step 10: Test the server locally
- Run uvicorn main:app --reload
- Check /docs for Swagger documentation
- Test endpoints manually or with Postman

## Step 11: Prepare for deployment
- Ensure all files are ready
- Instructions for setting env vars in Render dashboard
