#!/usr/bin/env python
"""
Script to send JSON-RPC requests directly to the MCP server.
"""

import json
import subprocess
import sys
import os
import glob

def send_jsonrpc_request(request_obj):
    """
    Send a JSON-RPC request to the server.py process.
    
    Args:
        request_obj: Dictionary containing the JSON-RPC request
        
    Returns:
        Dictionary containing the parsed response or error information
    """
    # Convert request to JSON string
    request_json = json.dumps(request_obj)
    
    # Get the path to server.py
    server_path = os.path.join("near-rubric-mcp", "server.py")
    if not os.path.exists(server_path):
        print(f"Error: Server script not found at {server_path}")
        return {"error": f"Server script not found at {server_path}"}
    
    # Start the server.py process
    process = subprocess.Popen(
        ["python", server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send the request
    stdout, stderr = process.communicate(input=request_json + "\n")
    
    # Try to parse the response
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON response",
            "stdout": stdout,
            "stderr": stderr
        }

def get_evaluation_framework():
    """Get the evaluation framework for NEAR integration."""
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": "get_evaluation_framework",
            "arguments": {
                "category": "near_integration",
                "project_type": "mixed"
            }
        },
        "id": 1
    }
    
    print("Sending request:", json.dumps(request, indent=2))
    return send_jsonrpc_request(request)

def get_file_suggestions():
    """Get file suggestions for NEAR integration from the monorepo."""
    # Find all files in the monorepo
    monorepo_path = "repos_to_audit/monorepo"
    available_files = []
    
    # Better patterns for NEAR-related files
    patterns = [
        "contracts/src/**/*.js",
        "contracts/src/**/*.ts",
        "contracts/package.json", 
        "packages/**/*.js",
        "packages/**/*.ts",
        "**/README.md"
    ]
    
    # Gather files matching patterns
    for pattern in patterns:
        full_pattern = os.path.join(monorepo_path, pattern.replace('/', os.sep))
        matching_files = glob.glob(full_pattern, recursive=True)
        for file_path in matching_files:
            rel_path = os.path.relpath(file_path, start=monorepo_path).replace(os.sep, '/')
            available_files.append(rel_path)
    
    # If no files found, use some hardcoded examples
    if not available_files:
        available_files = [
            "contracts/package.json",
            "contracts/README.md",
            "packages/poker-state-machine/src/index.ts"
        ]
    
    print(f"Found {len(available_files)} potentially relevant files")
    for file in available_files[:5]:  # Print first 5
        print(f"- {file}")
    if len(available_files) > 5:
        print(f"... and {len(available_files) - 5} more")
    
    # Create JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": "get_file_suggestions",
            "arguments": {
                "category": "near_integration",
                "available_files": available_files
            }
        },
        "id": 2
    }
    
    print("\nSending request for file suggestions...")
    return send_jsonrpc_request(request)

def analyze_code_file(file_path):
    """Analyze a specific file from the monorepo."""
    monorepo_path = "repos_to_audit/monorepo"
    
    # Fix path separators for Windows
    file_path_os = file_path.replace('/', os.sep)
    full_path = os.path.join(monorepo_path, file_path_os)
    
    if not os.path.exists(full_path):
        print(f"Error: File not found: {full_path}")
        return {"error": f"File not found: {full_path}"}
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create code context with the file content
        code_context = {file_path: content}
        
        # Create JSON-RPC request for pattern analysis
        request = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {
                "name": "analyze_pattern_matches",
                "arguments": {
                    "category": "near_integration",
                    "code_content": code_context,
                    "project_type": "mixed"
                }
            },
            "id": 3
        }
        
        print(f"\nAnalyzing file: {file_path}")
        return send_jsonrpc_request(request)
    except Exception as e:
        print(f"Error reading or analyzing file: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("NEAR Rubric MCP Direct JSON-RPC Test")
    print("==================================")
    
    # Test 1: Get evaluation framework
    print("\n1. Testing get_evaluation_framework")
    framework_response = get_evaluation_framework()
    print("Evaluation framework retrieved successfully!")
    
    # Test 2: Get file suggestions
    print("\n2. Testing get_file_suggestions")
    file_suggestions_response = get_file_suggestions()
    
    # Extract suggested files from response
    suggested_files = []
    if (file_suggestions_response and 
        "result" in file_suggestions_response and 
        "suggested_files" in file_suggestions_response["result"]):
        suggested_files = file_suggestions_response["result"]["suggested_files"]
    
    print(f"\nResponse from file suggestions request:")
    print(json.dumps(file_suggestions_response, indent=2))
    
    # Test 3: Analyze a specific file
    print("\n3. Testing analyze_pattern_matches")
    if suggested_files:
        # Analyze the first suggested file
        first_file = suggested_files[0]
        analysis_response = analyze_code_file(first_file)
        print(f"\nAnalysis result for {first_file}:")
        print(json.dumps(analysis_response, indent=2))
    else:
        # Try to analyze a hardcoded file
        print("No suggested files found. Trying a hardcoded example...")
        example_file = "contracts/package.json"
        analysis_response = analyze_code_file(example_file)
        print(f"\nAnalysis result for {example_file}:")
        print(json.dumps(analysis_response, indent=2))
    
    # Test 4: Analyze a specific contract file
    print("\n4. Testing analyze_pattern_matches with a NEAR contract file")
    contract_file = "contracts/src/ai-gaming-club.js"
    contract_analysis = analyze_code_file(contract_file)
    print(f"\nAnalysis result for {contract_file}:")
    print(json.dumps(contract_analysis, indent=2)) 