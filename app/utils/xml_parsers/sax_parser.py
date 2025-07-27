"""
SAX/Pull-based XML Parser (XmlReader equivalent)
This module implements SAX/Pull-based XML parsing.
"""

import xml.sax
from typing import Dict, Any, List, Union, Optional, Callable

class SaxHandler(xml.sax.ContentHandler):
    """SAX Content Handler for XML parsing"""
    
    def __init__(self):
        super().__init__()
        self.result = {}
        self.current_path = []
        self.current_data = ""
        self.current_obj = None
        self.root = None
    
    def startElement(self, name, attrs):
        """Called at element start"""
        # Create element data structure
        element = {
            '#name': name
        }
        
        # Add attributes if any
        if attrs.getLength() > 0:
            element['@attributes'] = {
                attrs.getQName(i): attrs.getValue(i)
                for i in range(attrs.getLength())
            }
        
        # Set up parent-child relationship
        if not self.root:
            self.root = element
            self.result[name] = {}
            self.current_obj = self.result[name]
        else:
            # Navigate to the current position in the tree
            parent = self.current_obj
            
            # Handle the case where there are multiple elements with the same name
            if name in parent:
                if isinstance(parent[name], list):
                    parent[name].append({})
                    self.current_obj = parent[name][-1]
                else:
                    parent[name] = [parent[name], {}]
                    self.current_obj = parent[name][-1]
            else:
                parent[name] = {}
                self.current_obj = parent[name]
        
        # Track current element path
        self.current_path.append((name, self.current_obj))
        self.current_data = ""
    
    def endElement(self, name):
        """Called at element end"""
        if self.current_data.strip():
            self.current_obj['#text'] = self.current_data.strip()
        
        # Go back up one level in the tree
        if self.current_path:
            self.current_path.pop()
            if self.current_path:
                _, self.current_obj = self.current_path[-1]
    
    def characters(self, content):
        """Called for character data"""
        self.current_data += content

def parse_with_sax(xml_string: str) -> Dict[str, Any]:
    """
    Parse XML using SAX approach (similar to XmlReader in .NET)
    
    SAX parsing is an event-driven, sequential parsing approach.
    It's memory-efficient for large documents as it doesn't load the entire XML at once.
    Good for streaming large XML files.
    
    Args:
        xml_string: XML content as string
        
    Returns:
        Dictionary representation of the XML
    """
    try:
        handler = SaxHandler()
        xml.sax.parseString(xml_string, handler)
        return handler.result
    except Exception as e:
        raise ValueError(f"SAX parsing error: {str(e)}")

def parse_with_sax_callback(xml_string: str, element_callback: Callable[[str, Dict[str, str], str], None]) -> None:
    """
    Parse XML using SAX with callbacks for more efficient streaming
    
    Args:
        xml_string: XML content as string
        element_callback: Function to call for each element: fn(name, attrs, text)
    """
    class CallbackHandler(xml.sax.ContentHandler):
        def __init__(self, callback):
            super().__init__()
            self.callback = callback
            self.current_data = ""
            self.current_name = ""
            self.current_attrs = {}
            
        def startElement(self, name, attrs):
            self.current_name = name
            self.current_attrs = {attrs.getQName(i): attrs.getValue(i) for i in range(attrs.getLength())}
            self.current_data = ""
            
        def endElement(self, name):
            self.callback(name, self.current_attrs, self.current_data.strip())
            
        def characters(self, content):
            self.current_data += content
    
    try:
        handler = CallbackHandler(element_callback)
        xml.sax.parseString(xml_string, handler)
    except Exception as e:
        raise ValueError(f"SAX callback parsing error: {str(e)}")

def sax_example():
    """Example usage of SAX parser"""
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
    
    # Regular parsing
    result = parse_with_sax(xml)
    print("SAX Parsing Result:")
    print(result)
    
    # Callback-based parsing
    print("\nSAX Callback Processing:")
    elements = []
    def element_handler(name, attrs, text):
        if text:  # Only process elements with text
            element_info = f"{name}: {text}"
            if attrs:
                attrs_str = ", ".join([f"{k}={v}" for k, v in attrs.items()])
                element_info += f" (attrs: {attrs_str})"
            elements.append(element_info)
    
    parse_with_sax_callback(xml, element_handler)
    for element in elements:
        print(f"- {element}")
        
    return result
