# AppQuanta FastAPI Backend

A modern, efficient backend API for the AppQuanta application, built with FastAPI and integrated with Firebase Authentication and Firestore.

## Features

- **User Authentication**: Register and login users with Firebase Auth
- **JWT Token Management**: Secure API endpoints with JWT authentication
- **App Management**: CRUD operations for user applications stored in Firestore
- **Automatic Documentation**: Swagger UI available at `/docs`
- **CORS Support**: Configured for Flutter app integration
- **Error Handling**: Standardized error responses
- **24/7 Deployment**: Ready for Render deployment

## Tech Stack

- **Framework**: FastAPI
- **Authentication**: Firebase Auth + JWT
- **Database**: Firebase Firestore
- **Deployment**: Render
- **Language**: Python 3.11+

## Project Structure

```
appQuanta-server/
├── main.py                 # FastAPI application entry point
├── models/
│   ├── user.py            # User-related Pydantic models
│   └── app.py             # App-related Pydantic models
├── routes/
│   ├── auth.py            # Authentication endpoints
│   └── apps.py            # App management endpoints
├── services/
│   └── firebase_service.py # Firebase integration
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user and get JWT token

### Apps Management (Protected)
- `GET /api/v1/apps` - Get user's apps
- `POST /api/v1/apps/create` - Create new app
- `PUT /api/v1/apps/{app_id}` - Update app
- `DELETE /api/v1/apps/{app_id}` - Delete app

## Response Format

All API responses follow this standardized format:

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": { ... }
}
```

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd appQuanta-server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Firebase project credentials
   - Generate a secure JWT secret

5. **Run the server**
   ```bash
   python main.py
   ```

   The server will start at `http://localhost:8000`

## Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Authentication and Firestore
3. Generate a service account key (JSON file)
4. Set the following environment variables:
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_PRIVATE_KEY` (format with \n for line breaks)
   - `FIREBASE_CLIENT_EMAIL`
   - `JWT_SECRET`

## Flutter Integration

### Authentication
```dart
// Register
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/auth/register'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': 'user@example.com',
    'password': 'password123',
    'display_name': 'User Name'
  }),
);

// Login
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/auth/login'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'email': 'user@example.com',
    'password': 'password123'
  }),
);

// Extract token from response
final token = jsonDecode(response.body)['data']['access_token'];
```

### App Management
```dart
// Get apps
final response = await http.get(
  Uri.parse('https://your-render-app.com/api/v1/apps'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json'
  },
);

// Create app
final response = await http.post(
  Uri.parse('https://your-render-app.com/api/v1/apps/create'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json'
  },
  body: jsonEncode({
    'name': 'My App',
    'description': 'App description',
    'status': 'active'
  }),
);
```

## Deployment to Render

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Configure build settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Set environment variables** in Render dashboard:
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_PRIVATE_KEY`
   - `FIREBASE_CLIENT_EMAIL`
   - `JWT_SECRET`
   - `PORT` (automatically set by Render)

## Development

- **API Documentation**: Visit `http://localhost:8000/docs` for Swagger UI
- **Testing**: Use Postman or similar tools to test endpoints
- **Linting**: Run `flake8` for code quality checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
