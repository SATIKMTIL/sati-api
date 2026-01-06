from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)


class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def initialize(self, mongo_uri, db_name=None):
        """Initialize MongoDB connection"""
        try:
            self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            # Test connection
            self._client.admin.command('ping')
            
            # Extract database name from URI if not provided
            if db_name is None:
                # Parse db name from URI (e.g., mongodb://user:pass@host:port/dbname?params)
                try:
                    import re
                    match = re.search(r'/([^/?]+)(\?|$)', mongo_uri)
                    if match and match.group(1) not in ['', 'admin', 'local', 'config']:
                        db_name = match.group(1)
                    else:
                        db_name = 'sati_api'  # fallback to default
                except Exception as e:
                    logger.warning(f"Failed to parse database name from URI: {str(e)}")
                    db_name = 'sati_api'  # fallback to default
            
            self._db = self._client[db_name]
            logger.info(f"Successfully connected to MongoDB: {db_name}")
            self._create_indexes()
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing database: {str(e)}")
            raise

    def _create_indexes(self):
        """Create indexes for better performance"""
        try:
            # Users collection indexes
            self._db.users.create_index('email', unique=True)
            self._db.users.create_index('created_at')
            
            # Scam reports collection indexes
            self._db.scam_reports.create_index('user_id')
            self._db.scam_reports.create_index('created_at')
            self._db.scam_reports.create_index('status')
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating indexes: {str(e)}")

    def get_db(self):
        """Get database instance"""
        if self._db is None:
            raise Exception("Database not initialized. Call initialize() first.")
        return self._db

    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("Database connection closed")


# Singleton instance
db = Database()


def get_database():
    """Get database instance for use in routes"""
    return db.get_db()
