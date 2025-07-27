"""
XML Transformation Utility Module
This module provides utilities for XPath and XSLT transformations.
"""

from .xpath_utils import extract_with_xpath, get_book_titles, get_books_by_author, count_books
from .xslt_utils import transform_with_xslt

__all__ = [
    'extract_with_xpath',
    'get_book_titles',
    'get_books_by_author',
    'count_books',
    'transform_with_xslt'
]
