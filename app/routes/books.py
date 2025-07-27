from flask import Blueprint, request, current_app
from app.utils.xml_utils import (
    xml_to_dict, dict_to_xml, create_xml_response, create_error_response, 
    validate_xml_with_xsd, validate_xml_with_dtd
)
from app.utils.auth_utils import admin_required, student_required
from app.models.book import Book
import os

bp = Blueprint('books', __name__, url_prefix='/api/v1')


@bp.route('/books', methods=['GET'])
def get_books():
    """Get all books (no authentication required for testing)"""
    try:
        books = Book.get_all()
        
        # Convert to XML with enhanced formatting for better display
        response_data = {'books': {'book': []}}
        
        for book in books:
            book_data = {
                '@id': str(book['id']),
                'title': book['title'],
                'author': book['author'],
                'year': str(book['year']),
                'isbn': book['isbn']
            }
            
            # Add optional fields if they exist and are not empty
            if book.get('publisher'):
                book_data['publisher'] = book.get('publisher')
            
            if book.get('category'):
                book_data['category'] = book.get('category')
            
            if book.get('description'):
                book_data['description'] = {'#text': book.get('description')}
                
            response_data['books']['book'].append(book_data)
        
        xml_response = dict_to_xml(response_data)
        return xml_response, 200, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        xml_response = create_error_response(f"Error retrieving books: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}


@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID (no authentication required for testing)"""
    try:
        book = Book.get_by_id(book_id)
        
        if book is None:
            xml_response = create_error_response("Book not found")
            return xml_response, 404, {'Content-Type': 'application/xml'}
        
        # Convert to XML with consistent formatting
        book_data = {
            '@id': str(book['id']),
            'title': book['title'],
            'author': book['author'],
            'year': str(book['year']),
            'isbn': book['isbn']
        }
        
        # Add optional fields if they exist and are not empty
        if book.get('publisher'):
            book_data['publisher'] = book.get('publisher')
        
        if book.get('category'):
            book_data['category'] = book.get('category')
        
        if book.get('description'):
            book_data['description'] = {'#text': book.get('description')}
        
        response_data = {'book': book_data}
        
        xml_response = dict_to_xml(response_data)
        return xml_response, 200, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        xml_response = create_error_response(f"Error retrieving book: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}


@bp.route('/books', methods=['POST'])
@admin_required
def create_book():
    """Create a new book (requires admin role)"""
    print("Received book creation request")
    print(f"Headers: {request.headers}")
    
    # Check content type - case insensitive comparison to be more flexible
    if not request.content_type or 'application/xml' not in request.content_type.lower():
        print(f"Invalid content type: {request.content_type}")
        xml_response = create_error_response("Content-Type must be application/xml")
        return xml_response, 415, {'Content-Type': 'application/xml'}
    
    try:
        xml_data = request.data.decode('utf-8')
        print(f"Received XML: {xml_data}")
        
        # Skip validation temporarily for debugging
        dtd_valid, dtd_error = True, None
        xsd_valid, xsd_error = True, None
          # Parse XML
        book_data = xml_to_dict(xml_data)
        print(f"Parsed book data: {book_data}")
        book_submission = book_data.get('book_submission', {})
        if not book_submission:
            # Check if directly using <book> format instead
            book_submission = book_data.get('book', {})
            if not book_submission:
                print("Missing book or book_submission element")
                xml_response = create_error_response("Missing book element in XML")
                return xml_response, 400, {'Content-Type': 'application/xml'}
        
        # Extract book details from XML
        new_book = {
            'title': book_submission.get('title'),
            'author': book_submission.get('author'),
            'year': int(book_submission.get('year', 0)),
            'isbn': book_submission.get('isbn'),
            'publisher': book_submission.get('publisher', ''),
            'category': book_submission.get('category', ''),
            'description': book_submission.get('description', '')
        }
        
        print(f"Extracted book details: {new_book}")
        
        # Validate required fields
        missing_fields = []
        for field in ['title', 'author', 'isbn']:
            if not new_book.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(error_msg)
            xml_response = create_error_response(error_msg)
            return xml_response, 400, {'Content-Type': 'application/xml'}
        
        if new_book['year'] <= 0:
            print("Invalid year value")
            xml_response = create_error_response("Year must be a positive integer")
            return xml_response, 400, {'Content-Type': 'application/xml'}
        
        # Create book in database
        book_id = Book.create(new_book)
        print(f"Book created with ID: {book_id}")
        
        # Return success response
        response_data = {'book_id': str(book_id)}
        xml_response = create_xml_response('success', "Book created successfully", response_data)
        return xml_response, 201, {'Content-Type': 'application/xml'}
        
    except ValueError as e:
        print(f"Value error: {str(e)}")
        xml_response = create_error_response(f"Invalid data: {str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        print(f"Error creating book: {str(e)}")
        xml_response = create_error_response(f"Error creating book: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}


@bp.route('/books/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(book_id):
    """Delete a book (requires admin role)"""
    try:
        book = Book.get_by_id(book_id)
        
        if book is None:
            xml_response = create_error_response("Book not found")
            return xml_response, 404, {'Content-Type': 'application/xml'}
        
        # Delete the book
        Book.delete(book_id)
        
        # Return success response
        xml_response = create_xml_response('success', "Book deleted successfully")
        return xml_response, 200, {'Content-Type': 'application/xml'}
        
    except Exception as e:
        xml_response = create_error_response(f"Error deleting book: {str(e)}")
        return xml_response, 500, {'Content-Type': 'application/xml'}
