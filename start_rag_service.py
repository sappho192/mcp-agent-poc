#!/usr/bin/env python3
"""
Start the dummy RAG microservice on port 8000
"""

import sys
import subprocess
import os

def main():
    """Start the RAG service"""
    print("Starting RAG microservice on http://localhost:8000...")
    
    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Use PDM to run the RAG service
    try:
        subprocess.run([
            "pdm", "run", "python", "-m", "backend.rag_service.dummy_rag"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to start RAG service: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nRAG service stopped.")

if __name__ == "__main__":
    main()