#!/usr/bin/env python
"""
Direct test script for NEAR Rubric MCP Server using a single JSON-RPC request.
"""

import json
import subprocess
import os

def send_simple_request():
    """Send a simple get_evaluation_framework request to test the server."""
    
    # Create JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": "get_evaluation_framework",
            "arguments": {
                "category": "near_integration",
                "project_type": "rust"
            }
        },
        "id": 1
    }
    
    # Write request to a file
    with open("test_request.json", "w") as f:
        json.dump(request, f)
    
    print("Sending request to server.py...")
    print(json.dumps(request, indent=2))
    
    # Execute command
    cmd = "type test_request.json | near-rubric-mcp\\server.py"
    result = subprocess.run(
        cmd, 
        shell=True, 
        capture_output=True, 
        text=True
    )
    
    print("\nServer Response:")
    try:
        response = json.loads(result.stdout)
        print(json.dumps(response, indent=2))
    except json.JSONDecodeError:
        print("Invalid JSON response:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    
    # Clean up
    if os.path.exists("test_request.json"):
        os.unlink("test_request.json")

if __name__ == "__main__":
    print("NEAR Rubric MCP Server Direct Test")
    print("=================================")
    send_simple_request() 