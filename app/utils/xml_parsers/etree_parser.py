"""
ElementTree-based XML Parser (similar to LINQ to XML)
This module implements XML parsing using ElementTree, which provides a pythonic
approach somewhat similar to LINQ to XML in .NET
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Union, Optional

def parse_with_etree(xml_string: str) -> Dict[str, Any]:
    """
    Parse XML using ElementTree (similar to LINQ to XML functionality in .NET)
    
    ElementTree provides a Pythonic way to parse XML, with methods for finding and
    filtering elements, somewhat similar to LINQ to XML's query capabilities.
    
    Args:
        xml_string: XML content as string
        
    Returns:
        Dictionary representation of the XML
    """
    try:
        root = ET.fromstring(xml_string)
        result = {root.tag: _process_etree_element(root)}
        return result
    except Exception as e:
        raise ValueError(f"ElementTree parsing error: {str(e)}")

def _process_etree_element(element) -> Dict[str, Any]:
    """Process an ElementTree element recursively"""
    result = {}
    
    # Process attributes
    if element.attrib:
        result['@attributes'] = element.attrib.copy()
    
    # Process child elements
    children_by_tag = {}
    for child in element:
        if child.tag not in children_by_tag:
            children_by_tag[child.tag] = []
        children_by_tag[child.tag].append(child)
    
    # If no children, just get the text
    if not children_by_tag:
        text = element.text
        if text is not None and text.strip():
            result['#text'] = text.strip()
        return result
    
    # Process all child elements
    for tag, children in children_by_tag.items():
        if len(children) == 1:
            # Single child of this type
            result[tag] = _process_etree_element(children[0])
        else:
            # Multiple children of this type
            result[tag] = [_process_etree_element(child) for child in children]
    
    return result

def etree_query_example():
    """Example usage of ElementTree with query capabilities (LINQ to XML-like)"""
    xml = """
    <library>
        <book id="1" category="fiction">
            <title>To Kill a Mockingbird</title>
            <author>Harper Lee</author>
            <year>1960</year>
        </book>
        <book id="2" category="fiction">
            <title>1984</title>
            <author>George Orwell</author>
            <year>1949</year>
        </book>
        <book id="3" category="nonfiction">
            <title>A Brief History of Time</title>
            <author>Stephen Hawking</author>
            <year>1988</year>
        </book>
    </library>
    """
    
    # Parse XML
    root = ET.fromstring(xml)
    
    # Example 1: Find all books
    print("\nAll book titles:")
    for title in root.findall('.//title'):
        print(f"- {title.text}")
    
    # Example 2: Find books in the fiction category
    print("\nFiction books:")
    for book in root.findall('./book[@category="fiction"]'):
        title = book.find('title').text
        author = book.find('author').text
        print(f"- {title} by {author}")
    
    # Example 3: Find books published after 1950
    print("\nBooks published after 1950:")
    for book in root.findall('./book'):
        year = int(book.find('year').text)
        if year > 1950:
            title = book.find('title').text
            print(f"- {title} ({year})")
    
    # Traditional parsing
    result = parse_with_etree(xml)
    print("\nElementTree Parsing Result:")
    print(result)
    
    return result
