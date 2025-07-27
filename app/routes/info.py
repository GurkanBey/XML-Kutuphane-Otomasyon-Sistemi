from flask import Blueprint, request
from app.utils.xml_utils import create_xml_response, validate_xml_with_dtd, validate_xml_with_xsd, create_error_response
import datetime
import os
from flask import current_app

bp = Blueprint('info', __name__, url_prefix='/api/v1')

@bp.route('/info', methods=['GET'])
def get_info():
    """Simple endpoint that returns basic information about the API"""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create simple XML response with basic information
    info_data = {
        'api_info': {
            'version': 'v2',
            'name': 'Library API',
            'current_time': current_date,
            'endpoints': {
                'info': '/api/v2/info - Returns basic API information'
            },
            'status': 'active'
        }
    }
    
    xml_response = create_xml_response('success', "API information", info_data)
    return xml_response, 200, {'Content-Type': 'application/xml'}

@bp.route('/validate', methods=['POST'])
def validate_xml():
    """Validates an XML document against a schema (DTD or XSD)"""
    if request.content_type != 'application/xml':
        xml_response = create_error_response("Content-Type must be application/xml")
        return xml_response, 415, {'Content-Type': 'application/xml'}
    
    # Get the XML data from the request
    xml_data = request.data.decode('utf-8')
    
    # Get the schema type from the query parameter (default to DTD)
    schema_type = request.args.get('schema_type', 'dtd')
    
    if schema_type.lower() == 'dtd':
        # Use the book.dtd file for validation by default
        dtd_path = os.path.join(current_app.root_path, 'schemas', 'book.dtd')
        is_valid, error = validate_xml_with_dtd(xml_data, dtd_path)
        schema_name = "DTD"
    elif schema_type.lower() == 'xsd':
        # Use the book.xsd file for validation by default
        xsd_path = os.path.join(current_app.root_path, 'schemas', 'book.xsd')
        is_valid, error = validate_xml_with_xsd(xml_data, xsd_path)
        schema_name = "XSD"
    else:
        xml_response = create_error_response(f"Invalid schema type: {schema_type}")
        return xml_response, 400, {'Content-Type': 'application/xml'}
    
    # Return the validation result
    if is_valid:
        result_data = {
            'validation': {
                'schema_type': schema_name,
                'status': 'valid',
                'message': f"XML document is valid against {schema_name} schema"
            }
        }
        xml_response = create_xml_response('success', f"XML validation passed", result_data)
        return xml_response, 200, {'Content-Type': 'application/xml'}
    else:
        result_data = {
            'validation': {
                'schema_type': schema_name,
                'status': 'invalid',
                'message': error if error else f"XML document is invalid against {schema_name} schema"
            }
        }
        xml_response = create_xml_response('error', f"XML validation failed", result_data)
        return xml_response, 400, {'Content-Type': 'application/xml'}

@bp.route('/schemas/<schema_file>', methods=['GET'])
def get_schema(schema_file):
    """Returns the specified schema file"""
    schema_path = os.path.join(current_app.root_path, 'schemas', schema_file)
    
    if not os.path.exists(schema_path):
        return create_error_response(f"Schema file {schema_file} not found"), 404
    
    with open(schema_path, 'r') as f:
        schema_content = f.read()
    
    # Set the appropriate content type
    content_type = 'application/xml'
    if schema_file.endswith('.dtd'):
        content_type = 'application/xml-dtd'
    elif schema_file.endswith('.xsd'):
        content_type = 'application/xml'
    
    return schema_content, 200, {'Content-Type': content_type}
