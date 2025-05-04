# NEAR Rubric MCP Server

## Overview

The NEAR Rubric MCP (Model-Code-Project) Server is a specialized tool for evaluating NEAR Protocol projects according to defined rubrics. It provides AI-friendly tools to analyze code, suggest relevant files, and generate evaluation frameworks for assessing NEAR integration quality, on-chain code quality, and other aspects of NEAR blockchain projects.

## Features

- **File Pattern Matching**: Advanced glob and regex pattern matching to identify relevant files in a codebase
- **Code Analysis**: Identify patterns in code that indicate NEAR integration quality
- **Evaluation Frameworks**: Generate structured prompts for consistent project evaluation
- **Cross-Platform Support**: Works on both Windows and Unix-based systems

## Key Components

The server consists of several modules:

1. **server.py**: Main JSON-RPC server implementation
2. **evaluation/**
   - **file_matcher.py**: Advanced glob pattern matching
   - **pattern_library.py**: Pattern detection in code files
   - **orchestrator.py**: Coordinates evaluation process
   - **prompt_generator.py**: Generates evaluation prompts

## Tools

The server provides the following tools via JSON-RPC:

1. **get_evaluation_framework**: Returns evaluation framework for a specific category
2. **get_file_suggestions**: Suggests relevant files to analyze for a category
3. **analyze_code_context**: Analyzes provided code against rubric
4. **analyze_pattern_matches**: Finds pattern matches in code files

## Usage

### Running the Server

```bash
python server.py
```

### Testing the Server

```bash
python test_client.py
```

### Client Integration

The server uses a simple JSON-RPC protocol. Example request:

```json
{
  "jsonrpc": "2.0",
  "method": "call_tool",
  "params": {
    "name": "get_file_suggestions",
    "arguments": {
      "category": "near_integration",
      "available_files": ["src/lib.rs", "frontend/near-wallet.js"]
    }
  },
  "id": 1
}
```

## Patterns and Configuration

Pattern configurations are stored in YAML files in the `config/` directory. You can modify these to adjust detection patterns for different project types.

## License

This project is part of the NEAR ecosystem tooling. 