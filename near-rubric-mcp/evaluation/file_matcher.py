"""
File matching utilities for pattern-based file selection.
This module provides utilities for matching files against glob and regex patterns.
"""

from typing import List, Pattern, Dict, Any, Optional
import re
import fnmatch
from pathlib import Path
import logging

# Import error handling
from .errors import ErrorResponse, ErrorCode

# Set up logger
logger = logging.getLogger("file_matcher")

def compile_glob_pattern(pattern: str) -> Pattern:
    """
    Convert a glob pattern to a regex pattern.
    
    Args:
        pattern: A glob pattern (e.g., "**/*.js", "**/src/*.rs")
        
    Returns:
        A compiled regex pattern
    """
    # Handle '**/' which means "this directory and all subdirectories recursively"
    if "**/" in pattern:
        pattern = pattern.replace("**/", "(.*/)?")
    
    # Convert glob-style pattern to regex
    regex_pattern = fnmatch.translate(pattern)
    
    # Fix the path separators for Windows vs Unix
    regex_pattern = regex_pattern.replace("\\\\", "/").replace("/", r"[/\\]")
    
    return re.compile(regex_pattern)


def compile_extension_pattern(extension: str) -> Pattern:
    """
    Create a regex pattern for a file extension.
    
    Args:
        extension: File extension without dot (e.g., "js", "rs")
        
    Returns:
        A compiled regex pattern for the extension
    """
    return re.compile(r".*\." + re.escape(extension) + r"$")


def match_file_with_glob(file_path: str, glob_pattern: str) -> bool:
    """
    Check if a file path matches a glob pattern.
    
    Args:
        file_path: The file path to check
        glob_pattern: A glob pattern string
        
    Returns:
        True if the file matches the pattern, False otherwise
    """
    try:
        # Handle ** patterns (recursive directory matching)
        if "**" in glob_pattern:
            parts = glob_pattern.split("**")
            if len(parts) == 2:
                # Simple case like "**/*.py"
                prefix, suffix = parts
                if prefix and not file_path.startswith(prefix.rstrip("/\\")):
                    return False
                if suffix and not file_path.endswith(suffix.lstrip("/\\")):
                    return False
                return fnmatch.fnmatch(file_path, glob_pattern)
            else:
                # Complex case with multiple ** parts
                return fnmatch.fnmatch(file_path, glob_pattern)
        # Standard glob matching
        return fnmatch.fnmatch(file_path, glob_pattern)
    except Exception as e:
        logger.error(f"Error in glob matching: {str(e)}")
        return False


def filter_files_by_patterns(available_files: List[str], patterns: List[str]) -> List[str]:
    """
    Filter a list of files based on glob patterns.
    
    Args:
        available_files: List of file paths to filter
        patterns: List of glob patterns to match against
        
    Returns:
        List of matched file paths
    """
    logger.debug(f"Filtering {len(available_files)} files against {len(patterns)} patterns")
    matched_files = []
    
    # Validate inputs
    if not isinstance(available_files, list):
        logger.warning(f"Expected list for available_files, got {type(available_files)}")
        return []
        
    if not isinstance(patterns, list):
        logger.warning(f"Expected list for patterns, got {type(patterns)}")
        return []
    
    # Match each file against each pattern
    for file_path in available_files:
        if not isinstance(file_path, str):
            logger.warning(f"Skipping non-string file path: {file_path}")
            continue
            
        for pattern in patterns:
            if not isinstance(pattern, str):
                logger.warning(f"Skipping non-string pattern: {pattern}")
                continue
                
            try:
                if match_file_with_glob(file_path, pattern):
                    matched_files.append(file_path)
                    break  # Once a file matches any pattern, we can stop checking it
            except Exception as e:
                logger.error(f"Error matching file {file_path} with pattern {pattern}: {str(e)}")
    
    logger.info(f"Matched {len(matched_files)} files using glob patterns")
    return matched_files


def match_file_with_regex(file_path: str, regex_pattern: str) -> bool:
    """
    Check if a file path matches a regex pattern.
    
    Args:
        file_path: The file path to check
        regex_pattern: A regex pattern string
        
    Returns:
        True if the file matches the pattern, False otherwise
    """
    try:
        pattern = re.compile(regex_pattern)
        return bool(pattern.search(file_path))
    except re.error as e:
        logger.error(f"Invalid regex pattern '{regex_pattern}': {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in regex matching: {str(e)}")
        return False


def find_pattern_matches_in_file(file_content: str, patterns: List[str]) -> List[Dict[str, Any]]:
    """
    Find regex pattern matches in file content.
    
    Args:
        file_content: The content of the file to search
        patterns: List of regex patterns to search for
        
    Returns:
        List of matches with pattern and line numbers
    """
    matches = []
    
    # Validate inputs
    if not isinstance(file_content, str):
        logger.warning(f"Expected string for file_content, got {type(file_content)}")
        return []
        
    if not isinstance(patterns, list):
        logger.warning(f"Expected list for patterns, got {type(patterns)}")
        return []
    
    lines = file_content.split("\n")
    
    for pattern_str in patterns:
        if not isinstance(pattern_str, str):
            logger.warning(f"Skipping non-string pattern: {pattern_str}")
            continue
            
        try:
            pattern = re.compile(pattern_str)
            
            # Search each line
            for i, line in enumerate(lines):
                if pattern.search(line):
                    matches.append({
                        "pattern": pattern_str,
                        "line_number": i + 1,  # 1-based line numbering
                        "line_content": line.strip(),
                        "match": True
                    })
        except re.error as e:
            logger.error(f"Invalid regex pattern '{pattern_str}': {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error matching pattern '{pattern_str}': {str(e)}")
            continue
    
    logger.debug(f"Found {len(matches)} pattern matches")
    return matches


def resolve_complex_glob_pattern(pattern: str, available_files: List[str]) -> List[str]:
    """
    Resolve a complex glob pattern with multiple extensions or nested paths.
    
    Args:
        pattern: A glob pattern that may contain complex expressions
        available_files: List of available files to match against
        
    Returns:
        List of file paths that match the pattern
    """
    logger.debug(f"Resolving complex glob pattern: {pattern}")
    
    # Validate inputs
    if not isinstance(pattern, str):
        logger.warning(f"Expected string for pattern, got {type(pattern)}")
        return []
        
    if not isinstance(available_files, list):
        logger.warning(f"Expected list for available_files, got {type(available_files)}")
        return []
    
    # Handle multiple extensions pattern like "**/*.{js,ts}"
    if "{" in pattern and "}" in pattern:
        extension_part = pattern[pattern.find("{"):pattern.find("}")+1]
        extensions = extension_part.strip("{}").split(",")
        
        base_pattern = pattern.replace(extension_part, "{}")
        
        matched_files = []
        for ext in extensions:
            specific_pattern = base_pattern.format(ext)
            logger.debug(f"Checking specific pattern: {specific_pattern}")
            
            try:
                matches = [f for f in available_files if match_file_with_glob(f, specific_pattern)]
                matched_files.extend(matches)
                logger.debug(f"Found {len(matches)} matches for pattern: {specific_pattern}")
            except Exception as e:
                logger.error(f"Error matching with pattern {specific_pattern}: {str(e)}")
        
        return matched_files
    
    # Standard pattern matching
    logger.debug("Using standard pattern matching")
    return [f for f in available_files if match_file_with_glob(f, pattern)] 