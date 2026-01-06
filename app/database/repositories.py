from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, email, password, name):
        """Create a new user"""
        user_data = {
            'email': email.lower(),
            'password': generate_password_hash(password),
            'name': name,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email.lower()})

    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            if not user_id or not isinstance(user_id, str):
                return None
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except Exception as e:
            logger.warning(f"Invalid user_id format: {user_id}")
            return None

    def verify_password(self, user, password):
        """Verify user password"""
        return check_password_hash(user['password'], password)


class ScamReportRepository:
    def __init__(self, db):
        self.collection = db.scam_reports

    def create_report(self, user_id, conversation_text, analysis_result):
        """Create a new scam report"""
        report_data = {
            'user_id': user_id,
            'conversation_text': conversation_text,
            'status': analysis_result.get('status'),
            'confidence_score': analysis_result.get('confidence_score'),
            'reason': analysis_result.get('reason'),
            'red_flags': analysis_result.get('red_flags', []),
            'created_at': datetime.utcnow()
        }
        result = self.collection.insert_one(report_data)
        return str(result.inserted_id)

    def get_user_reports(self, user_id, limit=50, skip=0):
        """Get user's scam reports with pagination"""
        reports = self.collection.find(
            {'user_id': user_id}
        ).sort('created_at', -1).skip(skip).limit(limit)
        
        return [{
            'id': str(report['_id']),
            'conversation_text': report['conversation_text'],
            'status': report['status'],
            'confidence_score': report.get('confidence_score'),
            'reason': report['reason'],
            'red_flags': report.get('red_flags', []),
            'created_at': report['created_at'].isoformat()
        } for report in reports]

    def get_report_by_id(self, report_id, user_id):
        """Get specific report by ID for a user"""
        try:
            if not report_id or not isinstance(report_id, str):
                return None
            report = self.collection.find_one({
                '_id': ObjectId(report_id),
                'user_id': user_id
            })
            if report:
                return {
                    'id': str(report['_id']),
                    'conversation_text': report['conversation_text'],
                    'status': report['status'],
                    'confidence_score': report.get('confidence_score'),
                    'reason': report['reason'],
                    'red_flags': report.get('red_flags', []),
                    'created_at': report['created_at'].isoformat()
                }
            return None
        except Exception as e:
            logger.warning(f"Invalid report_id format: {report_id}")
            return None

    def get_statistics(self, user_id):
        """Get user's scam detection statistics"""
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }}
        ]
        results = list(self.collection.aggregate(pipeline))
        
        stats = {
            'total': 0,
            'danger': 0,
            'warning': 0,
            'normal': 0
        }
        
        for result in results:
            status = result['_id']
            count = result['count']
            stats[status] = count
            stats['total'] += count
            
        return stats
