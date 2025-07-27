"""
Parsing Methods Comparison Module
This module demonstrates and compares different XML parsing techniques.
"""

import time
import sys
from .dom_parser import parse_with_dom
from .sax_parser import parse_with_sax, parse_with_sax_callback
from .etree_parser import parse_with_etree

def performance_comparison(xml_string: str, repeat: int = 100) -> dict:
    """
    Compare performance of different parsing methods
    
    Args:
        xml_string: XML content to parse
        repeat: Number of times to repeat parsing for accurate measurement
        
    Returns:
        Dictionary with performance metrics
    """
    results = {}
    
    # DOM parsing (memory intensive, good for random access)
    start_time = time.time()
    for _ in range(repeat):
        parse_with_dom(xml_string)
    dom_time = (time.time() - start_time) / repeat
    
    # SAX parsing (memory efficient, sequential)
    start_time = time.time()
    for _ in range(repeat):
        parse_with_sax(xml_string)
    sax_time = (time.time() - start_time) / repeat
    
    # ElementTree parsing (balanced approach)
    start_time = time.time()
    for _ in range(repeat):
        parse_with_etree(xml_string)
    etree_time = (time.time() - start_time) / repeat
    
    # Callback-based SAX parsing (most memory efficient for large files)
    elements_found = 0
    def counter_callback(name, attrs, text):
        nonlocal elements_found
        elements_found += 1
    
    start_time = time.time()
    for _ in range(repeat):
        parse_with_sax_callback(xml_string, counter_callback)
    sax_callback_time = (time.time() - start_time) / repeat
    
    results = {
        'dom': dom_time,
        'sax': sax_time,
        'etree': etree_time,
        'sax_callback': sax_callback_time,
        'memory_notes': {
            'dom': 'Highest memory usage, loads entire document',
            'sax': 'Low memory usage, sequential access only',
            'etree': 'Moderate memory usage, good balance',
            'sax_callback': 'Lowest memory usage, best for very large documents'
        }
    }
    
    return results

def print_comparison_results(results: dict) -> None:
    """
    Print performance comparison results in a readable format
    
    Args:
        results: Dictionary with performance results
    """
    print("\n=== XML PARSING METHODS COMPARISON ===")
    print(f"DOM Parsing:       {results['dom']*1000:.4f} ms - {results['memory_notes']['dom']}")
    print(f"SAX Parsing:       {results['sax']*1000:.4f} ms - {results['memory_notes']['sax']}")
    print(f"ElementTree:       {results['etree']*1000:.4f} ms - {results['memory_notes']['etree']}")
    print(f"SAX w/ Callbacks:  {results['sax_callback']*1000:.4f} ms - {results['memory_notes']['sax_callback']}")
    
    # Determine fastest method
    fastest = min(results, key=lambda k: float('inf') if k.startswith('memory') else results[k])
    print(f"\nFastest method: {fastest.upper()} parsing")
    
    print("\nRecommendations:")
    print("- For small documents with random access needs: Use DOM")
    print("- For large documents with sequential processing: Use SAX with callbacks") 
    print("- For general-purpose XML processing with good performance: Use ElementTree")
    
def parse_all_methods_example(xml_string: str) -> dict:
    """
    Parse the same XML with all methods and compare results
    
    Args:
        xml_string: XML content to parse
        
    Returns:
        Dictionary with all parsing results
    """
    return {
        'dom': parse_with_dom(xml_string),
        'sax': parse_with_sax(xml_string),
        'etree': parse_with_etree(xml_string)
    }
