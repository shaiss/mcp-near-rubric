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

## Using NEAR Rubric MCP in Cursor IDE

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
   git clone https://github.com/HaidarJbeily7/YieldGuard.git
   ```

### Running the MCP Server

From the `near-rubric-mcp` directory, start the server:
```bash
python server.py
```

### Auditing a NEAR Project in Cursor

1. **Open Cursor IDE** and ensure both the MCP server and your target NEAR project are in your workspace.
2. **Start the MCP server** in the integrated terminal as shown above.
3. **Run an Audit**:
   - You can use the provided `test_client.py` or send JSON-RPC requests directly (see below).
   - Example: To get file suggestions for the "near_integration" category:
     ```json
     {
       "jsonrpc": "2.0",
       "method": "call_tool",
       "params": {
         "name": "get_file_suggestions",
         "arguments": {
           "category": "near_integration",
           "available_files": ["YieldGuard/src/lib.rs", "YieldGuard/README.md"]
         }
       },
       "id": 1
     }
     ```
   - Use the other tools (`get_evaluation_framework`, `analyze_code_context`, etc.) as needed.

4. **View Results**: The server will return structured results with scores and justifications for each rubric category.

### Example Workflow

1. Clone both the MCP server and your NEAR project into your workspace.
2. Install dependencies.
3. Start the MCP server.
4. Use the provided tools to audit your project.
5. Review the output in the Cursor terminal or via the integrated chat if available.

## Registering the MCP Server with Cursor

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