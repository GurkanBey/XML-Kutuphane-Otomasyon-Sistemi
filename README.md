# XML Library System

This project is a complete XML-based library automation system demonstrating various XML technologies including validation, transformation, and parsing techniques. The system features a full-featured RESTful API powered by Python Flask and a responsive frontend interface.

## Features

- **XML-Based Communication**: All system communication is XML-based, demonstrating XML as a viable alternative to JSON
- **XML Processing**: Support for multiple XML parsing techniques (DOM, SAX, ElementTree)
- **XML Validation**: DTD and XSD schema validation for data integrity
- **XML Transformation**: XPath queries and XSLT transformations
- **Authentication**: JWT token-based authentication with role-based access control
- **Modern Frontend**: Responsive design with book management and API testing interfaces
- **Comprehensive Testing**: Tools for API and feature testing

## Table of Contents
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Feature Overview](#feature-overview)
- [API Documentation](#api-documentation)
- [XML Technologies](#xml-technologies)
- [Testing Guide](#testing-guide)
- [User Credentials](#user-credentials)

## Project Structure

```
XML1/
├── backend/
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # XML validation schemas (DTD/XSD)
│   │   ├── services/       # External services
│   │   ├── stylesheets/    # XSLT templates
│   │   ├── utils/          # XML utilities and parsers
│   │   └── __init__.py
│   ├── instance/           # SQLite database
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Application entry point
│   └── tests/             # API tests
├── frontend/
│   ├── admin/             # Admin interface
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── index.html         # Main entry page
├── examples/              # Sample XML and code examples
└── API_DOCUMENTATION.md   # Detailed API documentation
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the application:
   ```
   python run.py
   ```

### Frontend Setup

1. Open `frontend/index.html` in your browser or use a local server:
   ```
   cd frontend
   ```

2. If you have Python installed:
   ```
   python -m http.server
   ```

3. Access the application at `http://localhost:8000`



## Feature Overview

### User Management
- Login and authentication using JWT tokens
- Role-based access control (Admin and Student roles)
- Token-based authentication for API endpoints

### Book Management
- View all books in library
- Add new books (Admin only)
- Delete books (Admin only)
- View detailed book information

### API Testing Interface
- Interactive API testing tool
- Test all API endpoints from a user-friendly interface
- View raw XML responses and formatted results

### XML Features
- **XML Parsing**: Test and compare different parsing methods
- **XPath**: Execute XPath queries on XML data
- **XSLT**: Transform XML to other formats (HTML, text, simplified XML)
- **Validation**: Validate XML against DTD and XSD schemas

## API Documentation

### Authentication
- `POST /api/v1/auth/login`: Authenticate user
- `POST /api/v1/auth/register`: Register new user (Admin only)

### Books
- `GET /api/v1/books`: Get all books
- `GET /api/v1/books/{id}`: Get book by ID
- `POST /api/v1/books`: Add new book (Admin only)
- `DELETE /api/v1/books/{id}`: Delete book (Admin only)

### XML Processing
- `POST /api/v1/parsing/methods`: Test different XML parsing methods
- `POST /api/v1/transform/xpath`: Execute XPath queries
- `POST /api/v1/transform/xslt`: Apply XSLT transformations
- `POST /api/v1/validate/dtd`: Validate XML using DTD
- `POST /api/v1/validate/xsd`: Validate XML using XSD

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## XML Technologies

### Why XML over JSON?
- **Validation**: XML provides stronger validation through DTD and XSD
- **Transformations**: XML supports document transformations via XSLT
- **Querying**: Enhanced querying capabilities with XPath
- **Namespaces**: Better categorization and organization of data
- **Legacy Support**: Greater compatibility with older systems

### XML Parsing Techniques
- **DOM Parser**: Loads entire XML document into memory
- **SAX Parser**: Event-based parser for lower memory footprint
- **ElementTree**: Python's efficient XML API with query-like operations

For more details, see [XML_PARSING_TECHNIQUES.md](XML_PARSING_TECHNIQUES.md).

### XML Transformation
- **XPath**: Query language for selecting nodes from XML documents
- **XSLT**: Language for transforming XML into other formats

For detailed usage, see [HOW_TO_USE_XML_TRANSFORMATION.md](HOW_TO_USE_XML_TRANSFORMATION.md).

## Testing Guide

### API Testing Methods
1. **Command-Line Tool**:
   ```bash
   cd backend
   python tests/api_test.py --test all
   ```

   Available test options:
   - `login`: Test authentication
   - `books`: Test book listing
   - `endpoints`: Test API endpoints listing
   - `add-book`: Test adding new books (admin only)
   - `xpath`: Test XPath querying
   - `xslt`: Test XSLT transformations
   - `transform-examples`: Test XML transformation examples
   
   Example:
   ```bash
   python tests/api_test.py --test xpath --username admin --password admin123
   ```

2. **Web Interface**:
   Open `frontend/admin/api_test.html` in your browser

3. **Unittest Framework**:
   ```bash
   cd backend
   python -m unittest tests.test_api_unittest
   ```

4. **Postman**:
   Import `backend/tests/postman_collection.json`

For a comprehensive testing guide, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

## User Credentials

### Admin User
- **Username**: admin
- **Password**: admin123
- **Permissions**: Full access to all features

### Student User
- **Username**: student
- **Password**: student123
- **Permissions**: Limited to viewing books and using XML transformations

## License

This project is licensed under the MIT License.
