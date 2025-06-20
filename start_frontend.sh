#!/bin/bash
"""
Start the React frontend on port 3000
"""

echo "Starting React frontend on http://localhost:3000..."

# Change to frontend directory
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start React development server
npm start