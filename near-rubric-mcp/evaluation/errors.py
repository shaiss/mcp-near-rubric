"""
Standardized error handling for the NEAR Rubric MCP Server.
This module provides error codes, structured error responses, and utilities for consistent error handling.
"""

from typing import Dict, Any, Optional, List, Union
from enum import Enum


class ErrorCode(str, Enum):
    """Standardized error codes for the MCP server."""
    # General errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    
    # Category-related errors
    CATEGORY_NOT_FOUND = "CATEGORY_NOT_FOUND"
    INVALID_CATEGORY = "INVALID_CATEGORY"
    
    # Tool-related errors
    UNKNOWN_TOOL = "UNKNOWN_TOOL"
    TOOL_EXECUTION_ERROR = "TOOL_EXECUTION_ERROR"
    
    # File-related errors
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_ACCESS_ERROR = "FILE_ACCESS_ERROR"
    
    # Config-related errors
    CONFIG_ERROR = "CONFIG_ERROR"
    MISSING_CONFIG = "MISSING_CONFIG"
    
    # Pattern-related errors
    PATTERN_ERROR = "PATTERN_ERROR"
    INVALID_PATTERN = "INVALID_PATTERN"


class ErrorResponse:
    """Standard structure for error responses."""
    
    @staticmethod
    def create(
        message: str, 
        error_code: Union[ErrorCode, str], 
        suggestion: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            message: Human-readable error message
            error_code: Error code for programmatic handling
            suggestion: Optional suggestion for fixing the error
            details: Optional additional details about the error
            
        Returns:
            Dict containing the structured error response
        """
        response = {
            "error": message,
            "error_code": error_code if isinstance(error_code, str) else error_code.value,
            "status": "failed"
        }
        
        if suggestion:
            response["suggestion"] = suggestion
            
        if details:
            response["details"] = details
            
        return response
    
    @staticmethod
    def category_not_found(category: str, available_categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a category not found error response.
        
        Args:
            category: The category that was not found
            available_categories: Optional list of available categories
            
        Returns:
            Dict containing the structured error response
        """
        suggestion = "Please check the spelling or use one of the supported categories."
        if available_categories:
            suggestion += f" Available categories: {', '.join(available_categories)}"
            
        return ErrorResponse.create(
            message=f"Category '{category}' is not supported.",
            error_code=ErrorCode.CATEGORY_NOT_FOUND,
            suggestion=suggestion,
            details={"requested_category": category, "available_categories": available_categories}
        )
    
    @staticmethod
    def unknown_tool(tool_name: str, available_tools: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create an unknown tool error response.
        
        Args:
            tool_name: The tool that was not found
            available_tools: Optional list of available tools
            
        Returns:
            Dict containing the structured error response
        """
        suggestion = "Please check the spelling or use one of the supported tools."
        if available_tools:
            suggestion += f" Available tools: {', '.join(available_tools)}"
            
        return ErrorResponse.create(
            message=f"Tool '{tool_name}' is not supported.",
            error_code=ErrorCode.UNKNOWN_TOOL,
            suggestion=suggestion,
            details={"requested_tool": tool_name, "available_tools": available_tools}
        )
    
    @staticmethod
    def invalid_input(message: str, field: Optional[str] = None) -> Dict[str, Any]:
        """
        Create an invalid input error response.
        
        Args:
            message: Description of the input error
            field: Optional field name that has the error
            
        Returns:
            Dict containing the structured error response
        """
        details = {"field": field} if field else None
        
        return ErrorResponse.create(
            message=message,
            error_code=ErrorCode.INVALID_INPUT,
            suggestion="Please check the input values and try again.",
            details=details
        )
    
    @staticmethod
    def internal_error(exception: Exception) -> Dict[str, Any]:
        """
        Create an internal error response.
        
        Args:
            exception: The exception that caused the error
            
        Returns:
            Dict containing the structured error response
        """
        return ErrorResponse.create(
            message=f"An internal error occurred: {str(exception)}",
            error_code=ErrorCode.INTERNAL_ERROR,
            suggestion="Please report this issue to the maintainers.",
            details={"exception_type": type(exception).__name__}
        ) 