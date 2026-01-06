import os
from app import create_app

# Get configuration from environment variable
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app using factory pattern
app = create_app(config_name)

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 3000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.run(
        host=host,
        port=port,
        debug=(config_name == 'development')
    )