# Testing the NEAR Rubric MCP Server

This guide provides hands-on approaches for testing the NEAR Rubric MCP Server against your NEAR projects. We'll cover multiple testing methods, from direct JSON-RPC calls to utilizing the provided test clients.

## Prerequisites

- Python 3.8 or higher
- A NEAR project to audit (or use our sample monorepo)
- Basic familiarity with command line tools

## Testing Options

The NEAR Rubric MCP Server supports three primary testing approaches, each with different use cases:

1. **Direct JSON-RPC Requests** - Simple, lightweight testing for specific tools
2. **Python Test Script** - Programmatic testing with detailed analysis
3. **Test Client Utility** - Comprehensive testing with the pre-built test client

## Option 1: Direct JSON-RPC Requests

The simplest way to test the MCP server is by sending JSON-RPC requests directly to it. This approach is ideal for quick tests or when you want to integrate the MCP server into non-Python tools.

### Workshop Steps

1. **Create a JSON request file** named `test_request.json`:

```json
{
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
```

2. **Run the server with your request**:

```bash
# Linux/MacOS
cat test_request.json | python near-rubric-mcp/server.py

# Windows PowerShell
type test_request.json | python near-rubric-mcp\server.py
```

3. **Create a batch/shell script** for convenience:

For Windows (`test_mcp.cmd`):
```
@echo off
echo Testing NEAR Rubric MCP Server
echo ==============================
echo.
echo Sending request to server.py...
type test_request.json | python near-rubric-mcp\server.py
echo.
echo Done
```

For Linux/MacOS (`test_mcp.sh`):
```bash
#!/bin/bash
echo "Testing NEAR Rubric MCP Server"
echo "=============================="
echo
echo "Sending request to server.py..."
cat test_request.json | python near-rubric-mcp/server.py
echo
echo "Done"
```

## Option 2: Python Test Script

This approach gives you programmatic control over sending requests and processing responses.

### Workshop Steps

1. **Create a test script** named `rpc_test.py`:

```python
#!/usr/bin/env python
"""
Script to send JSON-RPC requests directly to the MCP server.
"""

import json
import subprocess
import os

def send_jsonrpc_request(request_obj):
    """
    Send a JSON-RPC request to the server.py process.
    """
    # Convert request to JSON string
    request_json = json.dumps(request_obj)
    
    # Get the path to server.py
    server_path = os.path.join("near-rubric-mcp", "server.py")
    
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

def analyze_code_file(file_path):
    """Analyze a specific file from a project."""
    project_path = "repos_to_audit/monorepo"
    
    # Fix path separators for Windows
    file_path_os = file_path.replace('/', os.sep)
    full_path = os.path.join(project_path, file_path_os)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create JSON-RPC request for pattern analysis
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
            "id": 1
        }
        
        return send_jsonrpc_request(request)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Specify the file you want to analyze
    contract_file = "contracts/src/ai-gaming-club.js"
    
    print(f"Analyzing file: {contract_file}")
    result = analyze_code_file(contract_file)
    
    # Print the result
    print(json.dumps(result, indent=2))
```

2. **Run the test script**:

```bash
python rpc_test.py
```

This script will analyze a specific file for NEAR integration patterns and display the results.

3. **Extending the script**:

You can extend this script to perform more complex testing scenarios:
- Analyzing multiple files
- Testing different evaluation categories
- Generating reports or visualizations
- Integrating with CI/CD pipelines

## Option 3: Test Client Utility

The MCP server comes with a built-in test client that provides a comprehensive way to test all server functionality.

### Workshop Steps

1. **Set up the proper Python package structure**:

First, ensure your directory structure is proper by creating an `__init__.py` file in the categories directory:

```python
"""
Categories package for NEAR Rubric MCP
"""
```

2. **Run the test client** from the correct directory:

```bash
cd near-rubric-mcp
python -m test_client
```

3. **Customize the test client**:

The `test_client.py` file contains various test functions. You can modify it to test specific aspects of your NEAR project.

For example, to test your own monorepo:

```python
def test_monorepo():
    """Test with actual monorepo files."""
    print("\nTesting with actual monorepo files...")
    
    # Get all the files in the monorepo
    monorepo_path = "../repos_to_audit/monorepo"
    all_files = []
    
    # Find all files in the monorepo recursively
    for root, dirs, files in os.walk(monorepo_path):
        for file in files:
            # Convert absolute path to relative path from monorepo root
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, start=monorepo_path)
            all_files.append(relative_path)
    
    # Test file suggestions for NEAR integration
    print(f"\nTesting file suggestions for monorepo...")
    response = call_tool("get_file_suggestions", {
        "category": "near_integration",
        "available_files": all_files[:200]  # Limit to 200 files
    })
    print_json(response)
    
    # Analyze suggested files...
```

## Tips and Troubleshooting

### Common Issues

- **Python Import Errors**: Ensure all directories have proper `__init__.py` files
- **File Not Found Errors**: Verify file paths are correct for your operating system
- **JSON Parsing Errors**: Check JSON syntax in your request files
- **No Results Found**: Make sure your project contains NEAR-related files

### Best Practices

- Start with simple tests to verify server operation
- Test one category at a time for clearer results
- Use real project files for most meaningful analysis
- Check server logs for detailed error information

## Next Steps

After testing, you can:

1. **Implement Improvements**: Use the evaluation results to enhance your NEAR integration
2. **Automate Testing**: Add MCP testing to your CI/CD pipeline
3. **Extend the Server**: Add custom evaluation categories for your specific needs

Happy testing! 