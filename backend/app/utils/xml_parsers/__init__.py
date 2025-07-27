"""
XML Parsers Module
This module provides multiple XML parsing techniques.
"""

from .dom_parser import parse_with_dom
from .sax_parser import parse_with_sax
from .etree_parser import parse_with_etree

__all__ = [
    'parse_with_dom',     # DOM-based parsing (equivalent to XmlDocument)
    'parse_with_sax',     # SAX/Pull parsing (equivalent to XmlReader)
    'parse_with_etree'    # ElementTree parsing (similar to LINQ to XML)
]
