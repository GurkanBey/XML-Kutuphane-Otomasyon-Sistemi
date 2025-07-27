# How to Run the API Tests

This document provides instructions for running the API tests for the XML Library project.

## Prerequisites

1. Make sure the backend server is running (on http://localhost:5000)
2. Ensure you have the required Python packages installed:
   - requests
   - colorama
   - lxml

## Running the Tests

Navigate to the `backend` directory and run the test script using Python:

```bash
cd backend
python tests/api_test.py --test [test_name]
```

## Available Test Options

- `all` - Run all tests (default)
- `login` - Test user authentication
- `books` - Test book listing (requires login)
- `endpoints` - Test API endpoints listing
- `add-book` - Test book creation (requires admin login)
- `weather` - Test weather API (requires login)
- `api-v2-info` - Test API v2 info endpoint
- `xpath` - Test XPath transformation (requires login)
- `xslt` - Test XSLT transformation (requires login)
- `transform-examples` - Test transformation examples listing

## Examples

1. Run all tests:
```bash
python tests/api_test.py
```

2. Run XPath transformation test:
```bash
python tests/api_test.py --test xpath
```

3. Run XSLT transformation test:
```bash
python tests/api_test.py --test xslt
```

4. Run login test with custom credentials:
```bash
python tests/api_test.py --test login --username admin --password admin123
```

## Troubleshooting

If you encounter errors:

1. Make sure the backend server is running on http://localhost:5000
2. Check that you have admin privileges for tests that require admin access
3. Verify that the XML transformation endpoints are properly configured

For the XPath and XSLT tests, the script will automatically attempt to login and obtain a token.
