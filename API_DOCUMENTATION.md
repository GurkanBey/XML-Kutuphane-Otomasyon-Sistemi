# XML Library API Documentation

This document provides comprehensive information about all API endpoints available in the XML Library application.

## Table of Contents
1. [Authentication](#authentication)
2. [Books Management](#books-management)
3. [Info and Utilities](#info-and-utilities)

## Base URL

All API endpoints are available at the base URL: `http://localhost:5000/api/v1/`

---

## Authentication

### Login

Authenticates a user and returns a JWT token.

- **URL**: `/auth/login`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: None required

**Request Body**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<login>
    <username>admin</username>
    <password>adminpass</password>
</login>
```

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<authentication>
    <status>success</status>
    <token>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...</token>
    <user>
        <id>1</id>
        <username>admin</username>
        <role>admin</role>
    </user>
</authentication>
```

### Register

Registers a new user.

- **URL**: `/auth/register`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Admin token required

**Request Body**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<register>
    <username>newuser</username>
    <password>password123</password>
    <role>student</role>
</register>
```

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<registration>
    <status>success</status>
    <message>User registered successfully</message>
    <user>
        <id>3</id>
        <username>newuser</username>
        <role>student</role>
    </user>
</registration>
```

---

## Books Management

### Get All Books

Retrieves all books in the library.

- **URL**: `/books`
- **Method**: `GET`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
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
        <book id="2">
            <title>1984</title>
            <author>George Orwell</author>
            <year>1949</year>
            <isbn>978-0451524935</isbn>
            <publisher>Signet Classic</publisher>
            <category>Dystopian</category>
        </book>
        <!-- More books... -->
    </books>
</library>
```

### Get Book by ID

Retrieves a specific book by its ID.

- **URL**: `/books/{id}`
- **Method**: `GET`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book id="1">
    <title>To Kill a Mockingbird</title>
    <author>Harper Lee</author>
    <year>1960</year>
    <isbn>978-0446310789</isbn>
    <publisher>Grand Central Publishing</publisher>
    <category>Fiction</category>
</book>
```

### Add Book

Adds a new book to the library.

- **URL**: `/books`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Admin token required

**Request Body**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<book>
    <title>The Great Gatsby</title>
    <author>F. Scott Fitzgerald</author>
    <year>1925</year>
    <isbn>978-0743273565</isbn>
    <publisher>Scribner</publisher>
    <category>Fiction</category>
</book>
```

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>success</status>
    <message>Book added successfully</message>
    <book id="3">
        <title>The Great Gatsby</title>
        <author>F. Scott Fitzgerald</author>
        <year>1925</year>
        <isbn>978-0743273565</isbn>
        <publisher>Scribner</publisher>
        <category>Fiction</category>
    </book>
</response>
```

### Delete Book

Deletes a book from the library.

- **URL**: `/books/{id}`
- **Method**: `DELETE`
- **Content-Type**: `application/xml`
- **Authorization**: Admin token required

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <status>success</status>
    <message>Book deleted successfully</message>
</response>
```

---

## XML Transformation

### XPath Transformation

Extracts data from XML using XPath expressions.

- **URL**: `/transform/xpath`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token

**Request Body**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<transform>
    <xpath>//book[year>1950]/title/text()</xpath>
    <xml>
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
    </xml>
</transform>
```

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xpath-results>
    <expression>//book[year>1950]/title/text()</expression>
    <matches>
        <match>To Kill a Mockingbird</match>
    </matches>
</xpath-results>
```

### XSLT Transformation

Transforms XML using XSLT stylesheets.

- **URL**: `/transform/xslt`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token

**Request Body**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<transform>
    <stylesheet-name>books_to_html</stylesheet-name>
    <xml>
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
    </xml>
</transform>
```

**Response**:
```xml
<html>
  <head>
    <title>Book List</title>
  </head>
  <body>
    <h1>Library Books</h1>
    <table border="1">
      <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Author</th>
        <th>Year</th>
      </tr>
      <tr>
        <td>1</td>
        <td>To Kill a Mockingbird</td>
        <td>Harper Lee</td>
        <td>1960</td>
      </tr>
      <tr>
        <td>2</td>
        <td>1984</td>
        <td>George Orwell</td>
        <td>1949</td>
      </tr>
    </table>
  </body>
</html>
```

### Get Available Stylesheets

Retrieves a list of available XSLT stylesheets.

- **URL**: `/transform/stylesheets`
- **Method**: `GET`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<stylesheets>
    <stylesheet>
        <name>books_to_html</name>
        <description>Transforms books XML to HTML table</description>
    </stylesheet>
    <stylesheet>
        <name>books_to_text</name>
        <description>Transforms books XML to plain text</description>
    </stylesheet>
    <stylesheet>
        <name>books_to_simplified</name>
        <description>Transforms books XML to simplified XML</description>
    </stylesheet>
</stylesheets>
```

---

## XML Parsing

### Parse with All Methods

Parses XML using multiple parsing techniques.

- **URL**: `/parsing/methods`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Student or Admin token required

**Request Body**: Any valid XML document

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<parsing-methods-results>
  <summary>
    <total-time-ms>15.23</total-time-ms>
  </summary>
  <methods>
    <method>
      <name>dom</name>
      <type>DOM-based (XmlDocument equivalent)</type>
      <status>success</status>
      <time-ms>5.12</time-ms>
      <description>Loads entire document into memory as a tree, good for random access</description>
    </method>
    <method>
      <name>sax</name>
      <type>SAX/Pull parsing (XmlReader equivalent)</type>
      <status>success</status>
      <time-ms>4.87</time-ms>
      <description>Event-based, sequential parsing, memory efficient</description>
    </method>
    <method>
      <name>etree</name>
      <type>ElementTree (LINQ to XML equivalent)</type>
      <status>success</status>
      <time-ms>5.24</time-ms>
      <description>Pythonic API, good balance between features and performance</description>
    </method>
  </methods>
  <recommendations>
    <note>DOM: Best for small documents with random access needs</note>
    <note>SAX: Best for large documents with low memory requirements</note>
    <note>ElementTree: Good balance for most general XML processing</note>
  </recommendations>
</parsing-methods-results>
```

### Performance Comparison

Compares performance of different XML parsing techniques.

- **URL**: `/parsing/performance`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Student or Admin token required
- **Query Parameters**: `repeat` (optional, default: 50) - Number of iterations for performance test

**Request Body**: Any valid XML document

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<parsing-performance-results>
  <summary>
    <repeat-count>50</repeat-count>
  </summary>
  <methods>
    <method>
      <name>dom</name>
      <time-ms>0.2345</time-ms>
      <memory-note>Highest memory usage, loads entire document</memory-note>
    </method>
    <method>
      <name>sax</name>
      <time-ms>0.1876</time-ms>
      <memory-note>Low memory usage, sequential access only</memory-note>
    </method>
    <method>
      <name>etree</name>
      <time-ms>0.2153</time-ms>
      <memory-note>Moderate memory usage, good balance</memory-note>
    </method>
    <method>
      <name>sax_callback</name>
      <time-ms>0.1654</time-ms>
      <memory-note>Lowest memory usage, best for very large documents</memory-note>
    </method>
  </methods>
  <fastest-method>sax_callback</fastest-method>
</parsing-performance-results>
```

---

## External Services

### Weather Information

Retrieves current weather information from an external service.

- **URL**: `/external/weather`
- **Method**: `GET`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token
- **Query Parameters**: `city` (required) - Name of the city

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<weather>
    <city>Istanbul</city>
    <temperature>25.5</temperature>
    <condition>Sunny</condition>
    <humidity>65</humidity>
    <wind_speed>12</wind_speed>
    <last_updated>2025-06-19T10:30:00Z</last_updated>
</weather>
```

---

## Info and Utilities

### API Information

Returns information about the API.

- **URL**: `/info`
- **Method**: `GET`
- **Content-Type**: `application/xml`
- **Authorization**: None required

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<api-info>
    <name>XML Library API</name>
    <version>1.0</version>
    <base-url>/api/v1</base-url>
    <description>API for XML processing and library management demonstration</description>
    <endpoints>
        <endpoint>
            <path>/auth/login</path>
            <methods>POST</methods>
            <description>Authentication endpoint</description>
        </endpoint>
        <!-- More endpoints... -->
    </endpoints>
</api-info>
```

### Validate XML

Validates an XML document against a schema (DTD or XSD).

- **URL**: `/validate`
- **Method**: `POST`
- **Content-Type**: `application/xml`
- **Authorization**: Any valid token
- **Query Parameters**: `schema_type` (required) - Either 'dtd' or 'xsd'

**Request Body**: Any XML document to validate

**Response**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<validation-result>
    <status>success</status>
    <message>XML document is valid according to the schema</message>
    <schema-type>xsd</schema-type>
</validation-result>
```

---

## Error Responses

All API endpoints return errors in a consistent XML format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<error>
    <status>error</status>
    <code>401</code>
    <message>Unauthorized: Invalid or missing token</message>
</error>
```

Common error codes:
- `400` Bad Request - Invalid request format or parameters
- `401` Unauthorized - Authentication required
- `403` Forbidden - Insufficient permissions
- `404` Not Found - Resource not found
- `415` Unsupported Media Type - Expected XML content
- `422` Unprocessable Entity - XML document is not valid
- `500` Internal Server Error - Server-side error

## Authentication

To authenticate API requests, include the JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
