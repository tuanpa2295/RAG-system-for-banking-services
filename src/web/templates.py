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
        .mic-recording {
            background-color: #dc3545 !important;
            color: white !important;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .speech-controls {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        .ai-message-container {
            position: relative;
            padding-bottom: 35px; /* Add space for the button */
        }
        .speaker-btn {
            position: absolute;
            bottom: -30px;
            left: 0px;
            border: none;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.3s, background 0.3s;
            color: white;
            z-index: 10;
        }
        .speaker-btn:hover {
            opacity: 1;
            background: rgba(0, 0, 0, 0.9);
        }
        .speaker-btn.speaking {
            background: #198754;
            color: white;
            opacity: 1;
            animation: pulse 1s infinite;
        }
        .speaker-btn.paused {
            background: #ffc107;
            color: #000;
            opacity: 1;
        }
        
        /* Sidebar Menu Styles */
        .settings-sidebar {
            position: fixed;
            top: 0;
            left: -300px;
            width: 300px;
            height: 100vh;
            background: white;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            transition: left 0.3s ease;
            z-index: 1000;
            overflow-y: auto;
        }
        .settings-sidebar.open {
            left: 0;
        }
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .sidebar-content {
            padding: 20px;
        }
        .sidebar-section {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .sidebar-section:last-child {
            border-bottom: none;
        }
        .sidebar-section h4 {
            color: #333;
            margin-bottom: 15px;
            font-size: 16px;
        }
        .voice-setting-group {
            margin-bottom: 15px;
        }
        .voice-setting-group label {
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-size: 14px;
        }
        .voice-setting-group select,
        .voice-setting-group input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
        }
        .close-sidebar {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            color: white;
            font-size: 20px;
            cursor: pointer;
            opacity: 0.8;
        }
        .close-sidebar:hover {
            opacity: 1;
        }
        .settings-toggle {
            position: fixed;
            top: 20px;
            left: 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transition: background 0.3s;
            z-index: 999;
        }
        .settings-toggle:hover {
            background: #5a6fd8;
        }
        .sidebar-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.5);
            z-index: 999;
            display: none;
        }
        .sidebar-overlay.visible {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container py-4">
        <!-- Settings Toggle Button -->
        <button class="settings-toggle" onclick="toggleSettingsSidebar()" title="Voice Settings">
            <i class="bi bi-gear"></i>
        </button>

        <!-- Settings Sidebar -->
        <div class="sidebar-overlay" onclick="closeSettingsSidebar()"></div>
        <div class="settings-sidebar" id="settingsSidebar">
            <div class="sidebar-header">
                <i class="bi bi-gear"></i> Voice Settings
                <button class="close-sidebar" onclick="closeSettingsSidebar()">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            <div class="sidebar-content">
                <div class="sidebar-section">
                    <h4><i class="bi bi-person-voice"></i> Text-to-Speech Settings</h4>
                    <div class="voice-setting-group">
                        <label for="globalVoiceSelect">Voice:</label>
                        <select id="globalVoiceSelect" onchange="updateGlobalVoice()">
                            <option value="">Default Voice</option>
                        </select>
                    </div>
                    <div class="voice-setting-group">
                        <label for="speechRate">Speed:</label>
                        <input type="range" id="speechRate" min="0.5" max="2" step="0.1" value="0.8" onchange="updateSpeechRate()">
                        <small class="text-muted">Current: <span id="rateValue">0.8</span>x</small>
                    </div>
                    <div class="voice-setting-group">
                        <label for="speechPitch">Pitch:</label>
                        <input type="range" id="speechPitch" min="0.5" max="2" step="0.1" value="1" onchange="updateSpeechPitch()">
                        <small class="text-muted">Current: <span id="pitchValue">1.0</span></small>
                    </div>
                    <div class="voice-setting-group">
                        <label for="speechVolume">Volume:</label>
                        <input type="range" id="speechVolume" min="0" max="1" step="0.1" value="1" onchange="updateSpeechVolume()">
                        <small class="text-muted">Current: <span id="volumeValue">100</span>%</small>
                    </div>
                </div>
                <div class="sidebar-section">
                    <h4><i class="bi bi-mic"></i> Speech Recognition Settings</h4>
                    <div class="voice-setting-group">
                        <label for="speechLang">Language:</label>
                        <select id="speechLang" onchange="updateSpeechLanguage()">
                            <option value="en-US">English (US)</option>
                            <option value="en-GB">English (UK)</option>
                            <option value="en-AU">English (Australia)</option>
                            <option value="es-ES">Spanish</option>
                            <option value="fr-FR">French</option>
                            <option value="de-DE">German</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

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

                        <div class="chat-input-container">
                            <form onsubmit="event.preventDefault(); submitQuery();">
                                <div class="input-group">
                                    <textarea id="queryInput" class="form-control" 
                                            placeholder="Type your banking question here or use the microphone..." 
                                            rows="2"
                                            style="resize: none;"></textarea>
                                    <button id="micBtn" type="button" class="btn btn-outline-secondary" onclick="toggleSpeechRecognition()">
                                        <i class="bi bi-mic"></i>
                                    </button>
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
        function setQuery(query) {
            document.getElementById('queryInput').value = query;
        }

        async function submitQuery() {
            const query = document.getElementById('queryInput').value.trim();
            const submitBtn = document.getElementById('submitBtn');
            const chatbox = document.getElementById('chatbox');
            const sourcesArea = document.getElementById('sourcesArea');
            const sourcesList = document.getElementById('sourcesList');

            if (!query) {
                showToast('Please enter a question', 'warning');
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
                const response = await fetch('/api/v1/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Remove typing indicator
                    chatbox.removeChild(typingIndicator);

                    // Add AI response to chat
                    const aiMessage = document.createElement('div');
                    aiMessage.className = 'message ai ai-message-container';
                    aiMessage.innerHTML = `
                        <div class="message-content" id="msg-${Date.now()}">${data.answer}</div>
                        <button class="speaker-btn" onclick="toggleSpeechReading(this)" title="Read response aloud">
                            <i class="bi bi-volume-up"></i>
                        </button>
                    `;
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

        // Speech Recognition Variables
        let recognition = null;
        let isRecording = false;
        let speechSynthesis = window.speechSynthesis;
        let currentUtterance = null;
        let currentSpeakerButton = null;
        let isPaused = false;
        let availableVoices = [];
        
        // Global speech settings
        let globalVoice = null;
        let speechRate = 0.8;
        let speechPitch = 1.0;
        let speechVolume = 1.0;
        let speechLanguage = 'en-US';

        // Initialize Speech Recognition
        function initSpeechRecognition() {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = speechLanguage;
                
                recognition.onstart = function() {
                    console.log('Speech recognition started');
                    const micBtn = document.getElementById('micBtn');
                    micBtn.classList.add('mic-recording');
                    micBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
                };
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    document.getElementById('queryInput').value = transcript;
                    console.log('Speech recognized:', transcript);
                };
                
                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    stopRecording();
                    // Removed toast notification for speech recognition errors
                };
                
                recognition.onend = function() {
                    console.log('Speech recognition ended');
                    stopRecording();
                };
                
                return true;
            } else {
                console.warn('Speech recognition not supported');
                showToast('Speech recognition not supported in this browser', 'warning');
                return false;
            }
        }

        // Toggle Speech Recognition
        function toggleSpeechRecognition() {
            if (!recognition && !initSpeechRecognition()) {
                return;
            }
            
            if (isRecording) {
                recognition.stop();
            } else {
                recognition.start();
                isRecording = true;
            }
        }

        // Stop Recording
        function stopRecording() {
            isRecording = false;
            const micBtn = document.getElementById('micBtn');
            micBtn.classList.remove('mic-recording');
            micBtn.innerHTML = '<i class="bi bi-mic"></i>';
        }

        // Integrated Text-to-Speech Function with Pause/Resume
        function toggleSpeechReading(button) {
            const messageContainer = button.closest('.ai-message-container');
            const messageContent = messageContainer.querySelector('.message-content');
            const textContent = messageContent.textContent;
            
            // If currently speaking from this button
            if (currentSpeakerButton === button && speechSynthesis.speaking) {
                if (isPaused) {
                    // Resume
                    speechSynthesis.resume();
                    isPaused = false;
                    button.classList.remove('paused');
                    button.classList.add('speaking');
                    button.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
                    button.title = 'Pause reading';
                } else {
                    // Pause
                    speechSynthesis.pause();
                    isPaused = true;
                    button.classList.remove('speaking');
                    button.classList.add('paused');
                    button.innerHTML = '<i class="bi bi-play-fill"></i>';
                    button.title = 'Resume reading';
                }
                return;
            }
            
            // If this is the same button but speech has ended (handle edge case)
            if (currentSpeakerButton === button && !speechSynthesis.speaking) {
                // Reset the state and start fresh
                resetSpeechControls(button);
            }
            
            // Stop any currently playing speech and reset all states
            if (speechSynthesis.speaking || isPaused) {
                speechSynthesis.cancel();
                resetAllSpeechControls();
                
                // Small delay to ensure speech is fully stopped
                setTimeout(() => {
                    startNewSpeech(button, textContent);
                }, 100);
            } else {
                startNewSpeech(button, textContent);
            }
        }

        // Start New Speech Function
        function startNewSpeech(button, textContent) {
            // Ensure clean state
            currentUtterance = null;
            currentSpeakerButton = null;
            isPaused = false;
            
            // Create new speech
            const utterance = new SpeechSynthesisUtterance(textContent);
            utterance.rate = speechRate;
            utterance.pitch = speechPitch;
            utterance.volume = speechVolume;
            
            // Set global voice or default to English
            if (globalVoice) {
                utterance.voice = globalVoice;
            } else {
                const englishVoice = availableVoices.find(voice => voice.lang.startsWith('en'));
                if (englishVoice) {
                    utterance.voice = englishVoice;
                }
            }
            
            // Store current elements and reset state
            currentUtterance = utterance;
            currentSpeakerButton = button;
            isPaused = false;
            
            utterance.onstart = function() {
                button.classList.add('speaking');
                button.innerHTML = '<i class="bi bi-volume-up-fill"></i>';
                button.title = 'Pause reading';
            };
            
            utterance.onend = function() {
                resetSpeechControls(button);
            };
            
            utterance.onerror = function(event) {
                console.error('Speech synthesis error:', event.error);
                resetSpeechControls(button);
                // Removed toast notification for speech errors
            };
            
            speechSynthesis.speak(utterance);
        }

        // Settings Sidebar Functions
        function toggleSettingsSidebar() {
            const sidebar = document.getElementById('settingsSidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.toggle('open');
            overlay.classList.toggle('visible');
        }

        function closeSettingsSidebar() {
            const sidebar = document.getElementById('settingsSidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            
            sidebar.classList.remove('open');
            overlay.classList.remove('visible');
        }

        // Voice Settings Functions
        function updateGlobalVoice() {
            const select = document.getElementById('globalVoiceSelect');
            const selectedIndex = select.value;
            
            if (selectedIndex && availableVoices[selectedIndex]) {
                globalVoice = availableVoices[selectedIndex];
            } else {
                globalVoice = null;
            }
            
            // Apply immediately if speech is currently playing
            applyVoiceSettingsImmediately();
        }

        function updateSpeechRate() {
            const slider = document.getElementById('speechRate');
            speechRate = parseFloat(slider.value);
            document.getElementById('rateValue').textContent = speechRate;
            
            // Apply immediately if speech is currently playing
            applyVoiceSettingsImmediately();
        }

        function updateSpeechPitch() {
            const slider = document.getElementById('speechPitch');
            speechPitch = parseFloat(slider.value);
            document.getElementById('pitchValue').textContent = speechPitch;
            
            // Apply immediately if speech is currently playing
            applyVoiceSettingsImmediately();
        }

        function updateSpeechVolume() {
            const slider = document.getElementById('speechVolume');
            speechVolume = parseFloat(slider.value);
            document.getElementById('volumeValue').textContent = Math.round(speechVolume * 100);
            
            // Apply immediately if speech is currently playing
            applyVoiceSettingsImmediately();
        }

        function updateSpeechLanguage() {
            const select = document.getElementById('speechLang');
            speechLanguage = select.value;
            
            // Update speech recognition language
            if (recognition) {
                recognition.lang = speechLanguage;
            }
        }

        // Apply Voice Settings Immediately
        function applyVoiceSettingsImmediately() {
            if (currentUtterance && speechSynthesis.speaking) {
                // Store current position and text
                const currentButton = currentSpeakerButton;
                const messageContainer = currentButton.closest('.ai-message-container');
                const messageContent = messageContainer.querySelector('.message-content');
                const textContent = messageContent.textContent;
                const wasPlaying = !isPaused;
                
                // Cancel current speech
                speechSynthesis.cancel();
                
                // Wait a moment for cancel to complete, then restart with new settings
                setTimeout(() => {
                    if (currentButton && wasPlaying) {
                        // Reset states
                        resetAllSpeechControls();
                        
                        // Start fresh with new settings
                        startNewSpeech(currentButton, textContent);
                    }
                }, 150);
            }
        }

        // Load Available Voices
        function loadVoices() {
            availableVoices = speechSynthesis.getVoices();
            
            // Populate global voice selector
            const globalSelect = document.getElementById('globalVoiceSelect');
            if (globalSelect) {
                globalSelect.innerHTML = '<option value="">Default Voice</option>';
                
                availableVoices.forEach((voice, index) => {
                    const option = document.createElement('option');
                    option.value = index;
                    option.textContent = `${voice.name} (${voice.lang})`;
                    globalSelect.appendChild(option);
                });
            }
        }

        // Reset Speech Controls
        function resetSpeechControls(speakerButton) {
            if (speakerButton) {
                speakerButton.classList.remove('speaking', 'paused');
                speakerButton.innerHTML = '<i class="bi bi-volume-up"></i>';
                speakerButton.title = 'Read response aloud';
            }
            
            currentUtterance = null;
            currentSpeakerButton = null;
            isPaused = false;
        }

        // Reset All Speech Controls
        function resetAllSpeechControls() {
            document.querySelectorAll('.speaker-btn').forEach(btn => {
                btn.classList.remove('speaking', 'paused');
                btn.innerHTML = '<i class="bi bi-volume-up"></i>';
                btn.title = 'Read response aloud';
            });
            
            currentUtterance = null;
            currentSpeakerButton = null;
            isPaused = false;
        }

        // Show Toast Notification
        function showToast(message, type = 'info') {
            const toastEl = document.createElement('div');
            const bgClass = type === 'error' ? 'bg-danger' : type === 'warning' ? 'bg-warning text-dark' : 'bg-info';
            toastEl.innerHTML = `
                <div class="toast-container position-fixed bottom-0 end-0 p-3">
                    <div class="toast" role="alert">
                        <div class="toast-header ${bgClass} text-white">
                            <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                        </div>
                        <div class="toast-body">
                            ${message}
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(toastEl);
            const toast = new bootstrap.Toast(toastEl.querySelector('.toast'));
            toast.show();
            setTimeout(() => toastEl.remove(), 5000);
        }

        // Initialize speech recognition on page load
        window.addEventListener('load', function() {
            initSpeechRecognition();
            
            // Load voices for speech synthesis
            loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = loadVoices;
            }
        });

        // Handle page unload to stop speech
        window.addEventListener('beforeunload', function() {
            if (speechSynthesis.speaking) {
                speechSynthesis.cancel();
            }
        });

        // Handle visibility change to pause/resume speech
        document.addEventListener('visibilitychange', function() {
            if (document.hidden && speechSynthesis.speaking && !isPaused) {
                // Auto-pause when tab becomes hidden
                if (currentSpeakerButton) {
                    toggleSpeechReading(currentSpeakerButton);
                }
            }
        });
    </script>
</body>
</html>'''
