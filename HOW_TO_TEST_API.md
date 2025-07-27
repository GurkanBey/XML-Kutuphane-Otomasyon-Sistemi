# How to Test the API Functions from the Backend

This guide explains how to test the XML-based API functions for the library application. These tests can be performed directly from the backend, without needing to use the frontend.

## 1. Starting the Server

Before running any tests, you need to start the backend server:

```
cd c:\Users\Parlak\Desktop\XML1\backend
python run.py
```

This will start the Flask server at http://localhost:5000.

## 2. Test Using the Command-Line Tool (api_test.py)

The quickest way to test the API is using the `api_test.py` script. It provides colorized output and supports testing individual endpoints.

### Prerequisites

Install the required dependencies:

```
pip install requests colorama
```

### Testing Specific Endpoints

Open a new command prompt (while the server is running) and run:

```
cd c:\Users\Parlak\Desktop\XML1\backend
python tests\api_test.py --test [test-name]
```

Available test options:
- `login` - Tests the API v1 login function
- `books` - Tests the API v1 book listing function
- `endpoints` - Tests the API v1 endpoints listing function
- `add-book` - Tests the API v1 book addition function (requires admin credentials)
- `weather` - Tests the API v1 weather function
- `api-v2-info` - Tests the API v2 info function

### Testing All Endpoints at Once

To run all tests:

```
python tests\api_test.py
```

or

```
python tests\api_test.py --test all
```

### Testing with Different Credentials

To test with specific user credentials:

```
python tests\api_test.py --username student --password student123
```

## 3. Test Using the Unittest Framework (test_api_unittest.py)

For more structured testing with assertions:

```
cd c:\Users\Parlak\Desktop\XML1\backend
python -m unittest tests.test_api_unittest
```

This will run all test cases in the file. To run a specific test case:

```
python -m unittest tests.test_api_unittest.TestLoginAPI
```

## 4. Test Using Postman

If you prefer a GUI tool for testing APIs:

1. Install [Postman](https://www.postman.com/downloads/)
2. Import the collection file: `backend/tests/postman_collection.json`
3. Run the requests in the imported collection

## 5. Manual API Testing

You can also manually test endpoints using curl or similar tools:

### Login Example

```
curl -X POST http://localhost:5000/api/v1/login 
  -H "Content-Type: application/xml" 
  -d "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
      <login>
        <username>admin</username>
        <password>admin123</password>
      </login>"
```

### Getting Books (Requires Token)

First get a token using the login request, then:

```
curl http://localhost:5000/api/v1/books 
  -H "Content-Type: application/xml" 
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 6. API Endpoints Reference

| Endpoint | Method | Description | Auth Required | Role |
|----------|--------|-------------|--------------|------|
| `/api/v1/login` | POST | Login endpoint that returns a JWT token | No | Any |
| `/api/v1/logout` | POST | Logout endpoint | No | Any |
| `/api/v1/endpoints` | GET | List all available API v1 endpoints | No | Any |
| `/api/v1/books` | GET | Get all books | Yes | Student/Admin |
| `/api/v1/books/<id>` | GET | Get a specific book by ID | Yes | Student/Admin |
| `/api/v1/books` | POST | Add a new book | Yes | Admin only |
| `/api/v1/books/<id>` | PUT | Update an existing book | Yes | Admin only |
| `/api/v1/books/<id>` | DELETE | Delete a book | Yes | Admin only |
| `/api/v1/weather` | GET | Get weather data from external XML service | Yes | Student/Admin |
| `/api/v2/info` | GET | Simple endpoint with basic API info | No | Any |

## 7. XML Response Format

All API responses follow a consistent XML structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
  <status>success|error</status>
  <message>Descriptive message</message>
  <data>
    <!-- Response data goes here -->
  </data>
</response>
```

## 8. Troubleshooting

1. **Server Connection Issues**: Make sure the Flask server is running before running tests
2. **Authentication Errors**: Verify you're using the correct username/password
3. **XML Format Errors**: Ensure your XML follows the correct schema defined in app/schemas
