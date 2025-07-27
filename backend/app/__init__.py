import os
import time
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models.database import init_db


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY='jwt-secret-strong-key-2025',
        JWT_ACCESS_TOKEN_EXPIRES=86400,  # 1 day
        JWT_ALGORITHM='HS256',
        JWT_HEADER_TYPE='Bearer',
        JWT_TOKEN_LOCATION=['headers'],
        JWT_HEADER_NAME='Authorization',
        DATABASE=os.path.join(app.instance_path, 'library.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
      # Initialize extensions
    jwt = JWTManager(app)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # Configure JWT callbacks
    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        print(f"Identity lookup called with: {identity}")
        # Return as is since we're now using a string ID as identity
        return identity

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        print(f"JWT data in lookup: {jwt_data}")
        # Extract user info from token claims
        return {
            'id': jwt_data.get("sub"),
            'username': jwt_data.get("username"),
            'role': jwt_data.get("role")
        }
    
    # Configure CORS to allow requests from frontend
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes import auth, books, external_services, info, transform, parsing
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(transform.bp)
    app.register_blueprint(external_services.bp)
    app.register_blueprint(info.bp)
    app.register_blueprint(parsing.bp)
    
    @app.route('/health')
    def health_check():
        response = "<xml><status>healthy</status><timestamp>" + str(time.time()) + "</timestamp></xml>"
        return response, 200, {
            'Content-Type': 'application/xml',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        }
    
    return app
