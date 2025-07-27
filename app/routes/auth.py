from flask import Blueprint, request, current_app, url_for, Response
from app.utils.xml_utils import xml_to_dict, create_xml_response, create_error_response, validate_xml_with_xsd, validate_xml_with_dtd
from app.utils.auth_utils import authenticate, generate_token
from app.models.user import User
from app.models.database import get_db  
from werkzeug.security import generate_password_hash
from lxml import etree
import os
import inspect

bp = Blueprint('auth', __name__, url_prefix='/api/v1')


@bp.route('/login', methods=['POST'])
def login():
    """Login endpoint that returns a JWT token"""
    if request.content_type != 'application/xml':
        xml_response = create_error_response("Content-Type must be application/xml")
        return xml_response, 415, {'Content-Type': 'application/xml'}
    
    xml_data = request.data.decode('utf-8')
    
    # Validate XML using DTD
    dtd_path = os.path.join(current_app.root_path, 'schemas', 'login.dtd')
    dtd_valid, dtd_error = validate_xml_with_dtd(xml_data, dtd_path)
    
    if not dtd_valid:
        xml_response = create_error_response(f"XML DTD validation failed: {dtd_error}")
        return xml_response, 400, {'Content-Type': 'application/xml'}
    
    # Validate XML using XSD
    xsd_path = os.path.join(current_app.root_path, 'schemas', 'login.xsd')
    xsd_valid, xsd_error = validate_xml_with_xsd(xml_data, xsd_path)
    
    if not xsd_valid:
        xml_response = create_error_response(f"XML Schema validation failed: {xsd_error}")
        return xml_response, 400, {'Content-Type': 'application/xml'}
    
    # Parse XML
    try:
        login_data = xml_to_dict(xml_data)
        username = login_data['login']['username']
        password = login_data['login']['password']
    except (KeyError, ValueError) as e:
        xml_response = create_error_response(f"Invalid login XML format: {str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}
    
    # Authenticate user
    user = authenticate(username, password)
    
    if not user:
        xml_response = create_error_response("Invalid username or password")
        return xml_response, 401, {'Content-Type': 'application/xml'}
    
    # Generate JWT token
    token = generate_token(user)
    
    # Return XML response with token
    response_data = {
        'token': token,
        'user': {
            'username': user['username'],
            'role': user['role']
        }
    }
    
    xml_response = create_xml_response('success', "Authentication successful", response_data)
    return xml_response, 200, {'Content-Type': 'application/xml'}


@bp.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint - for now just sends a success response as token is handled client-side"""
    # In a more sophisticated implementation, you could track and invalidate tokens
    # But for this simple implementation, we'll just send a success response
    # since token management is handled client-side
    
    xml_response = create_xml_response('success', "Logged out successfully")
    return xml_response, 200, {'Content-Type': 'application/xml'}


@bp.route('/endpoints', methods=['GET'])
def list_endpoints():
    """List all available API v1 endpoints and their descriptions"""
    from app.routes import auth, books, external_services
    
    endpoints = []
    
    # Auth endpoints
    for name, func in inspect.getmembers(auth, inspect.isfunction):
        if hasattr(func, '__doc__') and func.__doc__ and hasattr(func, 'view_class') == False:
            route = next((rule.rule for rule in current_app.url_map.iter_rules() 
                          if rule.endpoint.startswith('auth.') and rule.endpoint.endswith('.' + name)), None)
            
            if route:
                endpoints.append({
                    'path': route,
                    'methods': list(func.view_class.methods) if hasattr(func, 'view_class') else ['GET'],
                    'description': func.__doc__.strip(),
                    'group': 'auth'
                })
    
    # Books endpoints
    for name, func in inspect.getmembers(books, inspect.isfunction):
        if hasattr(func, '__doc__') and func.__doc__:
            route = next((rule.rule for rule in current_app.url_map.iter_rules() 
                          if rule.endpoint.startswith('books.') and rule.endpoint.endswith('.' + name)), None)
            
            if route:
                endpoints.append({
                    'path': route,
                    'methods': list(func.view_class.methods) if hasattr(func, 'view_class') else ['GET'],
                    'description': func.__doc__.strip(),
                    'group': 'books'
                })
    
    # External services endpoints
    for name, func in inspect.getmembers(external_services, inspect.isfunction):
        if hasattr(func, '__doc__') and func.__doc__:
            route = next((rule.rule for rule in current_app.url_map.iter_rules() 
                          if rule.endpoint.startswith('external_services.') and rule.endpoint.endswith('.' + name)), None)
            
            if route:
                endpoints.append({
                    'path': route,
                    'methods': list(func.view_class.methods) if hasattr(func, 'view_class') else ['GET'],
                    'description': func.__doc__.strip(),
                    'group': 'external'
                })      # Create a more directly parseable XML structure
    api_endpoints = {
        'endpoints': {
            'endpoint': [
                {
                    'path': '/api/v1/login',
                    'methods': {'method': ['POST']},
                    'description': 'Login endpoint that returns a JWT token',
                    'group': 'auth'
                },
                {
                    'path': '/api/v1/register',
                    'methods': {'method': ['POST']},
                    'description': 'Register a new user endpoint',
                    'group': 'auth'
                },
                {
                    'path': '/api/v1/logout',
                    'methods': {'method': ['POST']},
                    'description': 'Logout endpoint - token invalidation is handled client-side',
                    'group': 'auth'
                },
                {
                    'path': '/api/v1/endpoints',
                    'methods': {'method': ['GET']},
                    'description': 'List all available API v1 endpoints and their descriptions',
                    'group': 'auth'
                },
                {
                    'path': '/api/v1/books',
                    'methods': {'method': ['GET']},
                    'description': 'Get all books (requires student or admin role)',
                    'group': 'books'
                },
                {
                    'path': '/api/v1/books/<id>',
                    'methods': {'method': ['GET']},
                    'description': 'Get a specific book by ID (requires student or admin role)',
                    'group': 'books'
                },
                {
                    'path': '/api/v1/books',
                    'methods': {'method': ['POST']},
                    'description': 'Add a new book (requires admin role)',
                    'group': 'books'
                },
                {
                    'path': '/api/v1/books/<id>',
                    'methods': {'method': ['DELETE']},
                    'description': 'Delete a book by ID (requires admin role)',
                    'group': 'books'
                },
                {
                    'path': '/api/v1/weather',
                    'methods': {'method': ['GET']},
                    'description': 'Get weather information from external service (requires student or admin role)',
                    'group': 'external'
                }
            ]
        }
    }
    
    xml_response = create_xml_response('success', "API v1 Endpoints", api_endpoints)
    return xml_response, 200, {'Content-Type': 'application/xml'}


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user endpoint"""
    if request.content_type != 'application/xml':
        xml_response = create_error_response("Content-Type must be application/xml")
        return xml_response, 415, {'Content-Type': 'application/xml'}
    
    xml_data = request.data.decode('utf-8')
    
    # Parse XML
    try:
        from lxml import etree
        tree = etree.fromstring(xml_data.encode('utf-8'))
        username_elem = tree.find('.//username')
        password_elem = tree.find('.//password')
        role_elem = tree.find('.//role')
        
        if username_elem is None or password_elem is None:
            xml_response = create_error_response("Missing required fields: username and password")
            return xml_response, 400, {'Content-Type': 'application/xml'}
        
        username = username_elem.text
        password = password_elem.text
        role = role_elem.text if role_elem is not None else 'student'
        
        # Check if user already exists
        from app.models.user import User
        existing_user = User.find_by_username(username)
        if existing_user:
            xml_response = create_error_response("Username already exists")
            return xml_response, 409, {'Content-Type': 'application/xml'}
        
        # Create new user
        from app.models.database import get_db
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        db.commit()
        
        # Return success response
        response_data = {
            'user': {
                'username': username,
                'role': role
            }
        }
        
        xml_response = create_xml_response('success', "User registered successfully", response_data)
        return xml_response, 201, {'Content-Type': 'application/xml'}
    
    except Exception as e:
        xml_response = create_error_response(f"Error registering user: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}
