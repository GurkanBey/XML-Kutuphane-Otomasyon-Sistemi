// Admin API Test Interface
document.addEventListener('DOMContentLoaded', function() {
    // Base URL for API requests
    const API_BASE_URL = 'http://localhost:5000/api/v1';
    
    // Check if API server is online
    checkApiStatus();
    
    // Function to check if API server is online
    async function checkApiStatus() {
        try {
            const response = await fetch('http://localhost:5000/health', {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                headers: {
                    'Accept': 'application/xml, text/html, */*'
                }
            });
            
            if (response.ok) {
                console.log('API server is online');
                const statusDiv = document.createElement('div');
                statusDiv.className = 'api-status online';
                statusDiv.textContent = 'API Server: Online';
                document.querySelector('.api-categories').prepend(statusDiv);
            } else {
                throw new Error('API returned error status');
            }
        } catch (error) {
            console.error('API server is offline:', error);
            const statusDiv = document.createElement('div');
            statusDiv.className = 'api-status offline';
            statusDiv.textContent = 'API Server: Offline';
            if (document.querySelector('.api-categories')) {
                document.querySelector('.api-categories').prepend(statusDiv);
            }
            
            // Show a warning to the user
            alert('Warning: The API server appears to be offline. Make sure the backend server is running at http://localhost:5000');
        }
    }
    
    // Get token from localStorage
    const getToken = () => localStorage.getItem('token');
    
    // Handle category selection
    const categoryItems = document.querySelectorAll('.api-categories li');
    categoryItems.forEach(item => {
        item.addEventListener('click', () => {
            // Update active state
            document.querySelector('.api-categories li.active').classList.remove('active');
            item.classList.add('active');
            
            // Show selected category section
            const categoryId = item.getAttribute('data-category');
            document.querySelectorAll('.endpoint-section').forEach(section => {
                section.classList.add('hidden');
            });
            document.getElementById(categoryId).classList.remove('hidden');
        });
    });
    
    // Handle API request buttons
    const sendButtons = document.querySelectorAll('.send-btn');
    sendButtons.forEach(button => {
        button.addEventListener('click', () => {
            const endpoint = button.getAttribute('data-endpoint');
            sendApiRequest(endpoint);
        });
    });
    
    // Handle logout button
    document.getElementById('logoutBtn').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        alert('Logged out successfully!');
        window.location.href = '../index.html'; // Redirect to login page
    });
      // API request handler
    async function sendApiRequest(endpoint) {
        try {
            let url, method, body, headers = {
                'Content-Type': 'application/xml',
                'Accept': 'application/xml, text/html, */*'
            };
            
            // Add authorization header if token exists
            const token = getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            // Process different endpoints
            switch(endpoint) {
                case 'auth-login':
                    url = `${API_BASE_URL}/auth/login`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="auth-login"]').value;
                    break;
                    
                case 'auth-register':
                    url = `${API_BASE_URL}/auth/register`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="auth-register"]').value;
                    break;
                    
                case 'books-getall':
                    url = `${API_BASE_URL}/books`;
                    method = 'GET';
                    break;
                    
                case 'books-getbyid':
                    const bookId = document.getElementById('book-id').value;
                    url = `${API_BASE_URL}/books/${bookId}`;
                    method = 'GET';
                    break;
                    
                case 'books-add':
                    url = `${API_BASE_URL}/books`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="books-add"]').value;
                    break;
                    
                case 'books-delete':
                    const deleteId = document.getElementById('book-delete-id').value;
                    if (!deleteId) {
                        displayResponse(endpoint, false, 'Book ID is required for deletion');
                        return;
                    }
                    url = `${API_BASE_URL}/books/${deleteId}`;
                    method = 'DELETE';
                    break;
                    
                case 'transform-xpath':
                    url = `${API_BASE_URL}/transform/xpath`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="transform-xpath"]').value;
                    break;
                    
                case 'transform-xslt':
                    url = `${API_BASE_URL}/transform/xslt`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="transform-xslt"]').value;
                    break;
                    
                case 'transform-stylesheets':
                    url = `${API_BASE_URL}/transform/stylesheets`;
                    method = 'GET';
                    break;
                    
                case 'parsing-methods':
                    url = `${API_BASE_URL}/parsing/methods`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="parsing-methods"]').value;
                    break;
                    
                case 'parsing-performance':
                    const repeat = document.getElementById('parsing-repeat').value;
                    url = `${API_BASE_URL}/parsing/performance?repeat=${repeat}`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="parsing-performance"]').value;
                    break;
                    
                case 'external-weather':
                    const city = document.getElementById('weather-city').value;
                    url = `${API_BASE_URL}/external/weather?city=${encodeURIComponent(city)}`;
                    method = 'GET';
                    break;
                    
                case 'info-api':
                    url = `${API_BASE_URL}/info`;
                    method = 'GET';
                    break;
                    
                case 'info-validate':
                    const schemaType = document.getElementById('validate-schema-type').value;
                    url = `${API_BASE_URL}/validate?schema_type=${schemaType}`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="info-validate"]').value;
                    break;
                    
                default:
                    displayResponse(endpoint, false, 'Unknown endpoint');
                    return;
            }
            
            // Visual feedback that request is being sent
            const button = document.querySelector(`button[data-endpoint="${endpoint}"]`);
            const originalText = button.textContent;
            button.textContent = 'Sending...';
            button.disabled = true;
              // Configure the request
            const requestOptions = { 
                method, 
                headers,
                mode: 'cors',
                cache: 'no-cache'
            };
            
            if (body && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
                requestOptions.body = body;
            }
            
            // Log the request details for debugging
            console.log(`Making ${method} request to ${url}`);
            if (body) console.log('With body:', body);
            
            // Send the request
            const response = await fetch(url, requestOptions);
              // Get the response
            let responseText;
            const contentType = response.headers.get("content-type");
            console.log(`Response status: ${response.status}, Content-Type: ${contentType}`);
            
            try {
                responseText = await response.text();
                console.log('Response text:', responseText);
            } catch (err) {
                console.error('Error reading response:', err);
                responseText = `Error reading response: ${err.message}`;
            }
              // Store token if this was a login request
            if (endpoint === 'auth-login' && response.ok) {
                try {
                    const parser = new DOMParser();
                    const xmlDoc = parser.parseFromString(responseText, "text/xml");
                    const tokenElement = xmlDoc.getElementsByTagName("token")[0];
                    if (tokenElement) {
                        const token = tokenElement.textContent;
                        localStorage.setItem('token', token);
                        console.log('Token saved to localStorage');
                        
                        // Show a success message
                        alert('Login successful! Token has been stored.');
                    }
                } catch (err) {
                    console.error('Error processing auth token:', err);
                }
            }
            
            // Reset button
            button.textContent = originalText;
            button.disabled = false;
            
            // Display the response
            displayResponse(endpoint, response.ok, responseText, response.status);
              } catch (error) {
            console.error('Error making API request:', error);
            
            // More detailed error information
            let errorDetails = `Error: ${error.message}\n\n`;
            errorDetails += `URL: ${url}\n`;
            errorDetails += `Method: ${method}\n`;
            
            if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
                errorDetails += `\nThis could be due to:\n`;
                errorDetails += `- The API server is not running (http://localhost:5000)\n`;
                errorDetails += `- CORS policy is blocking the request\n`;
                errorDetails += `- Network connectivity issues\n\n`;
                errorDetails += `Please check that the backend server is running and accessible.`;
            }
            
            displayResponse(endpoint, false, errorDetails);
        }
    }
    
    // Display API response
    function displayResponse(endpoint, success, content, status) {
        const responseContainer = document.getElementById(`${endpoint}-response`);
        const responseStatus = responseContainer.querySelector('.response-status');
        const responseBody = responseContainer.querySelector('.response-body');
        
        // Set status message
        responseStatus.textContent = success 
            ? `Success! Status: ${status || 200}` 
            : `Error! Status: ${status || 'N/A'}`;
        responseStatus.className = `response-status ${success ? 'success' : 'error'}`;
        
        // Set response body
        responseBody.textContent = formatXml(content);
        responseBody.style.display = 'block';
    }
    
    // Format XML for better display
    function formatXml(xml) {
        try {
            if (!xml || typeof xml !== 'string') return xml;
            
            // Try to parse and pretty print if it's XML
            if (xml.trim().startsWith('<')) {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xml, "text/xml");
                
                // Check for parsing errors
                const parseError = xmlDoc.getElementsByTagName("parsererror")[0];
                if (parseError) {
                    // Not valid XML, return as is
                    return xml;
                }
                
                // Use XMLSerializer and some regex to prettify the XML
                const serializer = new XMLSerializer();
                let xmlText = serializer.serializeToString(xmlDoc);
                
                // Basic indentation for XML - more advanced would require a proper XML formatter
                xmlText = xmlText.replace(/></g, '>\n<');
                
                // Handle indentation levels
                let formatted = '';
                let indent = 0;
                xmlText.split('\n').forEach(line => {
                    line = line.trim();
                    if (line.match(/<\/.+>/)) {
                        indent--;
                    }
                    formatted += '  '.repeat(Math.max(0, indent)) + line + '\n';
                    if (line.match(/<[^\/].+>/) && !line.match(/\/>/)) {
                        indent++;
                    }
                });
                
                return formatted;
            } else {
                return xml;
            }
        } catch (e) {
            console.error("Error formatting XML:", e);
            return xml;  // Return original if formatting fails
        }
    }
});
