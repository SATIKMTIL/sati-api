"""
Swagger/OpenAPI schemas for scam detection endpoints
"""

analyze_request_schema = {
    "type": "object",
    "properties": {
        "conversation_text": {
            "type": "string",
            "minLength": 10,
            "description": "The conversation text to analyze for scam patterns",
            "example": "สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร บัญชีของคุณมีปัญหาต้องโอนเงินมาตรวจสอบด่วน"
        }
    },
    "required": ["conversation_text"]
}

analysis_result_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["danger", "warning", "normal"],
            "description": "Risk level classification",
            "example": "danger"
        },
        "confidence_score": {
            "type": "number",
            "format": "float",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence score (0.0 - 1.0)",
            "example": 0.95
        },
        "reason": {
            "type": "string",
            "description": "Detailed explanation in Thai language",
            "example": "พบสัญญาณเตือนภัยหลายอย่าง เช่น การอ้างเป็นเจ้าหน้าที่ธนาคาร ขอโอนเงิน และสร้างความเร่งรีบ"
        },
        "red_flags": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of detected red flags",
            "example": [
                "อ้างว่าเป็นเจ้าหน้าที่ธนาคาร",
                "ขอโอนเงินโดยตรง",
                "สร้างความเร่งรีบและกดดัน"
            ]
        }
    }
}

analyze_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "report_id": {
            "type": "string",
            "description": "Unique report identifier",
            "example": "507f1f77bcf86cd799439011"
        },
        "analysis": analysis_result_schema
    }
}

report_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "description": "Report unique identifier",
            "example": "507f1f77bcf86cd799439011"
        },
        "conversation_text": {
            "type": "string",
            "description": "Original conversation text analyzed",
            "example": "สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร..."
        },
        "status": {
            "type": "string",
            "enum": ["danger", "warning", "normal"],
            "description": "Risk level",
            "example": "danger"
        },
        "confidence_score": {
            "type": "number",
            "format": "float",
            "minimum": 0.0,
            "maximum": 1.0,
            "description": "Confidence score",
            "example": 0.95
        },
        "reason": {
            "type": "string",
            "description": "Analysis reason",
            "example": "พบสัญญาณเตือนภัยหลายอย่าง..."
        },
        "red_flags": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "Detected red flags",
            "example": ["อ้างว่าเป็นเจ้าหน้าที่", "ขอโอนเงิน"]
        },
        "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "Report creation timestamp",
            "example": "2024-01-06T10:30:00"
        }
    }
}

history_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "reports": {
            "type": "array",
            "items": report_schema
        },
        "count": {
            "type": "integer",
            "description": "Number of reports returned",
            "example": 10
        }
    }
}

report_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "report": report_schema
    }
}

statistics_schema = {
    "type": "object",
    "properties": {
        "total": {
            "type": "integer",
            "description": "Total number of reports",
            "example": 100
        },
        "danger": {
            "type": "integer",
            "description": "Number of danger-level reports",
            "example": 30
        },
        "warning": {
            "type": "integer",
            "description": "Number of warning-level reports",
            "example": 45
        },
        "normal": {
            "type": "integer",
            "description": "Number of normal-level reports",
            "example": 25
        }
    }
}

statistics_response_schema = {
    "type": "object",
    "properties": {
        "success": {
            "type": "boolean",
            "example": True
        },
        "statistics": statistics_schema
    }
}
