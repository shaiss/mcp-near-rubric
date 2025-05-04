from typing import Dict, List, Any, Optional
import os
import yaml
import json
from pathlib import Path

# Import other evaluation components
from . import prompt_generator
from . import pattern_library
from . import file_matcher
from .errors import ErrorResponse, ErrorCode

# Define the base path for configuration files
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
RESOURCES_DIR = BASE_DIR / "resources"

def load_rubric_config() -> Dict[str, Any]:
    """Load the rubric configuration from YAML."""
    config_path = CONFIG_DIR / "rubric.yaml"
    if not config_path.exists():
        # Return a default configuration if file doesn't exist yet
        return {
            "categories": {
                "near_integration": {
                    "max_points": 20,
                    "evaluation_type": "hybrid",
                    "key_indicators": [
                        "NEAR SDK presence",
                        "Smart contract implementation",
                        "Wallet integration",
                        "NEP standards compliance"
                    ],
                    "file_patterns": [
                        "**/*contract*.rs",
                        "**/Cargo.toml",
                        "**/*near*.{js,ts}"
                    ],
                    "scoring_tiers": {
                        "advanced": {
                            "range": [16, 20],
                            "criteria": "Deep integration with advanced features"
                        },
                        "moderate": {
                            "range": [10, 15],
                            "criteria": "Basic integration with standard features"
                        },
                        "minimal": {
                            "range": [0, 9],
                            "criteria": "Limited or no NEAR integration"
                        }
                    }
                }
            }
        }
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

async def get_evaluation_framework(category: str, project_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the evaluation framework for a specific rubric category.
    
    Args:
        category: The category to evaluate (e.g., near_integration, onchain_quality)
        project_type: Optional project type (rust, javascript, mixed)
        
    Returns:
        Dict containing the evaluation framework
    """
    rubric_config = load_rubric_config()
    
    # Normalize category name (replace spaces, convert to lowercase)
    norm_category = category.lower().replace(" ", "_")
    if norm_category.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
        norm_category = norm_category[2:].strip()
    
    # Find the category in the configuration
    category_config = None
    category_key = None
    available_categories = list(rubric_config.get("categories", {}).keys())
    
    for cat_key, cat_data in rubric_config.get("categories", {}).items():
        if cat_key == norm_category or cat_key.endswith(norm_category):
            category_config = cat_data
            category_key = cat_key
            break
    
    if not category_config:
        # Use the new error response helper
        return ErrorResponse.category_not_found(category, available_categories)
    
    # Get relevant patterns for this category
    patterns = await pattern_library.get_patterns_for_category(category_key, project_type)
    
    # Generate evaluation prompt
    evaluation_prompt = await prompt_generator.generate_prompt(category_key, project_type)
    
    # Construct the evaluation framework
    max_points = category_config.get("max_points", 20)
    
    framework = {
        "category": category,
        "max_points": max_points,
        "evaluation_prompt": evaluation_prompt,
        "scoring_guide": {
            f"{tier['range'][0]}-{tier['range'][1]}": tier["criteria"]
            for tier_name, tier in category_config.get("scoring_tiers", {}).items()
        },
        "suggested_files": category_config.get("file_patterns", []),
        "quick_check_patterns": patterns.get("detection_patterns", [])
    }
    
    return framework

async def analyze_code_context(category: str, code_context: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze provided code context against a specific rubric category.
    
    Args:
        category: The category to evaluate
        code_context: Client-provided code snippets for analysis
        metadata: Optional metadata about the code
    
    Returns:
        Dict containing analysis framework and guidance
    """
    framework = await get_evaluation_framework(category)
    
    # Add specific analysis guidance
    framework["analysis_guidance"] = {
        "key_indicators": framework.get("quick_check_patterns", []),
        "contextual_prompts": [
            "Analyze how this code integrates with NEAR Protocol",
            "Identify the specific NEAR features being used",
            "Assess the sophistication of the implementation"
        ]
    }
    
    return framework

async def get_file_suggestions(category: str, available_files: List[str]) -> Dict[str, Any]:
    """
    Get suggestions for which files to analyze for a rubric category.
    
    Args:
        category: The rubric category
        available_files: List of file paths in the repository
    
    Returns:
        Dict containing suggested files and patterns
    """
    framework = await get_evaluation_framework(category)
    
    # Extract file patterns from the framework
    patterns = framework.get("suggested_files", [])
    
    # Filter the available files based on the patterns using the file_matcher module
    matched_files = file_matcher.filter_files_by_patterns(available_files, patterns)
    
    # Handle complex patterns with multiple extensions
    complex_matches = []
    for pattern in patterns:
        if "{" in pattern and "}" in pattern:
            matches = file_matcher.resolve_complex_glob_pattern(pattern, available_files)
            complex_matches.extend(matches)
    
    # Combine all matches and remove duplicates
    all_matched_files = list(set(matched_files + complex_matches))
    
    # Sort the matched files for consistent output
    all_matched_files.sort()
    
    # Group matched files by pattern for better explanations
    pattern_matches = {}
    for pattern in patterns:
        pattern_matches[pattern] = []
        for file_path in available_files:
            if file_matcher.match_file_with_glob(file_path, pattern):
                pattern_matches[pattern].append(file_path)
    
    return {
        "category": category,
        "suggested_files": all_matched_files,
        "patterns": patterns,
        "pattern_matches": pattern_matches,
        "explanation": "These files are likely to contain relevant code for this evaluation category."
    } 