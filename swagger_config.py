"""
Swagger/OpenAPI Configuration for SATI API
Production-ready API documentation with security schemes
"""

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "SATI API - Scam Detection System",
        "description": """
# SATI API Documentation

ระบบตรวจจับมิจฉาชีพด้วย AI สำหรับการวิเคราะห์บทสนทนาที่น่าสงสัย

## Features
- 🔐 User Authentication with JWT
- 🤖 AI-Powered Scam Detection (Google Gemini)
- 📊 Conversation Analysis with Risk Levels
- 📝 Report History Management
- 📈 Statistics & Analytics

## Authentication
Most endpoints require authentication. To use them:
1. Register a new account at `/api/v1/auth/register`
2. Login to get an access token at `/api/v1/auth/login`
3. Click the **Authorize** button (🔒) at the top right
4. ใส่แค่ **Token** เท่านั้น (ไม่ต้องใส่ 'Bearer ' นำหน้า - ระบบจะเพิ่มให้อัตโนมัติ!)
5. Click **Authorize** and close the dialog
6. Now you can test authenticated endpoints

## Risk Levels
- **danger** (≥ 0.75): High scam probability - immediate action recommended
- **warning** (0.40-0.74): Suspicious patterns detected - be cautious
- **normal** (< 0.40): Low risk - no significant threats detected

## Error Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request - Invalid input
- `401`: Unauthorized - Invalid or missing token
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `409`: Conflict - Resource already exists
- `500`: Internal Server Error

## Rate Limiting
API endpoints are rate-limited to prevent abuse. Production limits:
- Authentication: 10 requests/minute
- Scam Analysis: 30 requests/minute
- Other endpoints: 60 requests/minute

## Support
For issues or questions: https://github.com/your-org/sati-api
        """,
        "version": "1.0.0",
        "contact": {
            "name": "SATI API Support",
            "email": "support@sati-api.com",
            "url": "https://github.com/your-org/sati-api"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "termsOfService": "https://sati-api.com/terms"
    },
    "host": "localhost:3000",
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "ใส่แค่ Token เท่านั้น (ไม่ต้องใส่ 'Bearer ' นำหน้า ระบบจะเพิ่มให้อัตโนมัติ)"
        }
    },
    "tags": [
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints"
        },
        {
            "name": "Scam Detection",
            "description": "AI-powered scam detection and analysis endpoints"
        },
        {
            "name": "Health",
            "description": "Health check and system status endpoints"
        }
    ],
    "definitions": {
        "Error": {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "example": False
                },
                "message": {
                    "type": "string",
                    "example": "Error message"
                },
                "error": {
                    "type": "string",
                    "example": "Detailed error information"
                }
            }
        },
        "ValidationError": {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "example": False
                },
                "errors": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "example": ["Email is required", "Password must be at least 6 characters"]
                }
            }
        }
    }
}
