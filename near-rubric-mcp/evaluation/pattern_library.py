from typing import Dict, List, Any, Optional
import yaml
import logging
from pathlib import Path
from . import file_matcher
from .errors import ErrorResponse, ErrorCode

# Set up logger
logger = logging.getLogger("pattern_library")

# Define the base path for configuration files
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"

# Default patterns to use if no configuration file exists
DEFAULT_PATTERNS = {
    "near_integration": {
        "rust": [
            "near-sdk",
            "near_sdk",
            "#\\[near_bindgen\\]",
            "@NearContract",
            "Promise",
            "AccountId",
            "env::predecessor_account_id"
        ],
        "javascript": [
            "near-api-js",
            "near-sdk-js",
            "connect\\s*\\(",
            "WalletConnection",
            "keyStores",
            "Contract\\s*\\(",
            "createTransaction"
        ],
        "common": [
            "near",
            "NEAR",
            "contract",
            "wallet"
        ]
    },
    "onchain_quality": {
        "rust": [
            "pub\\s+fn",
            "#\\[payable\\]",
            "self\\..*\\s*=",
            "env::storage_",
            "borsh::",
            "assert!",
            "require!"
        ],
        "javascript": [
            "view\\s*\\(",
            "change\\s*\\(",
            "call\\s*\\(",
            "transaction",
            "sendTransaction",
            "FunctionCall",
            "setState"
        ],
        "common": [
            "storage",
            "state",
            "transaction"
        ]
    },
    "code_quality": {
        "rust": [
            "#\\[test\\]",
            "assert_eq!",
            "mod\\s+tests",
            "pub\\s+struct",
            "impl",
            "Result<"
        ],
        "javascript": [
            "test\\s*\\(",
            "describe\\s*\\(",
            "it\\s*\\(",
            "expect\\s*\\(",
            "class\\s+\\w+",
            "function\\s+\\w+"
        ],
        "common": [
            "test",
            "README",
            "documentation",
            "todo:",
            "TODO:",
            "FIXME:"
        ]
    },
    "technical_innovation": {
        "rust": [
            "unsafe\\s*\\{",
            "generics",
            "trait\\s+\\w+",
            "async\\s+fn",
            "macro_rules!"
        ],
        "javascript": [
            "async\\s+function",
            "Promise\\.all",
            "new\\s+Proxy",
            "Object\\.defineProperty",
            "reduce\\s*\\("
        ],
        "common": [
            "algorithm",
            "custom",
            "unique",
            "novel",
            "architecture"
        ]
    }
}

def load_patterns_config() -> Dict[str, Any]:
    """Load the patterns configuration from YAML."""
    config_path = CONFIG_DIR / "patterns.yaml"
    logger.debug(f"Attempting to load patterns config from: {config_path}")
    
    if not config_path.exists():
        logger.warning(f"Patterns config file not found at {config_path}, using defaults")
        return {"patterns": DEFAULT_PATTERNS}
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            logger.info(f"Loaded patterns config with {len(config.get('patterns', {}))} categories")
            return config
    except Exception as e:
        logger.error(f"Error loading patterns config: {str(e)}", exc_info=True)
        return {"patterns": DEFAULT_PATTERNS}

def normalize_category_name(category: str) -> str:
    """
    Normalize a category name for lookup.
    
    Args:
        category: The category name to normalize
        
    Returns:
        Normalized category name
    """
    if not isinstance(category, str):
        logger.warning(f"Non-string category provided: {category}")
        return ""
        
    norm_category = category.lower().replace(" ", "_")
    if norm_category.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
        norm_category = norm_category[2:].strip()
    
    logger.debug(f"Normalized category '{category}' to '{norm_category}'")
    return norm_category

async def get_patterns_for_category(category: str, project_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detection patterns for a specific category and project type.
    
    Args:
        category: The category to get patterns for
        project_type: Optional project type (rust, javascript, mixed)
        
    Returns:
        Dict containing patterns for the category
    """
    logger.info(f"Getting patterns for category: {category}, project_type: {project_type}")
    
    # Input validation
    if not isinstance(category, str):
        logger.error(f"Invalid category type: {type(category)}")
        return ErrorResponse.invalid_input(
            "Category must be a string", 
            field="category"
        )
    
    patterns_config = load_patterns_config()
    
    # Normalize category name
    norm_category = normalize_category_name(category)
    if not norm_category:
        logger.warning(f"Empty normalized category for: {category}")
        return {
            "category": category,
            "detection_patterns": [],
            "explanation": "Invalid category format."
        }
    
    # Get patterns for the category
    all_patterns = patterns_config.get("patterns", DEFAULT_PATTERNS)
    category_patterns = all_patterns.get(norm_category, {})
    
    # If no category found, try to match by suffix
    if not category_patterns:
        logger.debug(f"No exact category match for {norm_category}, trying suffix matching")
        for cat_key, cat_patterns in all_patterns.items():
            if cat_key.endswith(norm_category):
                logger.info(f"Found matching category by suffix: {cat_key}")
                category_patterns = cat_patterns
                break
    
    # If still no match, return empty patterns
    if not category_patterns:
        logger.warning(f"No matching patterns found for category: {category}")
        available_categories = list(all_patterns.keys())
        return {
            "category": category,
            "detection_patterns": [],
            "explanation": "No specific patterns available for this category.",
            "available_categories": available_categories
        }
    
    # Select appropriate patterns based on project type
    selected_patterns = []
    
    # Always include common patterns
    if "common" in category_patterns:
        common_patterns = category_patterns["common"]
        logger.debug(f"Adding {len(common_patterns)} common patterns")
        selected_patterns.extend(common_patterns)
    
    # Add language-specific patterns if project type specified
    if project_type:
        if project_type.lower() == "rust" and "rust" in category_patterns:
            rust_patterns = category_patterns["rust"]
            logger.debug(f"Adding {len(rust_patterns)} Rust patterns")
            selected_patterns.extend(rust_patterns)
        elif project_type.lower() in ["javascript", "js", "typescript", "ts"] and "javascript" in category_patterns:
            js_patterns = category_patterns["javascript"]
            logger.debug(f"Adding {len(js_patterns)} JavaScript patterns")
            selected_patterns.extend(js_patterns)
        elif project_type.lower() == "mixed":
            # For mixed, include all language patterns
            logger.debug("Using mixed project type, adding all language patterns")
            if "rust" in category_patterns:
                selected_patterns.extend(category_patterns["rust"])
            if "javascript" in category_patterns:
                selected_patterns.extend(category_patterns["javascript"])
    else:
        # If no project type, include all patterns
        logger.debug("No project type specified, adding all language patterns")
        for lang, lang_patterns in category_patterns.items():
            if lang != "common":  # Common patterns already added
                selected_patterns.extend(lang_patterns)
    
    # Remove duplicates
    selected_patterns = list(set(selected_patterns))
    logger.info(f"Selected {len(selected_patterns)} patterns for category: {category}")
    
    # Return the patterns
    return {
        "category": category,
        "detection_patterns": selected_patterns,
        "explanation": f"Found {len(selected_patterns)} relevant patterns for {category} evaluation."
    }

def find_pattern_matches_in_files(files_content: Dict[str, str], patterns: List[str]) -> Dict[str, List[Dict]]:
    """
    Find pattern matches in multiple files content.
    
    Args:
        files_content: Dict mapping file paths to file content
        patterns: List of regex patterns to search for
        
    Returns:
        Dict mapping file paths to lists of pattern matches
    """
    logger.info(f"Searching for patterns in {len(files_content)} files")
    
    if not isinstance(files_content, dict):
        logger.error(f"Invalid files_content type: {type(files_content)}")
        return {}
        
    if not isinstance(patterns, list):
        logger.error(f"Invalid patterns type: {type(patterns)}")
        return {}
    
    # Find matches in each file
    matches_by_file = {}
    for file_path, content in files_content.items():
        logger.debug(f"Searching for patterns in file: {file_path}")
        
        try:
            file_matches = file_matcher.find_pattern_matches_in_file(content, patterns)
            if file_matches:
                matches_by_file[file_path] = file_matches
                logger.debug(f"Found {len(file_matches)} matches in {file_path}")
        except Exception as e:
            logger.error(f"Error searching file {file_path}: {str(e)}", exc_info=True)
    
    logger.info(f"Found matches in {len(matches_by_file)} files")
    return matches_by_file 