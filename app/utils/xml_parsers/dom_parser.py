"""
DOM-based XML Parser (XmlDocument equivalent)
This module implements DOM-based XML parsing.
"""

import xml.dom.minidom
from typing import Dict, Any, List, Union, Optional

def parse_with_dom(xml_string: str) -> Dict[str, Any]:
    """
    Parse XML using DOM approach (similar to XmlDocument in .NET)
    
    DOM parsing loads the entire XML document into memory as a tree structure.
    Good for random access and modification, but memory-intensive for large documents.
    
    Args:
        xml_string: XML content as string
        
    Returns:
        Dictionary representation of the XML
    """
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        result = {}
        
        # Get root element
        root = dom.documentElement
        result[root.tagName] = _process_dom_element(root)
        
        return result
    except Exception as e:
        raise ValueError(f"DOM parsing error: {str(e)}")

def _process_dom_element(element) -> Dict[str, Any]:
    """Process a DOM element recursively"""
    result = {}
    
    # Process attributes
    if element.attributes and element.attributes.length > 0:
        result['@attributes'] = {
            attr.name: attr.value 
            for attr in element.attributes.values()
        }
    
    # Process child elements
    child_elements = [node for node in element.childNodes 
                     if node.nodeType == xml.dom.Node.ELEMENT_NODE]
    
    # Process text content if this is a leaf node (no child elements)
    if not child_elements:
        text_content = ''.join([
            node.data for node in element.childNodes 
            if node.nodeType == xml.dom.Node.TEXT_NODE
        ]).strip()
        
        if text_content:
            result['#text'] = text_content
        return result
    
    # Process child elements
    for child in child_elements:
        child_name = child.tagName
        child_result = _process_dom_element(child)
        
        # Handle multiple children with the same tag name
        if child_name in result:
            if isinstance(result[child_name], list):
                result[child_name].append(child_result)
            else:
                result[child_name] = [result[child_name], child_result]
        else:
            result[child_name] = child_result
            
    return result

def dom_example():
    """Example usage of DOM parser"""
    xml = """
    <library>
        <book id="1">
            <title>To Kill a Mockingbird</title>
            <author>Harper Lee</author>
        </book>
        <book id="2">
            <title>1984</title>
            <author>George Orwell</author>
        </book>
    </library>
    """
    
    result = parse_with_dom(xml)
    print("DOM Parsing Result:")
    print(result)
    return result
