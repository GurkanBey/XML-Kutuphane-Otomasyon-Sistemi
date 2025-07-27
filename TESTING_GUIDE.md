# XML Library Testing Guide

This comprehensive guide documents all testable features of the XML Library system, including API endpoints, XML functionalities, and frontend features.

## Table of Contents
- [Authentication Testing](#authentication-testing)
- [Books API Testing](#books-api-testing)
- [XML Transformation Testing](#xml-transformation-testing)
  - [XPath Testing](#xpath-testing)
  - [XSLT Testing](#xslt-testing)
- [XML Validation Testing](#xml-validation-testing)
- [API Testing Interface](#api-testing-interface)
- [Frontend Testing](#frontend-testing)
- [Automated Testing](#automated-testing)
- [Sample Test Data](#sample-test-data)

---

## Authentication Testing

### Login Testing

**Endpoint:** `POST /api/v1/login`

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><login><username>admin</username><password>admin123</password></login>' \
  http://localhost:5000/api/v1/login
```

**Test using Frontend:**
1. Open `frontend/index.html`
2. Enter username: `admin`, password: `admin123`
3. Click Login button
4. Verify JWT token appears in the header

**Expected Response:**
```xml
<response>
  <status>success</status>
  <message>Authentication successful</message>
  <data>
    <token>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...</token>
    <user>
      <username>admin</username>
      <role>admin</role>
    </user>
  </data>
</response>
```

### Test Student Login

```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><login><username>student</username><password>student123</password></login>' \
  http://localhost:5000/api/v1/login
```

### Test Invalid Login

```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?><login><username>wrong</username><password>wrong</password></login>' \
  http://localhost:5000/api/v1/login
```

Expected: Error response with 401 status code

---

## Books API Testing

### Get All Books

**Endpoint:** `GET /api/v1/books`

**Test using cURL:**
```bash
curl -X GET \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/books
```

**Test using Frontend:**
1. Login as admin or student
2. Books will automatically load on dashboard
3. Click on any book to view its XML structure

**Expected Response:**
```xml
<response>
  <books>
    <book id="1">
      <title>To Kill a Mockingbird</title>
      <author>Harper Lee</author>
      <year>1960</year>
      <isbn>978-0446310789</isbn>
      <publisher>Grand Central Publishing</publisher>
      <category>Fiction</category>
    </book>
    <!-- More books -->
  </books>
</response>
```

### Get Book by ID

**Endpoint:** `GET /api/v1/books/{id}`

**Test using cURL:**
```bash
curl -X GET \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/books/1
```

**Test using API Test Interface:**
1. Login as admin
2. Click "API Test Panel"
3. Select "Books Management" tab
4. Enter Book ID (e.g., 1) in the "Get Book by ID" section
5. Click "Send Request"

### Add New Book (Admin only)

**Endpoint:** `POST /api/v1/books`

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<book>
  <title>The Great Gatsby</title>
  <author>F. Scott Fitzgerald</author>
  <year>1925</year>
  <isbn>978-0743273565</isbn>
  <publisher>Scribner</publisher>
  <category>Fiction</category>
  <description>A novel of the Jazz Age</description>
</book>' \
  http://localhost:5000/api/v1/books
```

**Test using Frontend:**
1. Login as admin
2. Click "Add New Book" button
3. Fill in book details
4. Submit the form

### Delete Book (Admin only)

**Endpoint:** `DELETE /api/v1/books/{id}`

**Test using cURL:**
```bash
curl -X DELETE \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/books/1
```

**Test using Frontend:**
1. Login as admin
2. View books list
3. Click "Delete" on a book
4. Confirm deletion

---

## XML Transformation Testing

### XPath Testing

**Endpoint:** `POST /api/v1/transform/xpath`

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<request>
  <xpath>//book/title/text()</xpath>
  <content>
    <library>
      <books>
        <book id="1">
          <title>To Kill a Mockingbird</title>
          <author>Harper Lee</author>
          <year>1960</year>
        </book>
        <book id="2">
          <title>1984</title>
          <author>George Orwell</author>
          <year>1949</year>
        </book>
      </books>
    </library>
  </content>
</request>' \
  http://localhost:5000/api/v1/transform/xpath
```

**Test using Automated Script:**
```bash
cd backend
python tests/api_test.py --test xpath
```

**Expected Response:**
```xml
<xpath-result>
  <expression>//book/title/text()</expression>
  <results>
    <item>To Kill a Mockingbird</item>
    <item>1984</item>
  </results>
</xpath-result>
```

### Test Different XPath Expressions

Try these different XPath expressions:
- `//book[@id="1"]/title/text()` - Get title of book with id=1
- `count(//book)` - Count number of books
- `//book[contains(author, "Orwell")]/title/text()` - Get titles of books by Orwell
- `//book[year>1950]/title/text()` - Get titles of books published after 1950

### XSLT Testing

**Endpoint:** `POST /api/v1/transform/xslt`

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<request>
  <stylesheet-type>html</stylesheet-type>
  <content>
    <library>
      <books>
        <book id="1">
          <title>To Kill a Mockingbird</title>
          <author>Harper Lee</author>
          <year>1960</year>
          <isbn>978-0446310789</isbn>
          <publisher>Grand Central Publishing</publisher>
          <category>Fiction</category>
        </book>
      </books>
    </library>
  </content>
</request>' \
  http://localhost:5000/api/v1/transform/xslt
```

**Test using Automated Script:**
```bash
cd backend
python tests/api_test.py --test xslt
```

**Expected Response:** HTML content representing the books

### Test Different XSLT Transformations

Try these different stylesheet types:
- `html` - Transform to HTML table
- `text` - Transform to plain text format
- `simplified` - Transform to simplified XML structure

---

## XML Validation Testing

**Endpoint:** `POST /api/v1/validate`

### Validate against DTD

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book SYSTEM "http://localhost:5000/api/v1/schemas/book.dtd">
<book id="1">
  <title>To Kill a Mockingbird</title>
  <author>Harper Lee</author>
  <year>1960</year>
  <isbn>978-0446310789</isbn>
  <publisher>Grand Central Publishing</publisher>
  <category>Fiction</category>
</book>' \
  "http://localhost:5000/api/v1/validate?schema_type=dtd"
```

### Validate against XSD

**Test using cURL:**
```bash
curl -X POST \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<book xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
     xsi:noNamespaceSchemaLocation="http://localhost:5000/api/v1/schemas/book.xsd" 
     id="1">
  <title>To Kill a Mockingbird</title>
  <author>Harper Lee</author>
  <year>1960</year>
  <isbn>978-0446310789</isbn>
  <publisher>Grand Central Publishing</publisher>
  <category>Fiction</category>
</book>' \
  "http://localhost:5000/api/v1/validate?schema_type=xsd"
```

**Test using API Test Interface:**
1. Login as admin
2. Open API Test Panel
3. Go to "Info & Utilities" tab
4. Choose schema type (DTD or XSD) in the "Validate XML" section
5. Enter XML to validate
6. Send request

---

## API Testing Interface

The admin panel includes a dedicated API testing interface:

### Access API Test Interface
1. Login as admin
2. Click "API Test Panel" button
3. Use the left sidebar to navigate between API categories

### Test Authentication Endpoints
1. Select "Authentication" tab
2. Enter login credentials
3. Send login request
4. Verify token is returned

### Test Books Management Endpoints
1. Select "Books Management" tab
2. Test each endpoint:
   - Get All Books
   - Get Book by ID
   - Add Book
   - Delete Book

### Test XML Transformation Endpoints
1. Select "XML Transformation" tab
2. Test XPath transformation with different expressions
3. Test XSLT transformation with different stylesheets

### Test Utilities
1. Select "Info & Utilities" tab
2. Test XML validation against DTD and XSD
3. Get API information
4. View available endpoints

---

## Frontend Testing

### Authentication Features
- Login as admin (username: admin, password: admin123)
- Login as student (username: student, password: student123)
- Observe JWT token display in header
- Test logout functionality
- Test invalid credentials

### Admin Dashboard Features
- View list of books
- Add new book
- Delete existing book
- View book details
- Access API Test Panel
- View API information

### Student Dashboard Features
- View list of books
- View book details
- View API information

### Book XML Popup Feature
- Click on a book card to see its XML representation
- Use "View XML" button to see XML representation
- Test copying XML content
- Close modal using X button or clicking outside

---

## Automated Testing

### Using the API Test Script

The project includes an automated API testing script that can be used to verify different functionalities:

```bash
cd backend
python tests/api_test.py --test [test_name]
```

Available test options:
- `all` - Run all tests
- `login` - Test user authentication
- `books` - Test book listing
- `endpoints` - Test API endpoints listing
- `add-book` - Test book creation
- `xpath` - Test XPath transformation
- `xslt` - Test XSLT transformation
- `transform-examples` - Test transformation examples listing

### Custom Test Parameters
```bash
python tests/api_test.py --test login --username admin --password admin123
```

---

## Sample Test Data

### Sample Login XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<login>
  <username>admin</username>
  <password>admin123</password>
</login>
```

### Sample Book XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book>
  <title>The Great Gatsby</title>
  <author>F. Scott Fitzgerald</author>
  <year>1925</year>
  <isbn>978-0743273565</isbn>
  <publisher>Scribner</publisher>
  <category>Fiction</category>
  <description>A novel of the Jazz Age</description>
</book>
```

### Sample XPath Request
```xml
<?xml version="1.0" encoding="UTF-8"?>
<request>
  <xpath>//book/title/text()</xpath>
  <content>
    <library>
      <books>
        <book id="1">
          <title>To Kill a Mockingbird</title>
          <author>Harper Lee</author>
          <year>1960</year>
        </book>
        <book id="2">
          <title>1984</title>
          <author>George Orwell</author>
          <year>1949</year>
        </book>
      </books>
    </library>
  </content>
</request>
```

### Sample XSLT Request
```xml
<?xml version="1.0" encoding="UTF-8"?>
<request>
  <stylesheet-type>html</stylesheet-type>
  <content>
    <library>
      <books>
        <book id="1">
          <title>To Kill a Mockingbird</title>
          <author>Harper Lee</author>
          <year>1960</year>
          <isbn>978-0446310789</isbn>
        </book>
      </books>
    </library>
  </content>
</request>
```

---

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify you're using the correct credentials
   - Check that the token hasn't expired
   - Ensure you're including "Bearer " prefix before your token

2. **XML Parsing Errors**
   - Validate your XML for well-formedness
   - Check that all tags are properly closed
   - Ensure proper XML declaration

3. **Server Connection Issues**
   - Verify the backend server is running on port 5000
   - Check for any error messages in the server console

4. **CORS Issues**
   - If testing from a different domain, CORS may block requests
   - The backend has CORS enabled for localhost development

5. **XPath/XSLT Errors**
   - Verify XPath expression syntax
   - Check that your XML content is well-formed
   - Ensure XSLT stylesheet type is valid (html, text, or simplified)
