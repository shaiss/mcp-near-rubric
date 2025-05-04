# NEAR Rubric MCP Server

A Model Context Protocol (MCP) server for evaluating NEAR Protocol projects according to the NEAR Development Program rubric.

## Overview

This MCP server provides evaluation frameworks and prompts for scoring NEAR Protocol projects. It's designed to work with any MCP client (like Cursor) by providing structured evaluation data and guidance.

## Architecture

The server follows a client-agnostic approach:

- **Client-Agnostic**: Works with any MCP client, leveraging their capabilities
- **Evaluation Logic Only**: Provides evaluation criteria and prompts
- **Lightweight Server**: Minimal processing
- **Structured Guidance**: Returns evaluation frameworks for client-side processing

## Available Tools

- `get_evaluation_framework`: Get evaluation framework for a specific rubric category
- `analyze_code_context`: Analyze provided code context against rubric
- `get_file_suggestions`: Get suggestions for which files to analyze

## Categories

The server supports evaluation across these categories:

1. NEAR Protocol Integration (20 pts)
2. Onchain Quality (20 pts)
3. Offchain Quality (15 pts)
4. Code Quality & Documentation (15 pts)
5. Technical Innovation/Uniqueness (15 pts)
6. Team Activity & Project Maturity (10 pts)
7. Grant Impact & Ecosystem Fit (5 pts)

## Usage

### Running the Server

```bash
python server.py
```

The server communicates via JSON-RPC over stdio.

### Client Integration

```python
# Example of calling the MCP server from a client
import json
import subprocess

def call_mcp_tool(tool_name, arguments):
    """Call a tool from the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "method": "call_tool",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }
    
    # Call the MCP server process
    process = subprocess.Popen(
        ["python", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    # Send the request and get the response
    stdout, _ = process.communicate(json.dumps(request) + "\n")
    return json.loads(stdout)

# Example: Get evaluation framework for NEAR Integration
result = call_mcp_tool("get_evaluation_framework", {
    "category": "near_integration",
    "project_type": "rust"
})

print(result)
```

## Creating a New Category

You can easily add new evaluation categories using the category creation script:

```bash
python scripts/create_category.py --name "My New Category" --points 15
```

The script will:
1. Create a new category class in `categories/`
2. Add a prompt template in `resources/prompts/`
3. Update the `rubric.yaml` configuration
4. Update the `patterns.yaml` configuration

For more options, run:

```bash
python scripts/create_category.py --help
```

### Validating Configuration

To ensure all components are in sync, run the validation script:

```bash
python scripts/validate_config.py
```

This checks for:
- Categories missing prompt templates
- Categories missing from configuration files
- Orphaned prompt templates

## Extensibility

The server is designed to be highly extensible:

1. **Automatic Category Discovery**: Categories are automatically discovered and registered
2. **Dynamic Tool Listing**: Available tools are generated based on registered categories
3. **Configuration Validation**: Validation scripts ensure all components are in sync
4. **Template-Based Generation**: New categories can be generated from templates

## Configuration

Configuration files are in YAML format:

- `config/rubric.yaml`: Rubric specifications
- `config/patterns.yaml`: Pattern detection library

## Dependencies

- Python 3.7+
- PyYAML
- ujson (optional, for faster JSON processing)

## License

MIT 