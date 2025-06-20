#!/usr/bin/env python3
"""
Start the MCP agent backend on port 8001
"""

import sys
import subprocess
import os

def main():
    """Start the agent backend"""
    print("Starting MCP Agent backend on http://localhost:8001...")
    
    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set!")
        print("Please set it with: export OPENAI_API_KEY=your_api_key")
        print("Or create a .env file with: OPENAI_API_KEY=your_api_key")
    
    # Use PDM to run the agent backend
    try:
        subprocess.run([
            "pdm", "run", "python", "-m", "backend.main"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start agent backend: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAgent backend stopped.")

if __name__ == "__main__":
    main()