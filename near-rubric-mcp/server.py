from typing import Dict, List, Any, Optional
import json
import asyncio
import sys
import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent / "mcp_server.log")
    ]
)

logger = logging.getLogger("mcp_server")

# Import error handling
from evaluation.errors import ErrorResponse, ErrorCode

# Import category utilities
from categories import get_all_categories

class RubricMCPServer:
    """MCP Server for NEAR Protocol project evaluation."""
    
    def __init__(self):
        """Initialize the MCP server for NEAR Rubric evaluation."""
        self.server_info = {
            "name": "near-rubric-mcp",
            "version": "0.1.0",
            "description": "MCP Server for evaluating NEAR Protocol projects"
        }
        
        # Get all available categories
        self.categories = get_all_categories()
        
        logger.info(f"Initializing {self.server_info['name']} v{self.server_info['version']} with {len(self.categories)} categories")
        
    def _category_tools(self) -> List[Dict[str, Any]]:
        """Generate tool definitions for each category."""
        tools = []
        
        # Get evaluation framework tool
        tools.append({
            "name": "get_evaluation_framework",
            "description": "Get evaluation framework for a specific rubric category",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to evaluate (near_integration, onchain_quality, etc.)",
                        "enum": list(self.categories.keys())
                    },
                    "project_type": {
                        "type": "string",
                        "description": "The project type (rust, javascript, mixed)",
                        "optional": True,
                        "enum": ["rust", "javascript", "js", "typescript", "ts", "mixed"]
                    }
                },
                "required": ["category"]
            }
        })
        
        # Add analyze_code_context tool
        tools.append({
            "name": "analyze_code_context",
            "description": "Analyze provided code context against rubric",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to evaluate",
                        "enum": list(self.categories.keys())
                    },
                    "code_context": {
                        "type": "object",
                        "description": "Client-provided code snippets for analysis"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata about the code (file paths, dependencies)",
                        "optional": True
                    }
                },
                "required": ["category", "code_context"]
            }
        })
        
        # Add get_file_suggestions tool
        tools.append({
            "name": "get_file_suggestions",
            "description": "Get suggestions for which files to analyze",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The rubric category to get file suggestions for",
                        "enum": list(self.categories.keys())
                    },
                    "available_files": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of file paths in the repository"
                    }
                },
                "required": ["category", "available_files"]
            }
        })
        
        # Add analyze_pattern_matches tool
        tools.append({
            "name": "analyze_pattern_matches",
            "description": "Analyze code content for pattern matches and provide detailed analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to analyze patterns for",
                        "enum": list(self.categories.keys())
                    },
                    "code_content": {
                        "type": "object",
                        "description": "Client-provided code content for pattern matching"
                    },
                    "project_type": {
                        "type": "string",
                        "description": "The project type (rust, javascript, mixed)",
                        "optional": True,
                        "enum": ["rust", "javascript", "js", "typescript", "ts", "mixed"]
                    }
                },
                "required": ["category", "code_content"]
            }
        })
        
        return tools
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return the list of tools available from this MCP server."""
        tools = self._category_tools()
        
        # Add any additional tools that aren't category-specific
        
        logger.debug(f"Listed {len(tools)} available tools")
        return tools
        
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool call."""
        logger.info(f"Tool call: {name}")
        logger.debug(f"Tool arguments: {arguments}")
        
        # Get available tool names for error messages
        available_tools = [tool["name"] for tool in await self.list_tools()]
        
        try:
            # Validate required arguments for each tool
            if name == "get_evaluation_framework":
                if "category" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: category", 
                        field="category"
                    )
                
                from evaluation.orchestrator import get_evaluation_framework
                result = await get_evaluation_framework(
                    arguments["category"], 
                    arguments.get("project_type")
                )
                logger.info(f"get_evaluation_framework completed for category: {arguments['category']}")
                return result
                
            elif name == "analyze_code_context":
                # Validate required arguments
                if "category" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: category", 
                        field="category"
                    )
                if "code_context" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: code_context", 
                        field="code_context"
                    )
                
                from evaluation.orchestrator import analyze_code_context
                result = await analyze_code_context(
                    arguments["category"], 
                    arguments["code_context"],
                    arguments.get("metadata", {})
                )
                logger.info(f"analyze_code_context completed for category: {arguments['category']}")
                return result
                
            elif name == "get_file_suggestions":
                # Validate required arguments
                if "category" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: category", 
                        field="category"
                    )
                if "available_files" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: available_files", 
                        field="available_files"
                    )
                
                from evaluation.orchestrator import get_file_suggestions
                result = await get_file_suggestions(
                    arguments["category"],
                    arguments["available_files"]
                )
                logger.info(f"get_file_suggestions completed for category: {arguments['category']}")
                return result
                
            elif name == "analyze_pattern_matches":
                # Validate required arguments
                if "category" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: category", 
                        field="category"
                    )
                if "code_content" not in arguments:
                    return ErrorResponse.invalid_input(
                        "Missing required argument: code_content", 
                        field="code_content"
                    )
                
                from evaluation.pattern_library import get_patterns_for_category, find_pattern_matches_in_files
                
                category = arguments["category"]
                code_content = arguments["code_content"]
                project_type = arguments.get("project_type")
                
                # Get relevant patterns for this category
                pattern_data = await get_patterns_for_category(category, project_type)
                patterns = pattern_data.get("detection_patterns", [])
                
                # Find pattern matches in the provided code content
                matches = find_pattern_matches_in_files(code_content, patterns)
                
                # Ensure matches is a dictionary
                if matches is None:
                    matches = {}
                
                # Create a list of matched patterns more safely
                matched_patterns = []
                for pattern in patterns:
                    for file_path, file_matches in matches.items():
                        if file_matches and any(match.get("pattern") == pattern for match in file_matches):
                            matched_patterns.append(pattern)
                            break
                
                # Create structured response with pattern matches and explanations
                logger.info(f"analyze_pattern_matches completed for category: {category}")
                return {
                    "category": category,
                    "matches_by_file": matches,
                    "matched_patterns": matched_patterns,
                    "total_matches": sum(len(file_matches) for file_matches in matches.values()),
                    "explanation": f"Found pattern matches for {category} evaluation.",
                    "status": "success"
                }
            else:
                logger.warning(f"Unknown tool requested: {name}")
                return ErrorResponse.unknown_tool(name, available_tools)
        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
            return ErrorResponse.internal_error(e)

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming JSON-RPC message."""
        method = message.get("method")
        message_id = message.get("id")
        
        logger.info(f"Handling JSON-RPC method: {method}")
        
        if method == "list_tools":
            tools = await self.list_tools()
            return {"jsonrpc": "2.0", "result": tools, "id": message_id}
        elif method == "call_tool":
            params = message.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                error = ErrorResponse.invalid_input("Missing tool name", field="name")
                return {"jsonrpc": "2.0", "result": error, "id": message_id}
            
            result = await self.call_tool(tool_name, arguments)
            return {"jsonrpc": "2.0", "result": result, "id": message_id}
        else:
            logger.warning(f"Method not found: {method}")
            return {
                "jsonrpc": "2.0", 
                "error": {"code": -32601, "message": f"Method {method} not found"}, 
                "id": message_id
            }

    async def run_stdio(self):
        """Run the MCP server using stdio."""
        logger.info("Starting MCP server on stdio")
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    logger.info("Received EOF, shutting down")
                    break
                
                logger.debug(f"Received input: {line.strip()}")
                message = json.loads(line)
                response = await self.handle_message(message)
                
                logger.debug(f"Sending response: {json.dumps(response)}")
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {str(e)}")
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Internal error: {str(e)}", exc_info=True)
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
                    "id": None
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

def main():
    """Start the NEAR Rubric MCP server."""
    logger.info("Starting NEAR Rubric MCP server")
    server = RubricMCPServer()
    
    try:
        # Get an event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Create a new event loop if one doesn't exist
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run the server using stdio
    try:
        logger.info("Running server using stdio")
        loop.run_until_complete(server.run_stdio())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down")
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    finally:
        logger.info("Server shutdown complete")

if __name__ == "__main__":
    main() 