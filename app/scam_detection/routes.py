from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.database.connection import get_database
from app.database.repositories import ScamReportRepository
from app.scam_detection.models import ScamReport
from app.scam_detection.services import ScamDetectionService
from app.utils.helpers import sanitize_input
from app.middleware.rate_limit import rate_limit
from flask import current_app
import logging

logger = logging.getLogger(__name__)

scam_bp = Blueprint('scam', __name__, url_prefix='/api/v1/scam')


@scam_bp.route('/analyze', methods=['POST'])
@jwt_required()
@rate_limit(max_requests=10, window_seconds=60)  # 10 analyses per minute
def analyze_conversation():
    """
    Analyze conversation for scam patterns
    ---
    tags:
      - Scam Detection
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        description: Conversation text to analyze
        required: true
        schema:
          type: object
          required:
            - conversation_text
          properties:
            conversation_text:
              type: string
              minLength: 10
              example: สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร บัญชีของคุณมีปัญหาต้องโอนเงินมาตรวจสอบด่วน
              description: The conversation text to analyze for scam patterns (minimum 10 characters)
    responses:
      200:
        description: Analysis completed successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            report_id:
              type: string
              example: 507f1f77bcf86cd799439011
              description: Unique identifier for the report
            analysis:
              type: object
              properties:
                status:
                  type: string
                  enum: [danger, warning, normal]
                  example: danger
                  description: Risk level classification
                confidence_score:
                  type: number
                  format: float
                  minimum: 0.0
                  maximum: 1.0
                  example: 0.95
                  description: Confidence score (0.0 = safe, 1.0 = definitely scam)
                reason:
                  type: string
                  example: พบสัญญาณเตือนภัยหลายอย่าง เช่น การอ้างเป็นเจ้าหน้าที่ธนาคาร ขอโอนเงิน และสร้างความเร่งรีบ
                  description: Detailed explanation in Thai
                red_flags:
                  type: array
                  items:
                    type: string
                  example: ["อ้างว่าเป็นเจ้าหน้าที่ธนาคาร", "ขอโอนเงินโดยตรง", "สร้างความเร่งรีบและกดดัน"]
                  description: List of detected scam indicators
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/ValidationError'
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid or expired token
      500:
        description: Analysis failed
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Sanitize input
        if data.get('conversation_text'):
            data['conversation_text'] = sanitize_input(data['conversation_text'])
        
        # Validate input
        errors = ScamReport.validate_analysis_request(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        conversation_text = data['conversation_text']
        
        # Perform scam analysis using Gemini AI
        scam_service = ScamDetectionService(current_app.config['GOOGLE_API_KEY'])
        analysis_result = scam_service.analyze_conversation(conversation_text)
        
        # Save report to database
        db = get_database()
        report_repo = ScamReportRepository(db)
        report_id = report_repo.create_report(user_id, conversation_text, analysis_result)
        
        logger.info(f"Scam analysis completed for user {user_id}: {analysis_result['status']}")
        
        return jsonify({
            'success': True,
            'report_id': report_id,
            'analysis': analysis_result
        }), 200
        
    except Exception as e:
        logger.error(f"Scam analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to analyze conversation',
            'error': str(e)
        }), 500


@scam_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """
    Get user's scam detection history
    ---
    tags:
      - Scam Detection
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: limit
        type: integer
        default: 50
        minimum: 1
        maximum: 100
        description: Maximum number of reports to return
        example: 50
      - in: query
        name: skip
        type: integer
        default: 0
        minimum: 0
        description: Number of reports to skip (for pagination)
        example: 0
    responses:
      200:
        description: History retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            reports:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: 507f1f77bcf86cd799439011
                  conversation_text:
                    type: string
                    example: สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร...
                  status:
                    type: string
                    enum: [danger, warning, normal]
                    example: danger
                  confidence_score:
                    type: number
                    format: float
                    example: 0.95
                  reason:
                    type: string
                    example: พบสัญญาณเตือนภัยหลายอย่าง...
                  red_flags:
                    type: array
                    items:
                      type: string
                    example: ["อ้างว่าเป็นเจ้าหน้าที่", "ขอโอนเงิน"]
                  created_at:
                    type: string
                    format: date-time
                    example: 2024-01-06T10:30:00
            count:
              type: integer
              example: 10
              description: Number of reports returned
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid or expired token
      500:
        description: Failed to retrieve history
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters with validation
        try:
            limit = int(request.args.get('limit', 50))
            skip = int(request.args.get('skip', 0))
            
            # Validate ranges
            if limit < 1 or limit > 100:
                return jsonify({
                    'success': False,
                    'message': 'Limit must be between 1 and 100'
                }), 400
            
            if skip < 0:
                return jsonify({
                    'success': False,
                    'message': 'Skip must be non-negative'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid pagination parameters'
            }), 400
        
        db = get_database()
        report_repo = ScamReportRepository(db)
        reports = report_repo.get_user_reports(user_id, limit=limit, skip=skip)
        
        return jsonify({
            'success': True,
            'reports': reports,
            'count': len(reports)
        }), 200
        
    except Exception as e:
        logger.error(f"Get history error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get history',
            'error': str(e)
        }), 500


@scam_bp.route('/report/<report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """
    Get specific scam report by ID
    ---
    tags:
      - Scam Detection
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: report_id
        type: string
        required: true
        description: Unique identifier of the report
        example: 507f1f77bcf86cd799439011
    responses:
      200:
        description: Report retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            report:
              type: object
              properties:
                id:
                  type: string
                  example: 507f1f77bcf86cd799439011
                conversation_text:
                  type: string
                  example: สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร บัญชีของคุณมีปัญหา...
                status:
                  type: string
                  enum: [danger, warning, normal]
                  example: danger
                confidence_score:
                  type: number
                  format: float
                  example: 0.95
                reason:
                  type: string
                  example: พบสัญญาณเตือนภัยหลายอย่าง...
                red_flags:
                  type: array
                  items:
                    type: string
                  example: ["อ้างว่าเป็นเจ้าหน้าที่ธนาคาร", "ขอโอนเงินโดยตรง"]
                created_at:
                  type: string
                  format: date-time
                  example: 2024-01-06T10:30:00
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid or expired token
      404:
        description: Report not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Report not found
      500:
        description: Failed to retrieve report
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        user_id = get_jwt_identity()
        
        db = get_database()
        report_repo = ScamReportRepository(db)
        report = report_repo.get_report_by_id(report_id, user_id)
        
        if not report:
            return jsonify({
                'success': False,
                'message': 'Report not found'
            }), 404
        
        return jsonify({
            'success': True,
            'report': report
        }), 200
        
    except Exception as e:
        logger.error(f"Get report error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get report',
            'error': str(e)
        }), 500


@scam_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """
    Get user's scam detection statistics
    ---
    tags:
      - Scam Detection
    security:
      - BearerAuth: []
    responses:
      200:
        description: Statistics retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            statistics:
              type: object
              properties:
                total:
                  type: integer
                  example: 100
                  description: Total number of scam reports analyzed
                danger:
                  type: integer
                  example: 30
                  description: Number of high-risk (danger) reports
                warning:
                  type: integer
                  example: 45
                  description: Number of medium-risk (warning) reports
                normal:
                  type: integer
                  example: 25
                  description: Number of low-risk (normal) reports
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Invalid or expired token
      500:
        description: Failed to retrieve statistics
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        user_id = get_jwt_identity()
        
        db = get_database()
        report_repo = ScamReportRepository(db)
        stats = report_repo.get_statistics(user_id)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get statistics error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get statistics',
            'error': str(e)
        }), 500
