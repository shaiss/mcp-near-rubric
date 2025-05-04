# NEAR Rubric MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📋 Overview

The NEAR Rubric MCP (Model-Code-Project) Server is a specialized tool for evaluating NEAR Protocol projects according to defined rubrics. It provides AI-friendly tools to analyze code, suggest relevant files, and generate evaluation frameworks for assessing NEAR integration quality, on-chain code quality, and other aspects of NEAR blockchain projects.

## ✨ Features

- **Natural Language Interface**: Ask AI assistants to audit your NEAR projects with simple natural language queries
- **File Pattern Matching**: Advanced glob and regex pattern matching to identify relevant files in a codebase
- **Code Analysis**: Identify patterns in code that indicate NEAR integration quality
- **Evaluation Frameworks**: Generate structured prompts for consistent project evaluation
- **Cross-Platform Support**: Works on both Windows and Unix-based systems

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Cursor IDE](https://www.cursor.so/) installed

### Installation & Setup

1. **Clone the MCP Server Repository**
   ```bash
   git clone https://github.com/your-org/near-rubric-mcp.git
   cd near-rubric-mcp
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Clone the NEAR Project to Audit**
   ```bash
   git clone https://github.com/your-project/near-project.git
   ```

4. **Start the MCP Server**
   ```bash
   python server.py
   ```

## 💬 Using with Natural Language in Cursor

The NEAR Rubric MCP is designed to work seamlessly with Cursor's AI assistants through natural language. Once set up, you can simply ask:

```
run a near audit on [xyz] local repo
```

The AI assistant will:
1. Understand your natural language request
2. Identify the relevant NEAR evaluation categories
3. Find and analyze the appropriate files in your codebase
4. Generate a comprehensive evaluation based on the NEAR rubric
5. Present you with scores, justifications, and recommendations

### Example Natural Language Queries

- **General audit**: "Analyze this NEAR project according to the rubric"
- **Specific category**: "Evaluate the NEAR integration quality of this codebase"
- **Targeted analysis**: "Check the onchain quality of this NEAR project"

No need to manually construct JSON-RPC requests or understand the underlying API - the natural language interface handles all the complexity for you.

## 🔧 Testing the Server

You can test if the server is functioning correctly with:

```bash
python test_client.py
```

## 🏗️ Architecture

The server consists of several key modules:

1. **server.py**: Main JSON-RPC server implementation
2. **evaluation/**
   - **file_matcher.py**: Advanced glob pattern matching
   - **pattern_library.py**: Pattern detection in code files
   - **orchestrator.py**: Coordinates evaluation process
   - **prompt_generator.py**: Generates evaluation prompts

## 🛠️ Tools

The server provides the following tools via JSON-RPC:

1. **get_evaluation_framework**: Returns evaluation framework for a specific category
2. **get_file_suggestions**: Suggests relevant files to analyze for a category
3. **analyze_code_context**: Analyzes provided code against rubric
4. **analyze_pattern_matches**: Finds pattern matches in code files

## ⚙️ Configuration

Pattern configurations are stored in YAML files in the `config/` directory. You can modify these to adjust detection patterns for different project types.

## 📚 Documentation

- [NEAR Rubric: Category Breakdown](docs/near_rubric.md): Friendly, human-readable overview of the rubric categories and scoring guidelines. 

## 🔄 Integration with Cursor

### Registering the MCP Server with Cursor

To use the NEAR Rubric MCP server natively in Cursor, register it in your `.cursor/mcp.json` file. This allows Cursor to automatically discover and connect to the server, making its tools available in the command palette and chat.

### Steps

1. **Clone the MCP server repository and install dependencies** as described above.
2. **Open (or create) `.cursor/mcp.json`** in your home directory or workspace root.
3. **Add the following entry** (adjust the `cwd` path as needed):

   ```json
   {
     "mcpServers": {
       "near-rubric-mcp": {
         "command": "python",
         "args": ["server.py"],
         "cwd": "C:/path/to/near-rubric-mcp"
       }
     }
   }
   ```

   - `command`: The executable to run (here, `python`)
   - `args`: Arguments to the command (here, just `server.py`)
   - `cwd`: The working directory where the server should be started

4. **Restart Cursor** (if needed) so it picks up the new server.
5. **Use Cursor's UI or chat** to invoke the NEAR Rubric MCP tools directly on your codebase.

> **Tip:** This is the preferred way to use MCP servers in Cursor, as it enables seamless integration and tool discovery.

## 🔍 Advanced Usage: Direct JSON-RPC Integration

For developers integrating the NEAR Rubric MCP outside of Cursor or similar AI environments, the server uses a simple JSON-RPC protocol. Example request:

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

## 📄 License

This project is part of the NEAR ecosystem tooling and is released under the MIT License. 