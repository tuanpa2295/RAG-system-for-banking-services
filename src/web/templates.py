"""
HTML Templates for Banking RAG System

Web interface templates for the Banking RAG system.
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banking RAG System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .query-panel, .response-panel {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .query-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 15px;
            min-height: 100px;
            resize: vertical;
        }
        .query-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .query-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        .query-button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .response-area {
            min-height: 200px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            font-family: 'Georgia', serif;
            line-height: 1.6;
        }
        .sources {
            margin-top: 20px;
            padding: 15px;
            background: #e8f4fd;
            border-left: 4px solid #007bff;
            border-radius: 0 8px 8px 0;
        }
        .source-item {
            margin: 5px 0;
            font-size: 14px;
        }
        .sample-queries {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .sample-button {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 10px 15px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            display: inline-block;
            font-size: 14px;
            transition: all 0.2s;
        }
        .sample-button:hover {
            background: #e9ecef;
            border-color: #adb5bd;
        }
        .loading {
            color: #666;
            font-style: italic;
        }
        .confidence {
            float: right;
            background: #28a745;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
        }
        .confidence.medium { background: #ffc107; color: #212529; }
        .confidence.low { background: #dc3545; }
        .stats {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .stat-item {
            display: inline-block;
            margin: 0 20px;
            padding: 10px;
        }
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏦 Banking RAG System</h1>
        <p>AI-Powered Banking & Financial Services Q&A</p>
        <p><em>Enhanced with comprehensive knowledge base and advanced retrieval</em></p>
    </div>

    <div class="stats">
        <div class="stat-item">
            <div class="stat-number" id="docCount">15+</div>
            <div class="stat-label">Knowledge Documents</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">10+</div>
            <div class="stat-label">Service Categories</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">AI Availability</div>
        </div>
    </div>

    <div class="container">
        <div class="query-panel">
            <h3>Ask a Banking Question</h3>
            <textarea id="queryInput" class="query-input" placeholder="Type your banking question here, for example: 'What are the requirements for getting a personal loan?'"></textarea>
            <button id="submitBtn" class="query-button" onclick="submitQuery()">Submit Query</button>
        </div>

        <div class="response-panel">
            <h3>AI Response</h3>
            <div id="responseArea" class="response-area">
                Welcome to the Banking RAG System! Ask any banking or financial services question and get instant, accurate answers based on our comprehensive knowledge base.
                
Our system covers:
• Personal and business loans
• Savings and investment accounts  
• Credit cards and mortgages
• Digital banking services
• Regulatory compliance
• Customer support information
            </div>
            <div id="sourcesArea" class="sources" style="display: none;">
                <strong>Sources:</strong>
                <div id="sourcesList"></div>
            </div>
        </div>
    </div>

    <div class="sample-queries">
        <h3>Sample Questions</h3>
        <p>Click any sample question to try it out:</p>
        <div class="sample-button" onclick="setQuery('What are the requirements for getting a personal loan?')">Personal Loan Requirements</div>
        <div class="sample-button" onclick="setQuery('How do I open a savings account and what are the benefits?')">Savings Account Information</div>
        <div class="sample-button" onclick="setQuery('What is the process for applying for a credit card?')">Credit Card Application</div>
        <div class="sample-button" onclick="setQuery('What investment options do you offer?')">Investment Options</div>
        <div class="sample-button" onclick="setQuery('How secure is mobile banking?')">Mobile Banking Security</div>
        <div class="sample-button" onclick="setQuery('What do I need to qualify for a mortgage?')">Mortgage Requirements</div>
        <div class="sample-button" onclick="setQuery('What business banking services are available?')">Business Banking</div>
        <div class="sample-button" onclick="setQuery('What are the current interest rates?')">Interest Rates</div>
        <div class="sample-button" onclick="setQuery('Do you offer cryptocurrency services?')">Crypto Services</div>
        <div class="sample-button" onclick="setQuery('What wealth management services are available?')">Wealth Management</div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }

        async function submitQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const responseArea = document.getElementById('responseArea');
            const sourcesArea = document.getElementById('sourcesArea');
            const sourcesList = document.getElementById('sourcesList');

            if (!query) {
                alert('Please enter a question');
                return;
            }

            // Disable button and show loading
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            responseArea.innerHTML = 'Processing your question...\\n\\nSearching through our knowledge base...';
            responseArea.className = 'response-area loading';
            sourcesArea.style.display = 'none';

            try {
                const response = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    responseArea.innerHTML = data.answer;
                    responseArea.className = 'response-area';

                    // Show sources
                    if (data.sources && data.sources.length > 0) {
                        sourcesList.innerHTML = '';
                        data.sources.forEach(source => {
                            const sourceItem = document.createElement('div');
                            sourceItem.className = 'source-item';
                            const confidenceClass = source.relevance_score > 0.8 ? 'high' : source.relevance_score > 0.6 ? 'medium' : 'low';
                            sourceItem.innerHTML = `
                                <strong>${source.title}</strong> (${source.category})
                                <span class="confidence ${confidenceClass}">${(source.relevance_score * 100).toFixed(0)}%</span>
                            `;
                            sourcesList.appendChild(sourceItem);
                        });
                        sourcesArea.style.display = 'block';
                    }
                } else {
                    responseArea.innerHTML = 'Error: ' + (data.message || 'Unknown error occurred');
                    responseArea.className = 'response-area';
                }
            } catch (error) {
                responseArea.innerHTML = 'Error: Unable to process request. Please try again.';
                responseArea.className = 'response-area';
                console.error('Error:', error);
            } finally {
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Query';
            }
        }

        // Allow Enter key to submit (with Shift+Enter for new line)
        document.getElementById('queryInput').addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submitQuery();
            }
        });

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

        // Load stats when page loads
        window.addEventListener('load', loadStats);
    </script>
</body>
</html>
"""
