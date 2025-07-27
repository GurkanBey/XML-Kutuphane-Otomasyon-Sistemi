// Admin API Test Interface
document.addEventListener('DOMContentLoaded', function() {
    // Base URL for API requests
    const API_BASE_URL = 'http://localhost:5000/api/v1';
    
    // Check if API server is online
    setTimeout(checkApiStatus, 100); // Delay slightly to ensure DOM is ready
    
    // Function to check if API server is online
    async function checkApiStatus() {
        console.log('Checking API server status...');
        try {
            const response = await fetch('http://localhost:5000/health', {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
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
            
            // Add instructions for continuing anyway
            const retryDiv = document.createElement('div');
            retryDiv.className = 'api-retry';
            retryDiv.innerHTML = '<button id="retry-connection">Retry Connection</button> or continue testing with mock responses';
            if (document.querySelector('.api-categories')) {
                document.querySelector('.api-categories').append(retryDiv);
            }
            
            // Add retry functionality
            setTimeout(() => {
                const retryBtn = document.getElementById('retry-connection');
                if (retryBtn) {
                    retryBtn.addEventListener('click', checkApiStatus);
                }
            }, 100);
            
            // Show a warning to the user (but don't block with alert)
            console.warn('API server appears to be offline. Make sure the backend server is running at http://localhost:5000');
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
    
    // Handle API request buttons - using event delegation for reliability
    console.log('Setting up API request button handlers');
    document.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('send-btn')) {
            const endpoint = event.target.getAttribute('data-endpoint');
            console.log('Button clicked for endpoint:', endpoint);
            sendApiRequest(endpoint);
        }
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
                    url = `${API_BASE_URL}/login`;
                    method = 'POST';
                    body = document.querySelector('textarea[data-endpoint="auth-login"]').value;
                    break;
                  case 'books-getall':
                    url = `${API_BASE_URL}/books`;
                    method = 'GET';
                    console.log('Preparing to fetch all books...');
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
              // Show loading indicator for the endpoint
            const loadingIndicator = document.getElementById(`${endpoint}-loading`);
            if (loadingIndicator) {
                loadingIndicator.style.display = 'inline-block';
            }
            
            // Configure the request
            const requestOptions = { 
                method, 
                headers,
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin'  // Handle cookies properly
            };
            
            if (body && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
                requestOptions.body = body;
                console.log('Request with body:', method, url);
            }
            
            // Add custom timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            requestOptions.signal = controller.signal;
            
            console.log(`Sending ${method} request to: ${url}`);
            
            try {
                // Send the request
                console.log(`Attempting fetch to ${url} with method ${method}`);
                const response = await fetch(url, requestOptions);
                clearTimeout(timeoutId);
                console.log('Response received:', response.status);
                
                // Get the response
                let responseText;
                const contentType = response.headers.get("content-type");
                  try {
                    responseText = await response.text();
                    
                    // Special logging for books-getall to help troubleshoot
                    if (endpoint === 'books-getall') {
                        console.log("Books response received, length:", responseText.length);
                        console.log("First 100 characters:", responseText.substring(0, 100));
                    }
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
                  // Hide loading indicator
                const loadingIndicator = document.getElementById(`${endpoint}-loading`);
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }                // Special handling for books-getall to show in terminal
                if (endpoint === 'books-getall' && response.ok) {
                    try {                        console.log("======= ALL BOOKS IN DATABASE =======");
                        console.log("Raw response length:", responseText.length);
                        
                        // Show a small snippet of the raw XML in the terminal for debugging
                        console.log("\n--- RAW XML RESPONSE (first 200 chars) ---");
                        console.log(responseText.substring(0, 200) + "...");
                        console.log("--- END RAW XML SNIPPET ---\n");
                        
                        // Use our comprehensive XML parser utility to find books in any structure
                        const result = parseXMLResponse(responseText);
                        console.log("XML parsing result:", result.success ? "Success" : "Failed");
                        
                        // If books were found, use them
                        let bookElements = result.success ? result.books : [];
                        
                        // If the utility failed, parse manually as fallback
                        if (!result.success) {
                            console.log("Utility parsing failed, trying manual parsing as fallback...");
                            
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(responseText, "text/xml");
                            
                            // Check if there was an XML parsing error
                            const parseError = xmlDoc.getElementsByTagName("parsererror");
                            if (parseError.length > 0) {
                                console.error("XML parsing error:", parseError[0].textContent);
                                return;
                            }
                            
                            console.log("Manual XML parsing successful. Root element:", xmlDoc.documentElement.tagName);
                            
                            // Try various structures to find books
                            const responseElement = xmlDoc.getElementsByTagName('response')[0];
                            
                            if (responseElement) {
                                console.log("Found 'response' element");
                                const booksContainer = responseElement.getElementsByTagName('books')[0];
                                
                                if (booksContainer) {
                                    console.log("Found 'books' container");
                                    bookElements = booksContainer.getElementsByTagName('book');
                                }
                            }
                            
                            // If still no books, try direct search
                            if (bookElements.length === 0) {
                                bookElements = xmlDoc.getElementsByTagName('book');
                            }
                        }
                        
                        if (bookElements.length === 0) {
                            console.log("No books found in the database or XML structure is different than expected.");
                            console.log("Showing XML structure for debugging:");
                            logXmlStructure(xmlDoc.documentElement, 0);
                        } else {
                            console.log(`Found ${bookElements.length} books in database:`);
                            console.log("------------------------------------");
                            
                            // Loop through all books and print details
                            for (let i = 0; i < bookElements.length; i++) {
                                const book = bookElements[i];
                                console.log(`Book #${i+1}:`);
                                
                                // Get attributes and elements safely with fallbacks
                                const getBookValue = (tagName) => {
                                    const element = book.getElementsByTagName(tagName)[0];
                                    return element ? element.textContent : `Unknown ${tagName}`;
                                };
                                
                                const id = book.getAttribute('id') || (i+1).toString();
                                const title = getBookValue('title');
                                const author = getBookValue('author');
                                const year = getBookValue('year');
                                const isbn = getBookValue('isbn');
                                const publisher = getBookValue('publisher');
                                const category = getBookValue('category');
                                
                                // Display in terminal with clear formatting
                                console.log(`ID: ${id}`);
                                console.log(`Title: ${title}`);
                                console.log(`Author: ${author}`);
                                console.log(`Year: ${year}`);
                                console.log(`ISBN: ${isbn}`);
                                console.log(`Publisher: ${publisher}`);
                                console.log(`Category: ${category}`);
                                console.log("------------------------------------");
                            }
                        }
                        console.log("======= END OF BOOKS LIST =======");
                    } catch (error) {
                        console.error("Error processing books for terminal display:", error);
                        console.error("Error details:", error.stack);
                    }
                }
                
                // Display the response in the UI
                displayResponse(endpoint, response.ok, responseText, response.status);
                
            } catch (fetchError) {                // Reset button
                button.textContent = originalText;
                button.disabled = false;
                
                // Hide loading indicator
                const loadingIndicator = document.getElementById(`${endpoint}-loading`);
                if (loadingIndicator) {
                    loadingIndicator.style.display = 'none';
                }
                
                console.error('Fetch error:', fetchError);
                
                if (fetchError.name === 'AbortError') {
                    displayResponse(endpoint, false, 'Request timed out after 10 seconds. The server might be offline or responding slowly.');
                    return;
                }
                
                // Display error directly
                displayResponse(endpoint, false, `Error: ${fetchError.message}`);
            }
        } catch (error) {
            console.error('Error making API request:', error);
            
            // More detailed error information
            let errorDetails = `Error: ${error.message}\n\n`;
            if (typeof url !== 'undefined') {
                errorDetails += `URL: ${url}\n`;
                errorDetails += `Method: ${method}\n`;
            }
            
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
    
    // Update displayResponse to provide better error messages and XML formatting
    function displayResponse(endpoint, isSuccess, response, status = '') {
        console.log(`Displaying response for ${endpoint}. Success: ${isSuccess}, Status: ${status}`);
        
        const responseContainer = document.getElementById(`${endpoint}-response`);
        if (!responseContainer) {
            console.error(`No response container found for endpoint ${endpoint}`);
            return;
        }
        
        const responseStatus = responseContainer.querySelector('.response-status');
        const responseBody = responseContainer.querySelector('.response-body');
        
        // Set status text and styling
        if (isSuccess) {
            responseStatus.textContent = status || 'Success';
            responseStatus.className = 'response-status success';
        } else {
            if (status === 404) {
                responseStatus.textContent = '404 Not Found - Endpoint does not exist';
            } else if (status === 401) {
                responseStatus.textContent = '401 Unauthorized - Authentication required';
            } else if (status === 403) {
                responseStatus.textContent = '403 Forbidden - Insufficient permissions';
            } else if (status === 400) {
                responseStatus.textContent = '400 Bad Request - Check your XML format';
            } else if (status === 500) {
                responseStatus.textContent = '500 Server Error - See server logs for details';
            } else {
                responseStatus.textContent = status || 'Error';
            }
            responseStatus.className = 'response-status error';
        }
        
        // Format XML for better readability - enhanced for book listings
        if (typeof response === 'string' && (response.trim().startsWith('<?xml') || response.trim().startsWith('<'))) {
            try {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(response, "text/xml");
                
                // Check if there was an XML parsing error
                if (xmlDoc.getElementsByTagName("parsererror").length > 0) {
                    // XML contains errors, just show the raw text
                    responseBody.textContent = response;
                } else {                    // Special handling for book listings to ensure all elements are properly displayed
                    if (endpoint === 'books-getall') {
                        // Enhanced display for book listings
                        console.log("Processing book listing for UI display...");
                        const formattedBookXml = processBookListing(xmlDoc);
                        responseBody.textContent = formattedBookXml;
                        
                        // Additional debugging - show all tags in the XML
                        console.log("All XML tags in response:");
                        const allTags = Array.from(xmlDoc.getElementsByTagName('*')).map(el => el.tagName);
                        console.log([...new Set(allTags)]); // Show unique tag names
                    }
                    else if (endpoint === 'books-getbyid') {
                        // Create a pretty-printed version of the XML for single book
                        const serializer = new XMLSerializer();
                        const formattedXml = formatXml(serializer.serializeToString(xmlDoc));
                        responseBody.textContent = formattedXml;
                    } 
                    else {
                        // Standard XML formatting for other responses
                        const serializer = new XMLSerializer();
                        responseBody.textContent = formatXml(serializer.serializeToString(xmlDoc));
                    }
                }
            } catch (e) {
                console.error("Error formatting XML:", e);
                // If any error in XML processing, show raw response
                responseBody.textContent = response;
            }
        } else {
            // Not XML, show as is
            responseBody.textContent = response;
        }
        
        // Scroll to the response section
        responseContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Helper function to format XML with indentation - improved for book listings
    function formatXml(xml) {
        let formatted = '';
        let indent = '';
        
        // Fix XML declaration if present
        if (xml.startsWith('<?xml')) {
            const xmlDeclEnd = xml.indexOf('?>') + 2;
            formatted = xml.substring(0, xmlDeclEnd) + '\r\n';
            xml = xml.substring(xmlDeclEnd);
        }
        
        // Split by > and < but keep attributes together
        xml.split(/>\s*</).forEach(function(node) {
            if (node.match(/^\/\w/)) { // If this is a closing tag, decrease indent
                indent = indent.substring(2);
            }
            
            // Special handling for empty tags
            if (node.endsWith('/')) {
                formatted += indent + '<' + node + '>\r\n';
            } else {
                formatted += indent + '<' + node + '>\r\n';
            }
            
            if (node.match(/^<?\w[^>]*[^\/]$/) && !node.includes('/')) { // If this is an opening tag, increase indent
                indent += '  ';
            }
        });
        
        // Clean up the final string
        if (formatted.startsWith('\r\n')) {
            formatted = formatted.substring(2);
        }
        
        // Handle the first and last line properly
        if (formatted.endsWith('\r\n')) {
            return formatted.substring(0, formatted.length - 2);
        }
        
        return formatted;
    }    // Function to format book listings with improved structure detection
    function processBookListing(xmlDoc) {
        try {
            // First check the correct path for backend structure: response > books > book[]
            let books = [];
            const responseElement = xmlDoc.getElementsByTagName('response')[0];
            
            if (responseElement) {
                console.log("Found 'response' element - checking for books container");
                const booksContainer = responseElement.getElementsByTagName('books')[0];
                
                if (booksContainer) {
                    console.log("Found 'books' container element");
                    books = booksContainer.getElementsByTagName('book');
                    console.log("Books found in container:", books.length);
                }
            }
            
            // If books not found in expected structure, try direct search
            if (books.length === 0) {
                console.log("Books not found in expected structure, trying direct search...");
                books = xmlDoc.getElementsByTagName('book');
                console.log("Books found with direct search:", books.length);
            }
            
            // Create a summary text
            const count = books.length;
            const summary = `${count} ${count === 1 ? 'book' : 'books'} found in the database.\n\n`;
            
            // Create a more readable XML representation for the UI
            if (count > 0) {
                let formattedOutput = summary;
                formattedOutput += "Books in database:\n\n";
                
                for (let i = 0; i < books.length; i++) {
                    const book = books[i];
                    const getBookValue = (tagName) => {
                        const element = book.getElementsByTagName(tagName)[0];
                        return element ? element.textContent : null;
                    };
                    
                    formattedOutput += `Book #${i+1}:\n`;
                    formattedOutput += `ID: ${book.getAttribute('id') || 'Unknown'}\n`;
                    formattedOutput += `Title: ${getBookValue('title') || 'Unknown'}\n`;
                    formattedOutput += `Author: ${getBookValue('author') || 'Unknown'}\n`;
                    formattedOutput += `Year: ${getBookValue('year') || 'Unknown'}\n`;
                    formattedOutput += `ISBN: ${getBookValue('isbn') || 'Unknown'}\n`;
                    
                    const publisher = getBookValue('publisher');
                    if (publisher) formattedOutput += `Publisher: ${publisher}\n`;
                    
                    const category = getBookValue('category');
                    if (category) formattedOutput += `Category: ${category}\n`;
                    
                    formattedOutput += "\n";
                }
                
                // Add the raw XML at the end for reference
                formattedOutput += "\n--- Raw XML ---\n";
                formattedOutput += formatXml(new XMLSerializer().serializeToString(xmlDoc));
                return formattedOutput;
            } else {
                // Log XML structure for debugging
                console.log("XML document structure (no books found):");
                logXmlStructure(xmlDoc.documentElement, 0);
                
                // Return the formatted XML with summary for the UI
                return summary + "No books found.\n\n" + formatXml(new XMLSerializer().serializeToString(xmlDoc));
            }
        } catch (err) {
            console.error("Error processing book listing:", err);
            return "Error processing book listing: " + err.message;
        }
    }
      // Utility function to parse XML response in multiple ways to ensure we get the books
    function parseXMLResponse(xmlString) {
        console.log("Attempting to parse XML response with multiple methods");
        
        // Method 1: Using DOMParser
        try {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlString, "text/xml");
            
            // Check if there was an XML parsing error
            if (xmlDoc.getElementsByTagName("parsererror").length > 0) {
                console.error("XML parse error with DOMParser");
                console.error(xmlDoc.getElementsByTagName("parsererror")[0].textContent);
            } else {
                console.log("XML parsed successfully. Root element:", xmlDoc.documentElement.tagName);
                
                // Try the expected structure first (response > books > book[])
                let bookElements = [];
                const responseElement = xmlDoc.getElementsByTagName('response')[0];
                
                if (responseElement) {
                    console.log("Found 'response' element");
                    const booksContainer = responseElement.getElementsByTagName('books')[0];
                    
                    if (booksContainer) {
                        console.log("Found 'books' container element");
                        bookElements = booksContainer.getElementsByTagName('book');
                        console.log(`Found ${bookElements.length} books inside response > books container`);
                        
                        if (bookElements.length > 0) {
                            return {success: true, books: bookElements, structure: "response > books > book[]"};
                        }
                    }
                    
                    // Try looking in response > data > books > book[]
                    const dataElement = responseElement.getElementsByTagName('data')[0];
                    if (dataElement) {
                        const dataBooksContainer = dataElement.getElementsByTagName('books')[0];
                        if (dataBooksContainer) {
                            bookElements = dataBooksContainer.getElementsByTagName('book');
                            console.log(`Found ${bookElements.length} books inside response > data > books container`);
                            
                            if (bookElements.length > 0) {
                                return {success: true, books: bookElements, structure: "response > data > books > book[]"};
                            }
                        }
                    }
                }
                
                // Try looking for direct book elements
                bookElements = xmlDoc.getElementsByTagName('book');
                console.log(`Found ${bookElements.length} direct book elements`);
                
                if (bookElements.length > 0) {
                    console.log("Book elements found directly, displaying first book details:");
                    const book = bookElements[0];
                    console.log("Book attributes:", book.attributes.length ? "Yes" : "None");
                    console.log("Book child elements:", book.children.length);
                    Array.from(book.children).forEach(child => {
                        console.log(`- ${child.tagName}: ${child.textContent}`);
                    });
                    
                    return {success: true, books: bookElements, structure: "direct book[]"};
                }
                
                // If still not found, check for any book-like elements
                const allElements = xmlDoc.getElementsByTagName('*');
                const bookLikeElements = Array.from(allElements).filter(el => 
                    el.tagName.toLowerCase().includes('book') || 
                    el.tagName.toLowerCase() === 'item'
                );
                
                if (bookLikeElements.length > 0) {
                    console.log(`Found ${bookLikeElements.length} book-like elements`);
                    return {success: true, books: bookLikeElements, structure: "book-like elements"};
                }
                
                // If still not found, log the entire DOM structure for debugging
                console.log("No book elements found. Complete XML structure:");
                logXmlStructure(xmlDoc.documentElement, 0);
            }
        } catch (e) {
            console.error("Error in DOMParser method:", e);
            console.error(e.stack);
        }
        
        // Method 2: Simple text search as last resort
        try {
            if (xmlString.includes('<book')) {
                console.log("Found <book> tags in raw XML using text search");
                const bookCount = (xmlString.match(/<book/g) || []).length;
                console.log(`Raw text search found approximately ${bookCount} book elements`);
                return {success: false, books: [], textSearchFound: bookCount};
            } else {
                console.log("No <book> tags found in raw XML using text search");
                
                // Look for common XML patterns to help diagnose the issue
                const commonTags = ['response', 'data', 'books', 'items', 'records', 'results'];
                const foundTags = commonTags.filter(tag => xmlString.includes(`<${tag}`));
                console.log("Found these common XML tags:", foundTags.join(', ') || "none");
            }
        } catch (e) {
            console.error("Error in text search method:", e);
        }
        
        return {success: false, books: []};
    }
      // Helper function to print XML structure with more details
    function logXmlStructure(node, level) {
        if (!node) return;
        
        const indent = ' '.repeat(level * 2);
        if (node.nodeType === 1) { // Element node
            // Print element name with any ID attribute
            const id = node.getAttribute('id') ? ` id="${node.getAttribute('id')}"` : '';
            console.log(`${indent}<${node.tagName}${id}>`);
            
            // Print text content if it's a simple text node (no children but has text)
            if (node.children.length === 0 && node.textContent.trim()) {
                console.log(`${indent}  "${node.textContent.trim()}"`);
            }
            
            // Recursively process child elements
            for (let i = 0; i < node.children.length; i++) {
                logXmlStructure(node.children[i], level + 1);
            }
        }
    }
});
