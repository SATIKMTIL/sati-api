# SATI API - Scam Detection System

ระบบตรวจจับมิจฉาชีพด้วย AI สำหรับการวิเคราะห์บทสนทนาที่น่าสงสัย

## Features

- 🔐 **Authentication System**: User registration and login with JWT
- 🤖 **AI-Powered Scam Detection**: Powered by Google Gemini AI
- 📊 **Scam Analysis**: Analyze conversations and get risk levels (danger, warning, normal)
- 📝 **Report History**: Track all scam detection reports
- 📈 **Statistics**: Get insights on scam detection patterns
- 🗄️ **MongoDB Integration**: Persistent data storage
- 📚 **Interactive API Documentation**: Swagger/OpenAPI UI for testing endpoints

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **AI**: Google Gemini API
- **Authentication**: JWT (Flask-JWT-Extended)
- **API**: RESTful API
- **Documentation**: Swagger/OpenAPI (Flasgger)

## Project Structure

```
sati-api/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py
│   │   ├── routes.py           # Login, register, user endpoints
│   │   └── models.py           # User model and validation
│   ├── scam_detection/         # Scam detection module
│   │   ├── __init__.py
│   │   ├── routes.py           # Scam analysis endpoints
│   │   ├── services.py         # Gemini AI integration
│   │   └── models.py           # Scam report model
│   ├── database/               # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py       # MongoDB connection
│   │   └── repositories.py    # Data access layer
│   ├── middleware/             # Middleware
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT authentication
│   ├── schemas/               # Swagger schemas
│   │   ├── __init__.py
│   │   ├── auth_schemas.py    # Auth endpoint schemas
│   │   └── scam_schemas.py    # Scam detection schemas
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── logger.py          # Logging setup
│       └── helpers.py         # Helper functions
├── config.py                   # Configuration
├── swagger_config.py          # Swagger/OpenAPI clper functions
├── config.py                   # Configuration
├── app.py                      # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables example
└── .gitignore               # Git ignore file
```

## Installation

### Option 1: Docker (Recommended) 🐳

The fastest way to get started! Docker handles all dependencies including MongoDB.

```bash
# 1. Copy environment file
cp .env.docker .env

# 2. Edit .env with your credentials
# Required: GOOGLE_API_KEY, SECRET_KEY, JWT_SECRET_KEY

# 3. Start all services
docker-compose up -d

# 4. Access the API
# http://localhost:5000/api/docs
```

**That's it!** MongoDB and the API are now running.

📖 See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed Docker documentation.

### Option 2: Manual Installation

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud instance)
- Google Gemini API Key

### Setup Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd sati-api
```

2. **Create virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
# Copy .env.example to .env
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

Edit `.env` file with your credentials:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGO_URI=mongodb://localhost:27017/sati_api
GOOGLE_API_KEY=your-google-api-key-here
```

5. **Run the application**

```bash
python Documentation (Swagger UI)

### Accessing Interactive Documentation

Once the application is running, access the **Swagger UI** for interactive API documentation and testing:

```

http://localhost:5000/api/docs

```

### Swagger UI Features

- 📖 **Complete API Documentation**: All endpoints with detailed descriptions
- 🧪 **Test API Directly**: Execute API calls from the browser
- 🔒 **JWT Authentication**: Built-in token authorization
- 📝 **Request/Response Examples**: See real examples for all endpoints
- ✅ **Schema Validation**: View required fields and data types
- 🌐 **Multi-language Support**: Thai and English descriptions

### Using Swagger UI

1. **Open Swagger UI** at `http://localhost:5000/api/docs`
2. **Register a new account**:
   - Find `POST /api/v1/auth/register` endpoint
   - Click "Try it out"
   - Fill in the request body
   - Click "Execute"
   - Copy the `access_token` from the response

3. **Authorize with JWT**:
   - Click the **Authorize 🔒** button (top right)
   - Enter: `Bearer <your_access_token>`
   - Click "Authorize" and close

4. **Test Protected Endpoints**:
   - Now you can test all authenticated endpoints
   - Try `/api/v1/scam/analyze` to analyze a conversation
   - View your history with `/api/v1/scam/history`

### API Specification

The OpenAPI specification is available at:
```

http://localhost:5000/apispec.json

```

You can import this into tools like:
- Postman
- Insomnia
- VS Code REST Client extensions

## API app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication

#### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "User Name"
}
```

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Scam Detection

#### Analyze Conversation

```http
POST /api/v1/scam/analyze
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "conversation_text": "สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร บัญชีของคุณมีปัญหา กรุณาโอนเงิน..."
}
```

Response:

```json
{
  "success": true,
  "report_id": "507f1f77bcf86cd799439011",
  "analysis": {
    "status": "danger",
    "confidence_score": 0.95,
    "reason": "พบสัญญาณเตือนภัยหลายอย่าง...",
    "red_flags": [
      "อ้างว่าเป็นเจ้าหน้าที่ธนาคาร",
      "ขอโอนเงินโดยตรง",
      "สร้างความกลัว"
    ]
  }
}
```

#### Get History

```http
GET /api/v1/scam/history?limit=50&skip=0
Authorization: Bearer <access_token>
```

#### Get Report by ID

```http
GET /api/v1/scam/report/<report_id>
Authorization: Bearer <access_token>
```

#### Get Statistics

```http
GET /api/v1/scam/statistics
Authorization: Bearer <access_token>
```

Response:

```json
{
  "success": true,
  "statistics": {
    "total": 100,
    "danger": 30,
    "warning": 45,
    "normal": 25
  }
}
```

### Health Check

```http
GET /
GET /api/v1/health
```

## Risk Levels

- **🔴 Danger** (confidence ≥ 0.75): High probability of scam, multiple red flags detected
- **🟡 Warning** (0.40 ≤ confidence < 0.75): Suspicious patterns found, be cautious
- **🟢 Normal** (confidence < 0.40): Low risk, no significant red flags

## Scam Detection Red Flags

The AI analyzes conversations for these patterns:

1. Direct money transfer requests
2. Creating urgency or pressure
3. Impersonating officials, banks, or companies
4. Requesting sensitive personal information (passwords, PINs)
5. Too-good-to-be-true offers or prizes
6. Fear-inducing language (threats of arrest, account closure)
7. Unusual grammar or language errors
8. Requests to download apps or click unknown links
9. Claims of changed phone numbers from relatives/friends
10. Social engineering techniques

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
python app.py
```

### Running in Production Mode

```bash
export FLASK_ENV=production  # macOS/Linux
set FLASK_ENV=production     # Windows
python app.py
```

### Accessing Swagger UI in Different Environments

**Development**: `http://localhost:5000/api/docs`

**Production**: Update `host` in `swagger_config.py` to your production domain:

```python
"host": "api.yourdomain.com",
"schemes": ["https"]
```

## MongoDB Setup

### Local MongoDB

```bash
# Install MongoDB and run
mongod
```

### MongoDB Atlas (Cloud)

1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string
4. Update `MONGO_URI` in `.env`

## Security Considerations

- Never commit `.env` file to git
- Use strong `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Enable MongoDB authentication
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Validate and sanitize all user inputs
- **Swagger UI in Production**:
  - Consider restricting Swagger UI access in production
  - Use environment variables to enable/disable Swagger
  - Add authentication for `/api/docs` endpoint if needed
  - Update `swagger_config.py` to use production URLs

### Production Swagger Configuration

For production, update `swagger_config.py`:

```python
import os

swagger_template = {
    # ... other config ...
    "host": os.getenv("API_HOST", "api.yourdomain.com"),
    "schemes": ["https"],  # Use HTTPS only in production
}

# Optionally disable Swagger in production
SWAGGER_ENABLED = os.getenv("SWAGGER_ENABLED", "true").lower() == "true"
```

Then in `app/__init__.py`:

```python
# Only initialize Swagger if enabled
if app.config.get('SWAGGER_ENABLED', True):
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
```

## API Testing Tools

### Using Swagger UI (Recommended)

- Built-in interactive testing at `/api/docs`
- No additional tools needed
- Copy access tokens directly from responses

### Using curl

```bash
# Register
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Analyze conversation
curl -X POST http://localhost:5000/api/v1/scam/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"conversation_text":"สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร..."}'
```

### Using Postman

1. Import OpenAPI spec from `http://localhost:5000/apispec.json`
2. Set up authorization with Bearer token
3. Test all endpoints with saved environments

## License

MIT

## Support

For issues and questions, please create an issue in the repository.
