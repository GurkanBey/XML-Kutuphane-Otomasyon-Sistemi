"""
XML Parsing API Routes
This module provides API endpoints for demonstrating XML parsing techniques.
"""

from flask import Blueprint, request, Response, jsonify
import os
from lxml import etree
import json
import time

from ..utils.auth_utils import student_required
from ..utils.xml_utils import create_xml_response, create_error_response

# Import the different XML parsing methods
from ..utils.xml_parsers.dom_parser import parse_with_dom
from ..utils.xml_parsers.sax_parser import parse_with_sax
from ..utils.xml_parsers.etree_parser import parse_with_etree
from ..utils.xml_parsers.comparison import performance_comparison, parse_all_methods_example

bp = Blueprint('parsing', __name__, url_prefix='/api/v1/parsing')

@bp.route('/methods', methods=['POST'])
@student_required
def parse_with_all_methods():
    """Parse provided XML using different parsing methods"""
    try:
        if request.content_type != 'application/xml':
            xml_response = create_error_response("Content-Type must be application/xml")
            return xml_response, 415, {'Content-Type': 'application/xml'}
            
        xml_string = request.data.decode('utf-8')
        
        # Start timing
        start_time = time.time()
        
        # Parse using all methods
        results = {}
        
        # DOM parsing
        dom_start = time.time()
        try:
            dom_result = parse_with_dom(xml_string)
            results['dom'] = {
                'status': 'success',
                'time_ms': round((time.time() - dom_start) * 1000, 2),
                'method': 'DOM-based (XmlDocument equivalent)',
                'description': 'Loads entire document into memory as a tree, good for random access',
                'result': 'Parsed successfully'
            }
        except Exception as e:
            results['dom'] = {
                'status': 'error',
                'time_ms': round((time.time() - dom_start) * 1000, 2),
                'method': 'DOM-based (XmlDocument equivalent)',
                'error': str(e)
            }
            
        # SAX parsing
        sax_start = time.time()
        try:
            sax_result = parse_with_sax(xml_string)
            results['sax'] = {
                'status': 'success',
                'time_ms': round((time.time() - sax_start) * 1000, 2),
                'method': 'SAX/Pull parsing (XmlReader equivalent)',
                'description': 'Event-based, sequential parsing, memory efficient',
                'result': 'Parsed successfully'
            }
        except Exception as e:
            results['sax'] = {
                'status': 'error',
                'time_ms': round((time.time() - sax_start) * 1000, 2),
                'method': 'SAX/Pull parsing (XmlReader equivalent)',
                'error': str(e)
            }
            
        # ElementTree parsing
        etree_start = time.time()
        try:
            etree_result = parse_with_etree(xml_string)
            results['etree'] = {
                'status': 'success',
                'time_ms': round((time.time() - etree_start) * 1000, 2),
                'method': 'ElementTree (LINQ to XML equivalent)',
                'description': 'Pythonic API, good balance between features and performance',
                'result': 'Parsed successfully'
            }
        except Exception as e:
            results['etree'] = {
                'status': 'error',
                'time_ms': round((time.time() - etree_start) * 1000, 2),
                'method': 'ElementTree (LINQ to XML equivalent)',
                'error': str(e)
            }
            
        # Performance summary
        total_time = round((time.time() - start_time) * 1000, 2)
        
        # Build response XML
        root = etree.Element('parsing-methods-results')
        summary = etree.SubElement(root, 'summary')
        etree.SubElement(summary, 'total-time-ms').text = str(total_time)
        
        methods = etree.SubElement(root, 'methods')
        
        for method_name, method_data in results.items():
            method_elem = etree.SubElement(methods, 'method')
            etree.SubElement(method_elem, 'name').text = method_name
            etree.SubElement(method_elem, 'type').text = method_data['method']
            etree.SubElement(method_elem, 'status').text = method_data['status']
            etree.SubElement(method_elem, 'time-ms').text = str(method_data['time_ms'])
            
            if 'description' in method_data:
                etree.SubElement(method_elem, 'description').text = method_data['description']
                
            if 'error' in method_data:
                etree.SubElement(method_elem, 'error').text = method_data['error']
                
        # Build recommendations
        recomm = etree.SubElement(root, 'recommendations')
        etree.SubElement(recomm, 'note').text = "DOM: Best for small documents with random access needs"
        etree.SubElement(recomm, 'note').text = "SAX: Best for large documents with low memory requirements"
        etree.SubElement(recomm, 'note').text = "ElementTree: Good balance for most general XML processing"
        
        return Response(etree.tostring(root, encoding='unicode', pretty_print=True),
                      mimetype='application/xml')
            
    except Exception as e:
        return create_error_response(str(e)), 500, {'Content-Type': 'application/xml'}

@bp.route('/performance', methods=['POST'])
@student_required
def compare_performance():
    """Compare performance of different parsing methods"""
    try:
        if request.content_type != 'application/xml':
            xml_response = create_error_response("Content-Type must be application/xml")
            return xml_response, 415, {'Content-Type': 'application/xml'}
            
        xml_string = request.data.decode('utf-8')
        
        # Get repeat count from query param if provided
        repeat = request.args.get('repeat', default=50, type=int)
        if repeat > 1000:  # limit for safety
            repeat = 1000
            
        # Run performance comparison
        perf_results = performance_comparison(xml_string, repeat)
        
        # Build response XML
        root = etree.Element('parsing-performance-results')
        summary = etree.SubElement(root, 'summary')
        etree.SubElement(summary, 'repeat-count').text = str(repeat)
        
        methods = etree.SubElement(root, 'methods')
        
        for method_name, time_value in perf_results.items():
            if method_name == 'memory_notes':
                continue
                
            method_elem = etree.SubElement(methods, 'method')
            etree.SubElement(method_elem, 'name').text = method_name
            etree.SubElement(method_elem, 'time-ms').text = str(round(time_value * 1000, 4))
            etree.SubElement(method_elem, 'memory-note').text = perf_results['memory_notes'][method_name]
            
        # Find fastest method
        fastest = min(
            ['dom', 'sax', 'etree', 'sax_callback'], 
            key=lambda k: perf_results[k]
        )
        etree.SubElement(root, 'fastest-method').text = fastest
            
        return Response(etree.tostring(root, encoding='unicode', pretty_print=True),
                      mimetype='application/xml')
            
    except Exception as e:
        return create_error_response(str(e)), 500, {'Content-Type': 'application/xml'}
