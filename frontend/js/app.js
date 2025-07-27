// API Configuration
const API_V1_URL = 'http://localhost:5000/api/v1';
const API_V2_URL = 'http://localhost:5000/api/v2';
const CONTENT_TYPE_XML = 'application/xml';

// DOM Elements
const loginForm = document.getElementById('login-form');
const adminBooksContainer = document.getElementById('admin-books-container');
const studentBooksContainer = document.getElementById('student-books-container');
const adminPanel = document.getElementById('admin-panel');
const studentPanel = document.getElementById('student-panel');
const loginPanel = document.getElementById('login-panel');
const addBookForm = document.getElementById('add-book-form');
const logoutBtn = document.getElementById('logout-btn');
const alertBox = document.getElementById('alert-box');
const addBookBtn = document.getElementById('add-book-btn');
const addBookModal = document.getElementById('add-book-modal');
const closeModalBtn = document.getElementById('close-modal');
const welcomeMessage = document.getElementById('welcome-message');
const apiInfoContainer = document.getElementById('api-info-container');
const apiEndpointsContainer = document.getElementById('api-endpoints-container');
const viewApiEndpointsBtn = document.getElementById('view-api-endpoints-btn');
const endpointsList = document.getElementById('endpoints-list');

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  
  // Event listeners
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  if (addBookForm) {
    addBookForm.addEventListener('submit', handleAddBook);
  }
  
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
  
  if (addBookBtn) {
    addBookBtn.addEventListener('click', () => {
      addBookModal.style.display = 'block';
    });
  }
    if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      addBookModal.style.display = 'none';
    });
  }
  
  // Show API v1 endpoints when button is clicked
  if (viewApiEndpointsBtn) {
    viewApiEndpointsBtn.addEventListener('click', () => {
      if (endpointsList.classList.contains('hidden')) {
        fetchApiV1Endpoints();
        endpointsList.classList.remove('hidden');
        viewApiEndpointsBtn.textContent = 'Hide API v1 Endpoints';
      } else {
        endpointsList.classList.add('hidden');
        viewApiEndpointsBtn.textContent = 'View API v1 Endpoints';
      }
    });
  }
  
  // Always show API containers, regardless of login status
  if (apiEndpointsContainer) {
    apiEndpointsContainer.classList.remove('hidden');
  }
    // Close modal when clicking outside of it
  window.addEventListener('click', (event) => {
    if (event.target === addBookModal) {
      addBookModal.style.display = 'none';
    }
    if (event.target === document.getElementById('xml-modal')) {
      document.getElementById('xml-modal').style.display = 'none';
    }
  });
  
  // Close XML modal when clicking the X
  const closeXmlModal = document.querySelector('.close-xml-modal');
  if (closeXmlModal) {
    closeXmlModal.addEventListener('click', () => {
      document.getElementById('xml-modal').style.display = 'none';
    });
  }
});

// Check authentication status
function checkAuth() {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  const username = localStorage.getItem('username');
  
  if (token) {
    loginPanel.classList.add('hidden');
    
    // Show logout button
    if (logoutBtn) {
      logoutBtn.classList.remove('hidden');
    }
    
    if (userRole === 'admin') {
      adminPanel.classList.remove('hidden');
      studentPanel.classList.add('hidden');
    } else {
      adminPanel.classList.add('hidden');
      studentPanel.classList.remove('hidden');
    }
    
    if (welcomeMessage) {
      welcomeMessage.textContent = `Welcome, ${username}!`;
    }
    
    // Display JWT token in the header
    const tokenDisplay = document.getElementById('token-display');
    const tokenValue = document.getElementById('token-value');
    if (tokenDisplay && tokenValue) {
      tokenDisplay.classList.remove('hidden');
      tokenValue.textContent = token;
      tokenValue.title = token; // Show full token on hover
      
      // Set up copy button
      const copyTokenBtn = document.getElementById('copy-token-btn');
      if (copyTokenBtn) {
        copyTokenBtn.addEventListener('click', () => {
          navigator.clipboard.writeText(token)
            .then(() => {
              showAlert('Token copied to clipboard!', 'success', 2000);
              copyTokenBtn.textContent = 'Copied!';
              setTimeout(() => {
                copyTokenBtn.textContent = 'Copy';
              }, 2000);
            })
            .catch(err => {
              console.error('Failed to copy: ', err);
              showAlert('Failed to copy token', 'error');
            });
        });
      }
    }    
    fetchBooks();
    
    // Always fetch API info regardless of auth status
    fetchApiInfo();
  } else {
    loginPanel.classList.remove('hidden');
    adminPanel.classList.add('hidden');
    studentPanel.classList.add('hidden');
    
    // Hide logout button
    if (logoutBtn) {
      logoutBtn.classList.add('hidden');
    }
    
    // Clear welcome message
    if (welcomeMessage) {
      welcomeMessage.textContent = '';
    }
    
    // Still fetch API info even when not logged in
    fetchApiInfo();
  }
}

// Handle login form submission
async function handleLogin(event) {
  event.preventDefault();
  
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  
  // Create XML payload
  const loginXml = `<?xml version="1.0" encoding="UTF-8"?><login><username>${username}</username><password>${password}</password></login>`;
  
  try {
    const response = await fetch(`${API_V1_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': CONTENT_TYPE_XML,
      },
      body: loginXml,
    });
    
    const xmlText = await response.text();
    console.log('Login response XML:', xmlText);
    
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
    
    if (response.ok) {
      const statusElement = xmlDoc.querySelector('status');
      const tokenElement = xmlDoc.querySelector('token');
      const usernameElement = xmlDoc.querySelector('user username');
      const roleElement = xmlDoc.querySelector('user role');
        if (statusElement && statusElement.textContent === 'success' && tokenElement) {
        console.log('Token found:', tokenElement.textContent);
        console.log('Username:', usernameElement ? usernameElement.textContent : 'Not found');
        console.log('Role:', roleElement ? roleElement.textContent : 'Not found');
        
        // Store token exactly as received from backend - don't add Bearer prefix
        localStorage.setItem('token', tokenElement.textContent);
        localStorage.setItem('username', usernameElement ? usernameElement.textContent : 'User');
        localStorage.setItem('userRole', roleElement ? roleElement.textContent : 'student');
        
        // Debug token by splitting it to see components
        try {
          const tokenParts = tokenElement.textContent.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            console.log('Token payload:', payload);
          }
        } catch (e) {
          console.error('Error parsing token:', e);
        }
        
        showAlert('Login successful! Redirecting...', 'success');
        setTimeout(() => {
          checkAuth();
        }, 1000);
      }else {
        console.error('Invalid login response structure');
        showAlert('Invalid login response', 'error');
      }
    } else {
      const messageElement = xmlDoc.querySelector('message');
      const errorMessage = messageElement ? messageElement.textContent : 'Login failed';
      showAlert(errorMessage, 'error');
    }
  } catch (error) {
    showAlert(`Error: ${error.message}`, 'error');
  }
}

// Handle fetching books
async function fetchBooks() {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('userRole');
  
  if (!token) {
    return;
  }
  
  // Determine which container to use based on user role
  const booksContainer = userRole === 'admin' ? adminBooksContainer : studentBooksContainer;
  
  // Show loading spinner
  if (booksContainer) {
    booksContainer.innerHTML = '<div class="spinner"></div>';
  }
    try {
    console.log('Fetching books with token:', token);
    
    // Bearer token should be added in the request, not stored in localStorage
    const response = await fetch(`${API_V1_URL}/books`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': CONTENT_TYPE_XML,
      },
    });
    
    const xmlText = await response.text();
    console.log('Fetch books response:', xmlText);
    
    if (response.ok) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
      
      const bookElements = xmlDoc.querySelectorAll('book');
      
      if (booksContainer) {
        booksContainer.innerHTML = '';
        
        if (bookElements.length === 0) {
          booksContainer.innerHTML = '<p>No books found in library.</p>';
          return;
        }
        
        bookElements.forEach((book) => {
          const bookId = book.getAttribute('id');
          const title = book.querySelector('title').textContent;
          const author = book.querySelector('author').textContent;
          const year = book.querySelector('year').textContent;
          const isbn = book.querySelector('isbn').textContent;
          const publisher = book.querySelector('publisher') ? book.querySelector('publisher').textContent : '';
          const category = book.querySelector('category') ? book.querySelector('category').textContent : '';
          const description = book.querySelector('description') ? book.querySelector('description').textContent : '';
          
          const bookCard = createBookCard(bookId, title, author, year, isbn, publisher, category, description);
          booksContainer.appendChild(bookCard);
        });
      }
    } else {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
      const messageElement = xmlDoc.querySelector('message');
      const errorMessage = messageElement ? messageElement.textContent : `Failed to fetch books (${response.status})`;
      
      console.error('Error fetching books:', errorMessage);
      showAlert(errorMessage, 'error');
      
      if (booksContainer) {
        booksContainer.innerHTML = `<p class="error">Error: ${errorMessage}</p>`;
      }
      
      // If we got a 401/403, it might be an auth issue - try to log out
      if (response.status === 401 || response.status === 403) {
        console.log("Authentication issue detected. Logging out in 3 seconds...");
        setTimeout(handleLogout, 3000);
      }
    }
  } catch (error) {
    console.error('Fetch error:', error);
    showAlert(`Error: ${error.message}`, 'error');
    
    const booksContainer = userRole === 'admin' ? adminBooksContainer : studentBooksContainer;
    if (booksContainer) {
      booksContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
  }
}

// Create a book card HTML element
function createBookCard(id, title, author, year, isbn, publisher, category, description) {
  const bookCard = document.createElement('div');
  bookCard.className = 'book-card';
  bookCard.dataset.id = id;
  
  bookCard.innerHTML = `
    <div class="book-header">
      <h3 class="book-title">${title}</h3>
      <p class="book-author">by ${author}</p>
    </div>
    <div class="book-body">
      <div class="book-meta">
        <p><strong>Year:</strong> ${year}</p>
        <p><strong>ISBN:</strong> ${isbn}</p>
        <p><strong>Publisher:</strong> ${publisher}</p>
        <p><strong>Category:</strong> ${category}</p>
      </div>
      <div class="book-description">
        <p>${description}</p>
      </div>
      <div class="book-actions">
        <button class="btn btn-info view-xml" data-id="${id}">View XML</button>
        ${localStorage.getItem('userRole') === 'admin' ? 
          `<button class="btn btn-danger delete-book" data-id="${id}">Delete</button>` : 
          ''}
      </div>
    </div>
  `;
  
  // Add view XML event listener
  const viewXmlBtn = bookCard.querySelector('.view-xml');
  viewXmlBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent card click event
    showBookXML(id);
  });
  
  // Make entire card clickable to show XML
  bookCard.addEventListener('click', () => {
    showBookXML(id);
  });
  
  // Add delete event listener if admin
  if (localStorage.getItem('userRole') === 'admin') {
    const deleteBtn = bookCard.querySelector('.delete-book');
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation(); // Prevent card click event
      if (confirm('Are you sure you want to delete this book?')) {
        deleteBook(id);
      }
    });
  }
  
  return bookCard;
}

// Function to fetch and show book XML in a modal
async function showBookXML(bookId) {
  const token = localStorage.getItem('token');
  const xmlModal = document.getElementById('xml-modal');
  const xmlDisplay = document.getElementById('xml-display');
  
  // Show loading in the modal
  xmlDisplay.innerHTML = '<div class="spinner"></div>';
  xmlModal.style.display = 'block';
  
  try {
    const response = await fetch(`${API_V1_URL}/books/${bookId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': CONTENT_TYPE_XML,
      },
    });
    
    const xmlText = await response.text();
    
    if (response.ok) {
      // Format and highlight the XML
      const formattedXML = formatXMLWithHighlighting(xmlText);
      xmlDisplay.innerHTML = formattedXML;
    } else {
      xmlDisplay.innerHTML = `<p class="error">Error fetching book XML: ${response.status}</p>`;
    }
  } catch (error) {
    xmlDisplay.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    console.error('Error fetching book XML:', error);
  }
}

// Function to format and highlight XML
function formatXMLWithHighlighting(xmlString) {
  // Replace special characters to prevent HTML injection
  let escaped = xmlString
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
    
  // Add indentation
  let formatted = '';
  let indent = 0;
  const lines = escaped.split('\n');
  
  lines.forEach(line => {
    line = line.trim();
    if (!line) return;
    
    // Check if this line is a closing tag
    if (line.startsWith('&lt;/')) {
      indent -= 2;
    }
    
    // Add proper indentation
    formatted += ' '.repeat(indent) + line + '\n';
    
    // Check if this line is an opening tag (and not self-closing)
    if (line.startsWith('&lt;') && 
        !line.startsWith('&lt;/') && 
        !line.startsWith('&lt;?') && 
        !line.endsWith('/&gt;')) {
      indent += 2;
    }
  });
  
  // Add syntax highlighting
  formatted = formatted
    // Tag highlighting
    .replace(/&lt;(\/?[^\s&]+)([^&]*)&gt;/g, '<span class="xml-tag">&lt;$1</span>$2<span class="xml-tag">&gt;</span>')
    // Attribute highlighting
    .replace(/([^\s]+)=(&quot;[^&]*&quot;)/g, '<span class="xml-attr">$1</span>=$2');
    
  return formatted;
}

// Handle book deletion
async function deleteBook(bookId) {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`${API_V1_URL}/books/${bookId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': CONTENT_TYPE_XML,
      },
    });
    
    const xmlText = await response.text();
    console.log('Delete response:', xmlText);
    
    if (response.ok) {
      showAlert('Book deleted successfully', 'success');
      fetchBooks(); // Refresh the book list
    } else {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
      const messageElement = xmlDoc.querySelector('message');
      const errorMessage = messageElement ? messageElement.textContent : 'Failed to delete book';
      showAlert(errorMessage, 'error');
    }
  } catch (error) {
    showAlert(`Error: ${error.message}`, 'error');
  }
}

// Handle adding a new book
async function handleAddBook(event) {
  event.preventDefault();
  
  const title = document.getElementById('book-title').value;
  const author = document.getElementById('book-author').value;
  const year = document.getElementById('book-year').value;
  const isbn = document.getElementById('book-isbn').value;
  const publisher = document.getElementById('book-publisher').value;
  const category = document.getElementById('book-category').value;
  const description = document.getElementById('book-description').value;
  
  // Basic validation
  if (!title || !author || !year || !isbn) {
    showAlert('Please fill in all required fields', 'error');
    return;
  }
  
  if (isNaN(year) || parseInt(year) <= 0) {
    showAlert('Please enter a valid year', 'error');
    return;
  }
  
  // Create XML payload
  const bookXml = `<?xml version="1.0" encoding="UTF-8"?><book_submission><title>${title}</title><author>${author}</author><year>${year}</year><isbn>${isbn}</isbn><publisher>${publisher}</publisher><category>${category}</category><description>${description}</description></book_submission>`;
  
  const token = localStorage.getItem('token');
  try {
    console.log('Sending book data:', bookXml);
    console.log('Using token:', token);
      const response = await fetch(`${API_V1_URL}/books`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': CONTENT_TYPE_XML,
        'Accept': CONTENT_TYPE_XML
      },
      body: bookXml,
    });
    
    console.log('Response status:', response.status);
    const xmlText = await response.text();
    console.log('Response text:', xmlText);
    
    if (response.ok) {
      showAlert('Book added successfully', 'success');
      addBookForm.reset();
      addBookModal.style.display = 'none';
      fetchBooks(); // Refresh the book list
    } else {
      let errorMessage = 'Failed to add book';
      
      try {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
        const messageElement = xmlDoc.querySelector('message');
        if (messageElement) {
          errorMessage = messageElement.textContent;
        }
      } catch (parseError) {
        console.error('Error parsing response XML:', parseError);
      }
      
      showAlert(`Error (${response.status}): ${errorMessage}`, 'error');
    }
  } catch (error) {
    console.error('Add book error:', error);
    showAlert(`Network Error: ${error.message}`, 'error');
  }
}

// Handle logout
async function handleLogout() {
  const username = localStorage.getItem('username');
  const token = localStorage.getItem('token');
  
  try {
    // Call the backend logout endpoint if we have a token
    if (token) {
      await fetch(`${API_V1_URL}/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': CONTENT_TYPE_XML,
        }
      });
    }
  } catch (error) {
    console.error('Logout API error:', error);
    // Continue with logout even if API call fails
  } finally {
    // Clear all auth-related items from local storage
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    localStorage.removeItem('username');
      // Hide token display
    const tokenDisplay = document.getElementById('token-display');
    if (tokenDisplay) {
      tokenDisplay.classList.add('hidden');
    }
    
    // Update the UI
    checkAuth();
    
    // Show feedback to the user
    showAlert(`Goodbye, ${username || 'User'}! You have been logged out successfully.`, 'success');
    
    // Scroll to top for better user experience
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Show alert message
function showAlert(message, type) {
  if (!alertBox) return;
  
  alertBox.textContent = message;
  alertBox.className = `alert alert-${type}`;
  alertBox.classList.remove('hidden');
  
  // Hide after 5 seconds
  setTimeout(() => {
    alertBox.classList.add('hidden');
  }, 5000);
}

// Fetch weather data from external service
// Handle fetching API information (v2 API)
async function fetchApiInfo() {
  try {
    const response = await fetch(`${API_V2_URL}/info`, {
      method: 'GET',
      headers: {
        'Accept': CONTENT_TYPE_XML,
      },
    });
    
    if (response.ok) {
      const xmlText = await response.text();
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
      
      const apiInfoElement = xmlDoc.querySelector('api_info');
      
      if (apiInfoElement && apiInfoContainer) {
        const version = apiInfoElement.querySelector('version').textContent;
        const name = apiInfoElement.querySelector('name').textContent;
        const currentTime = apiInfoElement.querySelector('current_time').textContent;
        const status = apiInfoElement.querySelector('status').textContent;
        
        apiInfoContainer.innerHTML = `
          <div class="api-info-card">
            <h3>API Information</h3>
            <div class="api-info-details">
              <p><strong>Name:</strong> ${name}</p>
              <p><strong>Version:</strong> ${version}</p>
              <p><strong>Status:</strong> ${status}</p>
              <p><strong>Server Time:</strong> ${currentTime}</p>
            </div>
          </div>
        `;
        
        apiInfoContainer.classList.remove('hidden');
      }
    } else {
      console.error('Error fetching API info:', response.status);
      if (apiInfoContainer) {
        apiInfoContainer.innerHTML = '<p>API information unavailable</p>';
      }
    }
  } catch (error) {
    console.error('API info fetch error:', error);
    if (apiInfoContainer) {
      apiInfoContainer.innerHTML = `<p>Error loading API information: ${error.message}</p>`;
    }
  }
}

// Handle fetching API v1 endpoints
async function fetchApiV1Endpoints() {
  try {
    endpointsList.innerHTML = '<div class="spinner"></div>';
    
    const response = await fetch(`${API_V1_URL}/endpoints`, {
      method: 'GET',
      headers: {
        'Accept': CONTENT_TYPE_XML,
      },
    });
    
    if (response.ok) {
      const xmlText = await response.text();
      console.log('API Endpoints XML:', xmlText);
      
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlText, 'application/xml');
      
      // Try to get endpoints from data/endpoints/endpoint path (based on our revised backend XML)
      const endpointElements = xmlDoc.querySelectorAll('data endpoints endpoint');
      console.log('Found endpoints:', endpointElements.length);
      
      if (endpointElements.length > 0) {
        // Group endpoints by their group
        const groupedEndpoints = {};
        
        endpointElements.forEach(endpoint => {
          const path = endpoint.querySelector('path').textContent;
          const description = endpoint.querySelector('description').textContent;
          const group = endpoint.querySelector('group').textContent;
          
          // Get methods - they may be in different formats
          let methods = 'GET'; // Default
          const methodsEl = endpoint.querySelector('methods');
          
          if (methodsEl) {
            const methodNodes = methodsEl.querySelectorAll('method');
            if (methodNodes.length > 0) {
              methods = Array.from(methodNodes)
                .map(m => m.textContent)
                .join(', ');
            } else {
              methods = methodsEl.textContent || 'GET';
            }
          }
          
          if (!groupedEndpoints[group]) {
            groupedEndpoints[group] = [];
          }
          
          groupedEndpoints[group].push({
            path,
            methods,
            description
          });
        });
          // Create HTML for endpoints
        let endpointsHtml = '';
        
        Object.keys(groupedEndpoints).forEach(group => {
          endpointsHtml += `
            <div class="endpoint-group">
              <h4>${group.charAt(0).toUpperCase() + group.slice(1)}</h4>
              <table class="endpoints-table">
                <thead>
                  <tr>
                    <th>Path</th>
                    <th>Methods</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
          `;
          
          groupedEndpoints[group].forEach(endpoint => {
            endpointsHtml += `
              <tr>
                <td><code>${endpoint.path}</code></td>
                <td><code>${endpoint.methods}</code></td>
                <td>${endpoint.description}</td>
              </tr>
            `;
          });
          
          endpointsHtml += `
                </tbody>
              </table>
            </div>
          `;
        });
        
        endpointsList.innerHTML = endpointsHtml;      } else {
        // If direct approach fails, try an alternative parsing method
        console.log('Direct endpoint query failed, trying alternative method');
        
        // Try to get all path elements and work with their parents
        const pathElements = xmlDoc.querySelectorAll('path');
        console.log('Found path elements:', pathElements.length);
        
        if (pathElements.length > 0) {
          // Group endpoints by their group
          const groupedEndpoints = {};
          
          Array.from(pathElements).forEach(pathEl => {
            // Check if this is part of an endpoint structure
            const endpoint = pathEl.parentNode;
            if (endpoint && endpoint.querySelector('description') && endpoint.querySelector('group')) {
              const path = pathEl.textContent;
              const description = endpoint.querySelector('description').textContent;
              const group = endpoint.querySelector('group').textContent;
              
              // Get methods element or default to GET
              let methods = 'GET';
              const methodsEl = endpoint.querySelector('methods');
              if (methodsEl) {
                const methodNodes = methodsEl.querySelectorAll('method');
                if (methodNodes.length > 0) {
                  methods = Array.from(methodNodes).map(m => m.textContent).join(', ');
                } else {
                  methods = methodsEl.textContent || 'GET';
                }
              }
              
              if (!groupedEndpoints[group]) {
                groupedEndpoints[group] = [];
              }
              
              groupedEndpoints[group].push({
                path, 
                methods,
                description
              });
            }
          });
          
          if (Object.keys(groupedEndpoints).length > 0) {
            // Create HTML for endpoints using same code as above
            let endpointsHtml = '';
            
            Object.keys(groupedEndpoints).forEach(group => {
              endpointsHtml += `
                <div class="endpoint-group">
                  <h4>${group.charAt(0).toUpperCase() + group.slice(1)}</h4>
                  <table class="endpoints-table">
                    <thead>
                      <tr>
                        <th>Path</th>
                        <th>Methods</th>
                        <th>Description</th>
                      </tr>
                    </thead>
                    <tbody>
              `;
              
              groupedEndpoints[group].forEach(endpoint => {
                endpointsHtml += `
                  <tr>
                    <td><code>${endpoint.path}</code></td>
                    <td><code>${endpoint.methods}</code></td>
                    <td>${endpoint.description}</td>
                  </tr>
                `;
              });
              
              endpointsHtml += `
                    </tbody>
                  </table>
                </div>
              `;
            });
            
            endpointsList.innerHTML = endpointsHtml;
          } else {
            endpointsList.innerHTML = '<p>No API endpoints found. Could not parse endpoint structure.</p>';
          }
        } else {
          endpointsList.innerHTML = '<p>No API endpoints found. XML structure does not contain path elements.</p>';
          console.error('XML structure does not contain expected path elements.');
        }
      }
    } else {
      console.error('Error fetching API endpoints:', response.status);
      endpointsList.innerHTML = '<p class="error">Failed to load API endpoints.</p>';
    }
  } catch (error) {
    console.error('API endpoints fetch error:', error);
    endpointsList.innerHTML = `<p class="error">Error loading API endpoints: ${error.message}</p>`;
  }
}
