"""
HTML Templates for Banking RAG System

Web interface templates for the Banking RAG system.
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banking RAG System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background-color: #f0f2f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 0.5rem;
        }
        .message {
            max-width: 80%;
            padding: 1rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
        }
        .message.user {
            align-self: flex-end;
            background: #0d6efd;
            color: white;
            border-bottom-right-radius: 0.2rem;
        }
        .message.ai {
            align-self: flex-start;
            background: white;
            border: 1px solid #dee2e6;
            border-bottom-left-radius: 0.2rem;
        }
        .message.system {
            align-self: center;
            background: #e9ecef;
            border: 1px solid #dee2e6;
            text-align: center;
            max-width: 90%;
        }
        .message-content {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .chat-input-container {
            position: relative;
            background: white;
            border-top: 1px solid #dee2e6;
            padding: 1rem;
        }
        .sources {
            margin-top: 1rem;
            padding: 1rem;
            background: #e8f4fd;
            border-left: 4px solid #0d6efd;
            border-radius: 0.5rem;
            font-size: 0.9rem;
        }
        .typing-indicator {
            max-width: 320px !important;
        }
        .typing-dots {
            display: inline-flex;
            gap: 4px;
            padding: 4px 8px;
            background: #e9ecef;
            border-radius: 12px;
        }
        .typing-dots span {
            width: 8px;
            height: 8px;
            background: #6c757d;
            border-radius: 50%;
            animation: typingAnimation 1.4s infinite;
            display: inline-block;
        }
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typingAnimation {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.4;
            }
            30% {
                transform: translateY(-4px);
                opacity: 1;
            }
        }
        .session-controls {
            border-top: 1px solid #dee2e6;
            padding-top: 0.5rem;
        }
        .message-meta {
            margin-top: 0.5rem;
            padding-top: 0.5rem;
            border-top: 1px solid #f8f9fa;
            font-size: 0.85em;
        }
        .message-meta small {
            display: inline-block;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container py-4">
        <div class="header">
            <h1>🏦 Banking RAG System</h1>
            <p class="lead">AI-Powered Banking & Financial Services Q&A</p>
            <p><em>Enhanced with comprehensive knowledge base and advanced retrieval</em></p>
            <a href="/api/v1/add-qsa" class="btn btn-success btn-lg mt-3">Add New Q&A</a>
        </div>

        <div class="row text-center bg-white rounded-3 shadow-sm p-4 mb-4">
            <div class="col-md-4">
                <div class="stat-number" id="docCount">15+</div>
                <div class="stat-label">Knowledge Documents</div>
            </div>
            <div class="col-md-4">
                <div class="stat-number">10+</div>
                <div class="stat-label">Service Categories</div>
            </div>
            <div class="col-md-4">
                <div class="stat-number">24/7</div>
                <div class="stat-label">AI Availability</div>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-8">
                <!-- Main Chat Area -->
                <div class="card h-100">
                    <div class="card-body p-0">
                        <div id="chatbox" class="chat-container" style="height: 500px; overflow-y: auto;">
                            <div class="message system">
                                <div class="message-content">
                                    👋 Welcome to the Banking RAG System! Ask any banking or financial services question and get instant, accurate answers based on our comprehensive knowledge base.

Our system covers:
• Personal and business loans
• Savings and investment accounts  
• Credit cards and mortgages
• Digital banking services
• Regulatory compliance
• Customer support information
                                </div>
                            </div>
                        </div>
                        
                        <div id="sourcesArea" class="sources mx-3 mb-3" style="display: none;">
                            <strong><i class="bi bi-info-circle"></i> Sources:</strong>
                            <div id="sourcesList"></div>
                        </div>

                        <!-- Session Management Controls -->
                        <div class="session-controls mx-3 mb-2">
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    <i class="bi bi-chat-dots"></i> 
                                    <span id="sessionStatus">Ready to chat</span>
                                </small>
                                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="startNewSession()" title="Start New Session">
                                    <i class="bi bi-plus-circle"></i> New Session
                                </button>
                            </div>
                        </div>

                        <div class="chat-input-container">
                            <form onsubmit="event.preventDefault(); submitQuery();">
                                <div class="input-group">
                                    <textarea id="queryInput" class="form-control" 
                                            placeholder="Type your banking question here..." 
                                            rows="2"
                                            style="resize: none;"></textarea>
                                    <button id="submitBtn" type="submit" class="btn btn-primary px-4">
                                        <i class="bi bi-send"></i>
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-4">
                <!-- Sample Questions Sidebar -->
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title mb-3">
                            <i class="bi bi-lightbulb"></i> Sample Questions
                        </h5>
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What are the requirements for getting a personal loan?')">
                                <i class="bi bi-arrow-right-circle"></i> Personal Loan Requirements
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('How do I open a savings account and what are the benefits?')">
                                <i class="bi bi-arrow-right-circle"></i> Savings Account Information
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What is the process for applying for a credit card?')">
                                <i class="bi bi-arrow-right-circle"></i> Credit Card Application
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What investment options do you offer?')">
                                <i class="bi bi-arrow-right-circle"></i> Investment Options
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('How secure is mobile banking?')">
                                <i class="bi bi-arrow-right-circle"></i> Mobile Banking Security
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What do I need to qualify for a mortgage?')">
                                <i class="bi bi-arrow-right-circle"></i> Mortgage Requirements
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What business banking services are available?')">
                                <i class="bi bi-arrow-right-circle"></i> Business Banking
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What are the current interest rates?')">
                                <i class="bi bi-arrow-right-circle"></i> Interest Rates
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('Do you offer cryptocurrency services?')">
                                <i class="bi bi-arrow-right-circle"></i> Crypto Services
                            </button>
                            <button class="btn btn-outline-primary text-start" onclick="setQuery('What wealth management services are available?')">
                                <i class="bi bi-arrow-right-circle"></i> Wealth Management
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Global session management
        let currentSessionId = localStorage.getItem('banking_rag_session_id');
        let sessionStartTime = new Date();

        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }

        function generateUserId() {
            // Generate a simple user ID for session tracking
            let userId = localStorage.getItem('banking_rag_user_id');
            if (!userId) {
                userId = 'user_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('banking_rag_user_id', userId);
            }
            return userId;
        }

        function startNewSession() {
            // Clear current session
            currentSessionId = null;
            localStorage.removeItem('banking_rag_session_id');
            
            // Clear chat history
            const chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = '';
            
            // Show welcome message
            const welcomeMessage = document.createElement('div');
            welcomeMessage.className = 'message ai';
            welcomeMessage.innerHTML = `
                <div class="message-content">
                    <strong>Welcome to Banking RAG Assistant!</strong><br>
                    I'm here to help you with banking questions. Ask me about loans, accounts, credit cards, and more.
                    <br><br>
                    <small class="text-muted">New session started at ${new Date().toLocaleTimeString()}</small>
                </div>
            `;
            chatbox.appendChild(welcomeMessage);
            sessionStartTime = new Date();
        }

        async function submitQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const chatbox = document.getElementById('chatbox');
            const sourcesArea = document.getElementById('sourcesArea');
            const sourcesList = document.getElementById('sourcesList');

            if (!query) {
                const toastEl = document.createElement('div');
                toastEl.innerHTML = `
                    <div class="toast-container position-fixed bottom-0 end-0 p-3">
                        <div class="toast" role="alert">
                            <div class="toast-header bg-warning text-dark">
                                <strong class="me-auto">Warning</strong>
                                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                            </div>
                            <div class="toast-body">
                                Please enter a question
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(toastEl);
                const toast = new bootstrap.Toast(toastEl.querySelector('.toast'));
                toast.show();
                setTimeout(() => toastEl.remove(), 5000);
                return;
            }

            // Add user message to chat
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.innerHTML = `<div class="message-content">${query}</div>`;
            chatbox.appendChild(userMessage);

            // Add AI typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message ai typing-indicator';
            typingIndicator.innerHTML = `
                <div class="message-content d-flex align-items-center gap-2">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <small class="text-muted">AI is typing...</small>
                </div>
            `;
            chatbox.appendChild(typingIndicator);

            // Scroll to bottom
            chatbox.scrollTop = chatbox.scrollHeight;

            // Clear input
            document.getElementById('queryInput').value = '';

            // Disable button
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            sourcesArea.style.display = 'none';

            try {
                // Prepare request payload with session management
                const requestPayload = { 
                    query: query,
                    user_id: generateUserId()
                };
                
                // Include session_id if we have one
                if (currentSessionId) {
                    requestPayload.session_id = currentSessionId;
                }

                const response = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestPayload)
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Store session ID if returned and not already stored
                    if (data.session_id && !currentSessionId) {
                        currentSessionId = data.session_id;
                        localStorage.setItem('banking_rag_session_id', currentSessionId);
                        console.log('New session created:', currentSessionId);
                    }

                    // Remove typing indicator
                    chatbox.removeChild(typingIndicator);

                    // Add AI response to chat with enhanced information
                    const aiMessage = document.createElement('div');
                    aiMessage.className = 'message ai';
                    
                    let messageContent = `<div class="message-content">${data.answer}</div>`;
                    
                    // Add response time and session info if available
                    if (data.response_time_ms || data.session_id) {
                        messageContent += `<div class="message-meta">`;
                        if (data.response_time_ms) {
                            messageContent += `<small class="text-muted">⏱️ ${data.response_time_ms}ms</small>`;
                        }
                        if (data.session_id && data.chat_enabled) {
                            messageContent += `<small class="text-muted ms-2">💬 Chat history enabled</small>`;
                        }
                        messageContent += `</div>`;
                    }
                    
                    aiMessage.innerHTML = messageContent;
                    chatbox.appendChild(aiMessage);

                    // Show sources
                    if (data.sources && data.sources.length > 0) {
                        sourcesList.innerHTML = '';
                        data.sources.forEach(source => {
                            const sourceItem = document.createElement('div');
                            sourceItem.className = 'source-item mb-2';
                            const confidenceClass = source.relevance_score > 0.8 ? 'high' : source.relevance_score > 0.6 ? 'medium' : 'low';
                            sourceItem.innerHTML = `
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <strong>${source.title}</strong>
                                        <span class="text-muted">(${source.category})</span>
                                    </div>
                                    <span class="badge ${
                                        confidenceClass === 'high' ? 'bg-success' : 
                                        confidenceClass === 'medium' ? 'bg-warning text-dark' : 
                                        'bg-danger'
                                    }">${(source.relevance_score * 100).toFixed(0)}%</span>
                                </div>
                            `;
                            sourcesList.appendChild(sourceItem);
                        });
                        sourcesArea.style.display = 'block';
                    }
                } else {
                    // Remove typing indicator
                    chatbox.removeChild(typingIndicator);

                    // Add error message to chat
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'message system';
                    errorMessage.innerHTML = `<div class="message-content text-danger">
                        <i class="bi bi-exclamation-triangle"></i> Error: ${data.message || 'Unknown error occurred'}
                    </div>`;
                    chatbox.appendChild(errorMessage);
                }
            } catch (error) {
                // Remove typing indicator
                chatbox.removeChild(typingIndicator);

                // Add error message to chat
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message system';
                errorMessage.innerHTML = `<div class="message-content text-danger">
                    <i class="bi bi-exclamation-triangle"></i> Error: Unable to process request. Please try again.
                </div>`;
                chatbox.appendChild(errorMessage);
                console.error('Error:', error);
            } finally {
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-send"></i>';
                
                // Scroll to bottom
                chatbox.scrollTop = chatbox.scrollHeight;
            }
        }

        // Allow Enter key to submit (with Shift+Enter for new line)
        document.getElementById('queryInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submitQuery();
            }
        });

        function updateSessionStatus() {
            const statusElement = document.getElementById('sessionStatus');
            if (currentSessionId) {
                const duration = Math.floor((new Date() - sessionStartTime) / 60000);
                statusElement.innerHTML = `Session active (${duration}m) • ID: ${currentSessionId.substr(0, 8)}...`;
            } else {
                statusElement.innerHTML = 'Ready to chat';
            }
        }

        // Update session status every 30 seconds
        setInterval(updateSessionStatus, 30000);

        // Load document count on page load
        async function loadStats() {
            try {
                const response = await fetch('/api/v1/categories');
                const data = await response.json();
                if (data.status === 'success') {
                    document.getElementById('docCount').textContent = data.total_documents;
                }
            } catch (error) {
                console.log('Could not load stats:', error);
            }
        }

        // Initialize page
        function initializePage() {
            loadStats();
            updateSessionStatus();
            // Show existing session info if available
            if (currentSessionId) {
                console.log('Resuming session:', currentSessionId);
                updateSessionStatus();
                loadSessionMessages(currentSessionId);
            }
        }

        // Load and render messages for a session
        async function loadSessionMessages(sessionId) {
            const chatbox = document.getElementById('chatbox');
            chatbox.innerHTML = '';
            try {
                const response = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: '', session_id: sessionId, user_id: generateUserId() })
                });
                const data = await response.json();
                if (data.messages && Array.isArray(data.messages)) {
                    data.messages.forEach(msg => {
                        const msgDiv = document.createElement('div');
                        msgDiv.className = 'message ' + (msg.message_type === 'user' ? 'user' : 'ai');
                        let content = `<div class="message-content">${msg.content}</div>`;
                        if (msg.timestamp) {
                            content += `<div class="message-meta"><small class="text-muted">${msg.timestamp}</small></div>`;
                        }
                        msgDiv.innerHTML = content;
                        chatbox.appendChild(msgDiv);
                    });
                }
            } catch (error) {
                console.error('Failed to load session messages:', error);
            }
        }

        // Load stats when page loads
        window.addEventListener('load', initializePage);
    </script>
</body>
</html>'''
