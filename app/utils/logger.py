import logging
import sys


def setup_logging(app):
    """Setup logging configuration"""
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure app logger
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(console_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        handlers=[console_handler]
    )
    
    app.logger.info("Logging configured successfully")
