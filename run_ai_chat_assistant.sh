#!/bin/bash

# Serve the docs directory using Python's built-in HTTP server
cd "$(dirname "$0")/docs"

# Start the server in the background
python3 -m http.server 8000 &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Open the AI Chat Assistant page in the default browser
xdg-open "http://localhost:8000/ai-chat-assistant.html" 2>/dev/null || open "http://localhost:8000/ai-chat-assistant.html" 2>/dev/null || start "http://localhost:8000/ai-chat-assistant.html"

# Wait for the server process to end (Ctrl+C to stop)
wait $SERVER_PID 