#!/usr/bin/env python
"""
Simple test script for NEAR Rubric MCP Server using direct JSON-RPC requests.
"""

import json
import subprocess
import tempfile
import os
import glob

def call_jsonrpc(request_obj):
    """
    Make a JSON-RPC call to the server.py
    
    Args:
        request_obj: The JSON-RPC request object
        
    Returns:
        The parsed JSON response
    """
    # Create a temporary file for the request
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp:
        temp_path = temp.name
        json.dump(request_obj, temp)
    
    try:
        # Windows command to pipe the JSON to server.py
        cmd = f'type {temp_path} | python server.py'
        
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=False
        )
        
        # Parse the response
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response",
                "raw": result.stdout,
                "stderr": result.stderr
            }
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_path)
        except:
            pass

def find_contract_files():
    """Find contract-related files in the monorepo."""
    monorepo_path = "../repos_to_audit/monorepo"
    
    # Search for contract files
    contract_paths = []
    
    # Search for specific patterns
    patterns = [
        os.path.join(monorepo_path, "**", "contracts", "**", "*.rs"),
        os.path.join(monorepo_path, "**", "contract", "**", "*.rs"),
        os.path.join(monorepo_path, "**", "near", "**", "*.{js,ts}"),
        os.path.join(monorepo_path, "**", "Cargo.toml")
    ]
    
    for pattern in patterns:
        # Use glob for pattern matching
        for file_path in glob.glob(pattern, recursive=True):
            # Convert to relative path
            rel_path = os.path.relpath(file_path, start=monorepo_path)
            contract_paths.append(rel_path)
    
    return contract_paths

def test_get_file_suggestions():
    """Test the get_file_suggestions tool with hand-picked files."""
    print("Testing get_file_suggestions...")
    
    # Find contract files
    monorepo_files = find_contract_files()
    
    if not monorepo_files:
        print("No contract files found. Using sample file list.")
        monorepo_files = [
            "contracts/src/lib.rs",
            "contracts/src/main.rs",
            "contracts/Cargo.toml"
        ]
    
    print(f"Found {len(monorepo_files)} contract-related files:")
    for file in monorepo_files[:10]:  # Show first 10 files
        print(f"- {file}")
    
    # Create JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": "get_file_suggestions",
            "arguments": {
                "category": "near_integration",
                "available_files": monorepo_files
            }
        },
        "id": 1
    }
    
    # Call the server
    response = call_jsonrpc(request)
    print("\nResponse:")
    print(json.dumps(response, indent=2))
    
    # Try to extract suggested files
    suggested_files = []
    if response and "result" in response and "suggested_files" in response["result"]:
        suggested_files = response["result"]["suggested_files"]
    
    return suggested_files

def analyze_file_content(file_path):
    """Analyze a specific file for NEAR integration patterns."""
    print(f"\nAnalyzing file: {file_path}")
    
    monorepo_path = "../repos_to_audit/monorepo"
    full_path = os.path.join(monorepo_path, file_path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {
                "name": "analyze_pattern_matches",
                "arguments": {
                    "category": "near_integration",
                    "code_content": {file_path: content},
                    "project_type": "mixed" 
                }
            },
            "id": 2
        }
        
        # Call the server
        response = call_jsonrpc(request)
        print("Analysis Result:")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error analyzing file {full_path}: {str(e)}")

if __name__ == "__main__":
    print("NEAR Rubric MCP Server Direct JSON-RPC Test")
    print("===========================================")
    
    # Test get_file_suggestions
    suggested_files = test_get_file_suggestions()
    
    # Analyze first suggested file if available
    if suggested_files:
        print(f"\nFound {len(suggested_files)} suggested files for analysis")
        if len(suggested_files) > 0:
            analyze_file_content(suggested_files[0])
    else:
        print("No suggested files found for analysis")
        
        # Try to analyze a specific file directly
        contract_files = find_contract_files()
        if contract_files:
            analyze_file_content(contract_files[0]) 