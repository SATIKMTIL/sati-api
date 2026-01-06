"""
Swagger/OpenAPI schemas for authentication endpoints
"""

register_request_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",
            "description": "User email address",
            "example": "user@example.com"
        },
        "password": {
            "type": "string",
            "format": "password",
            "minLength": 6,
            "description": "User password (minimum 6 characters)",
            "example": "password123"
        },
        "name": {
            "type": "string",
            "minLength": 1,
            "description": "User's full name",
            "example": "John Doe"
        }
    },
    "required": ["email", "password", "name"]
}

login_request_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email",
            "description": "User email address",
            "example": "user@example.com"
        },
        "password": {
            "type": "string",
            "format": "password",
            "description": "User password",
            "example": "password123"
        }
    },
    "required": ["email", "password"]
}

user_response_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "User unique identifier",
            "example": "507f1f77bcf86cd799439011"
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "User email address",
            "example": "user@example.com"
        },
        "name": {
            "type": "string",
            "description": "User's full name",
            "example": "John Doe"
        },
        "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "Account creation timestamp",
            "example": "2024-01-06T10:30:00"
        }
    }
}

register_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "message": {
            "type": "string",
            "example": "User registered successfully"
        },
        "access_token": {
            "type": "string",
            "description": "JWT access token for authentication",
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        },
        "user": user_response_schema
    }
}

login_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "message": {
            "type": "string",
            "example": "Login successful"
        },
        "access_token": {
            "type": "string",
            "description": "JWT access token for authentication",
            "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        },
        "user": user_response_schema
    }
}

me_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "user": user_response_schema
    }
}
