from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from flask import request, current_app
from app.utils.xml_utils import create_error_response
import os
import jwt


def authenticate(username, password):
    """
    Authenticate a user and return their data
    """
    from app.models.user import User
    return User.authenticate(username, password)


def generate_token(user_data):
    """
    Generate a JWT token for a user
    """
    # Convert identity to a string representation for compatibility
    identity = str(user_data['id'])
    
    # Include user data as additional claims instead of in the subject
    additional_claims = {
        'username': user_data['username'],
        'role': user_data['role'],
        'user_id': user_data['id']
    }
    
    print(f"Generating token with identity: {identity} and claims: {additional_claims}")
    token = create_access_token(identity=identity, additional_claims=additional_claims)
    print(f"Generated token: {token}")
    
    return token


def admin_required(fn):
    """
    Decorator to require admin role
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Get Authorization header
            auth_header = request.headers.get('Authorization', '')
            print(f"Authorization header: {auth_header}")
            
            if not auth_header:
                print("Missing Authorization header")
                xml_response = create_error_response("Missing Authorization header")
                return xml_response, 401, {'Content-Type': 'application/xml'}
                
            # Handle both with and without Bearer prefix
            token = auth_header
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
            print(f"Extracted token: {token}")
            
            # Manually decode JWT token
            try:
                secret = current_app.config.get('JWT_SECRET_KEY')
                algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
                decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
                
                print(f"Decoded token: {decoded_token}")
                
                # Get role from the additional claims
                role = decoded_token.get('role')
                
                if role != 'admin':
                    print(f"User role not admin: {role}")
                    xml_response = create_error_response("Admin privileges required")
                    return xml_response, 403, {'Content-Type': 'application/xml'}
                
                print("Admin role verified, proceeding with request")
                return fn(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                print("Token has expired")
                xml_response = create_error_response("Token has expired")
                return xml_response, 401, {'Content-Type': 'application/xml'}
                
            except jwt.InvalidTokenError as e:
                print(f"Invalid token: {str(e)}")
                xml_response = create_error_response(f"Invalid token: {str(e)}")
                return xml_response, 401, {'Content-Type': 'application/xml'}
                
        except Exception as e:
            print(f"Unexpected error in admin_required: {str(e)}")
            xml_response = create_error_response(f"Authentication error: {str(e)}")
            return xml_response, 500, {'Content-Type': 'application/xml'}
    
    return wrapper


def student_required(fn):
    """
    Decorator to require student role (or admin)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Get Authorization header
            auth_header = request.headers.get('Authorization', '')
            print(f"Authorization header: {auth_header}")
            
            if not auth_header:
                print("Missing Authorization header")
                xml_response = create_error_response("Missing Authorization header")
                return xml_response, 401, {'Content-Type': 'application/xml'}
            
            # Handle both with and without Bearer prefix
            token = auth_header
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
            print(f"Extracted token: {token}")
            
            # Manually decode JWT token
            try:
                secret = current_app.config.get('JWT_SECRET_KEY')
                algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
                decoded_token = jwt.decode(token, secret, algorithms=[algorithm])
                
                print(f"Decoded token: {decoded_token}")
                
                # Get role from the additional claims
                role = decoded_token.get('role')
                
                if role not in ['student', 'admin']:
                    print(f"User role not authorized: {role}")
                    xml_response = create_error_response("Student or admin privileges required")
                    return xml_response, 403, {'Content-Type': 'application/xml'}
                
                print("Role verified, proceeding with request")
                return fn(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                print("Token has expired")
                xml_response = create_error_response("Token has expired")
                return xml_response, 401, {'Content-Type': 'application/xml'}
                
            except jwt.InvalidTokenError as e:
                print(f"Invalid token: {str(e)}")
                xml_response = create_error_response(f"Invalid token: {str(e)}")
                return xml_response, 401, {'Content-Type': 'application/xml'}
                
        except Exception as e:
            print(f"Unexpected error in student_required: {str(e)}")
            xml_response = create_error_response(f"Authentication error: {str(e)}")
            return xml_response, 500, {'Content-Type': 'application/xml'}
    
    return wrapper
