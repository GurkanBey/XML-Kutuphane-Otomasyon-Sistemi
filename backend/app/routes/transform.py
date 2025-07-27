"""
XML Transformation API Routes
This module provides API endpoints for XML transformation using XPath and XSLT.
"""

from flask import Blueprint, request, Response, current_app
import os
from lxml import etree
from ..utils.xml_transform.xpath_utils import extract_with_xpath, get_book_titles, get_books_by_author, count_books
from ..utils.xml_transform.xslt_utils import transform_with_xslt, get_stylesheet_content
from ..utils.xml_utils import create_xml_response, create_error_response
from ..utils.auth_utils import admin_required, student_required

bp = Blueprint('transform', __name__, url_prefix='/api/v1/transform')

@bp.route('/xpath', methods=['POST'])
@student_required
def xpath_transform():
    """Extract data from XML using XPath expression"""
    try:
        if request.content_type != 'application/xml':
            xml_response = create_error_response("Content-Type must be application/xml")
            return xml_response, 415, {'Content-Type': 'application/xml'}
            
        request_data = request.data.decode('utf-8')
        root = etree.fromstring(request_data.encode('utf-8'))
        
        # Get XPath expression from XML request
        xpath_expr = root.xpath("//xpath/text()")[0] if root.xpath("//xpath/text()") else None
        xml_content = root.find(".//content")
        
        if xpath_expr and xml_content is not None:
            # Convert XML content element to string with its children
            xml_str = etree.tostring(xml_content, encoding='unicode')
            
            # Apply XPath
            result = extract_with_xpath(xml_str, xpath_expr)
            
            # Create response
            response_xml = etree.Element('xpath-result')
            expression = etree.SubElement(response_xml, 'expression')
            expression.text = xpath_expr
            
            results = etree.SubElement(response_xml, 'results')
            
            if isinstance(result, list):
                for item in result:
                    result_item = etree.SubElement(results, 'item')
                    result_item.text = str(item)
            else:
                results.text = str(result)
                
            return Response(etree.tostring(response_xml, encoding='unicode', pretty_print=True),
                          mimetype='application/xml')
        else:
            return create_error_response('Missing XPath expression or XML content'), 400, {'Content-Type': 'application/xml'}
            
    except Exception as e:
        return create_error_response(str(e)), 500, {'Content-Type': 'application/xml'}

@bp.route('/xslt', methods=['POST'])
@student_required
def xslt_transform():
    """Transform XML using XSLT stylesheet"""
    try:
        if request.content_type != 'application/xml':
            xml_response = create_error_response("Content-Type must be application/xml")
            return xml_response, 415, {'Content-Type': 'application/xml'}
            
        request_data = request.data.decode('utf-8')
        root = etree.fromstring(request_data.encode('utf-8'))
        
        # Get stylesheet type from XML request
        stylesheet_type = root.xpath("//stylesheet-type/text()")[0] if root.xpath("//stylesheet-type/text()") else None
        xml_content = root.find(".//content")
        
        if stylesheet_type and xml_content is not None:
            # Convert XML content element to string with its children
            xml_str = etree.tostring(xml_content, encoding='unicode')
            
            # Get appropriate stylesheet
            stylesheet_path = os.path.join(current_app.root_path, 'stylesheets', f'books_to_{stylesheet_type}.xslt')
            
            if os.path.exists(stylesheet_path):
                xslt_string = get_stylesheet_content(stylesheet_path)
                
                # Set appropriate mimetype based on stylesheet type
                if stylesheet_type == 'html':
                    mimetype = 'text/html'
                elif stylesheet_type == 'text':
                    mimetype = 'text/plain'
                else:
                    mimetype = 'application/xml'
                    
                # Apply transformation
                result = transform_with_xslt(xml_str, xslt_string)
                
                return Response(result, mimetype=mimetype)
            else:
                return create_error_response(f"Stylesheet not found for type: {stylesheet_type}"), 404, {'Content-Type': 'application/xml'}
        else:
            return create_error_response('Missing stylesheet type or XML content'), 400, {'Content-Type': 'application/xml'}
            
    except Exception as e:
        return create_error_response(str(e)), 500, {'Content-Type': 'application/xml'}

@bp.route('/examples', methods=['GET'])
def transformation_examples():
    """Get available transformation examples"""
    try:
        examples = etree.Element('transformation-examples')
        
        # XPath examples
        xpath = etree.SubElement(examples, 'xpath-examples')
        xpath_examples = [
            ('//book/title/text()', 'Extract all book titles'),
            ('//book[contains(author/text(), "Tolkien")]/title/text()', 'Find books by Tolkien'),
            ('count(//book)', 'Count total number of books'),
            ('//book[year>2000]/title/text()', 'Books published after 2000'),
            ('//book[contains(category/text(), "Fantasy")]', 'Books in Fantasy category')
        ]
        
        for expr, desc in xpath_examples:
            example = etree.SubElement(xpath, 'example')
            expression = etree.SubElement(example, 'expression')
            expression.text = expr
            description = etree.SubElement(example, 'description')
            description.text = desc
        
        # XSLT examples
        xslt = etree.SubElement(examples, 'xslt-examples')
        xslt_examples = [
            ('html', 'Transform books to HTML table format'),
            ('text', 'Transform books to plain text format'),
            ('simplified', 'Transform to simplified XML structure')
        ]
        
        for stype, desc in xslt_examples:
            example = etree.SubElement(xslt, 'example')
            stylesheet = etree.SubElement(example, 'stylesheet-type')
            stylesheet.text = stype
            description = etree.SubElement(example, 'description')
            description.text = desc
            
        return Response(etree.tostring(examples, encoding='unicode', pretty_print=True),
                       mimetype='application/xml')
                       
    except Exception as e:
        return create_error_response(str(e)), 500, {'Content-Type': 'application/xml'}
