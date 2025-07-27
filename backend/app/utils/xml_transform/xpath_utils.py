"""
XPath Utility Module
This module provides utilities for navigating and extracting data from XML using XPath expressions.
"""

import lxml.etree as ET
from io import StringIO

def extract_with_xpath(xml_string, xpath_expr):
    """
    Extract data from XML using XPath expressions.
    
    Args:
        xml_string (str): XML content as string
        xpath_expr (str): XPath expression to evaluate
        
    Returns:
        list or str: Results of XPath evaluation
    """
    try:
        root = ET.fromstring(xml_string)
        results = root.xpath(xpath_expr)
        
        if isinstance(results, list):
            # Convert elements to string representation if needed
            return [ET.tostring(r, encoding='unicode').strip() if hasattr(r, 'tag') else str(r) for r in results]
        else:
            # Handle non-list results (like boolean, number, string)
            return str(results)
    except Exception as e:
        return f"XPath Error: {str(e)}"

def get_book_titles(xml_string):
    """
    Example: Get all book titles using XPath.
    
    Args:
        xml_string (str): XML content as string
        
    Returns:
        list: List of book titles
    """
    return extract_with_xpath(xml_string, "//book/title/text()")

def get_books_by_author(xml_string, author):
    """
    Example: Get books by a specific author using XPath.
    
    Args:
        xml_string (str): XML content as string
        author (str): Author name to search for
        
    Returns:
        list: List of book titles by the specified author
    """
    return extract_with_xpath(xml_string, f"//book[contains(author/text(), '{author}')]/title/text()")

def count_books(xml_string):
    """
    Example: Count total number of books using XPath.
    
    Args:
        xml_string (str): XML content as string
        
    Returns:
        int: Number of books in XML
    """
    return extract_with_xpath(xml_string, "count(//book)")

def get_books_after_year(xml_string, year):
    """
    Get books published after the specified year.
    
    Args:
        xml_string (str): XML content as string
        year (int): Year to filter by
        
    Returns:
        list: List of book titles published after the specified year
    """
    return extract_with_xpath(xml_string, f"//book[year > {year}]/title/text()")

def get_book_by_id(xml_string, book_id):
    """
    Get a book by its ID attribute.
    
    Args:
        xml_string (str): XML content as string
        book_id (str): ID of the book to find
        
    Returns:
        str: XML representation of the book
    """
    return extract_with_xpath(xml_string, f"//book[@id='{book_id}']")
