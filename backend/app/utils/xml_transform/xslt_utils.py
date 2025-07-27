"""
XSLT Utility Module
This module provides utilities for transforming XML data into other formats using XSLT.
"""

import lxml.etree as ET
import os
from io import StringIO

def transform_with_xslt(xml_string, xslt_string):
    """
    Transform XML data using an XSLT stylesheet.
    
    Args:
        xml_string (str): XML content as string
        xslt_string (str): XSLT stylesheet content as string
        
    Returns:
        str: Transformed content as string
    """
    try:
        # Parse XML document
        xml_doc = ET.fromstring(xml_string.encode('utf-8'))
        
        # Parse XSLT stylesheet
        xslt_doc = ET.fromstring(xslt_string.encode('utf-8'))
        transform = ET.XSLT(xslt_doc)
        
        # Apply transformation
        result = transform(xml_doc)
            
        # Convert result to string
        return ET.tostring(result, encoding='unicode')
    except Exception as e:
        return f"XSLT Error: {str(e)}"

def get_stylesheet_content(stylesheet_path):
    """
    Read an XSLT stylesheet from file.
    
    Args:
        stylesheet_path (str): Path to the XSLT stylesheet file
        
    Returns:
        str: Content of the XSLT stylesheet
    """
    try:
        with open(stylesheet_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading stylesheet: {str(e)}"

def transform_with_stylesheet_file(xml_string, stylesheet_path):
    """
    Transform XML data using an XSLT stylesheet file.
    
    Args:
        xml_string (str): XML content as string
        stylesheet_path (str): Path to the XSLT stylesheet file
        
    Returns:
        str: Transformed content as string
    """
    xslt_string = get_stylesheet_content(stylesheet_path)
    return transform_with_xslt(xml_string, xslt_string)
