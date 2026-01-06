import logging
import sys


def setup_logging(app):
    """Setup logging configuration"""
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Clear existing handlers to prevent duplicates
    root_logger.handlers.clear()
    app.logger.handlers.clear()
    
    # Console handler (shared)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure root logger only (app.logger will propagate to it)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # Disable Flask's default handler by setting propagate
    # App logger inherits from root, no need for separate handler
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = True
    
    # Use root logger for the confirmation message
    logging.info("Logging configured successfully")
