from typing import Dict, Any, Optional, List
import os
import json
import logging
from pathlib import Path
import glob

# Import error handling
from .errors import ErrorResponse, ErrorCode

# Set up logger
logger = logging.getLogger("prompt_generator")

# Define the base paths
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources" / "prompts"

# In-memory cache of loaded prompts
_prompt_cache = {}
_available_templates = None

def discover_prompt_templates() -> Dict[str, Path]:
    """
    Discover available prompt templates in the resources/prompts directory.
    
    Returns:
        Dict mapping category keys to template file paths
    """
    global _available_templates
    
    if _available_templates is not None:
        return _available_templates
        
    templates = {}
    
    if RESOURCES_DIR.exists():
        for template_path in RESOURCES_DIR.glob("*.txt"):
            category_key = template_path.stem
            templates[category_key] = template_path
            logger.debug(f"Found prompt template: {category_key} ({template_path})")
    
    logger.info(f"Discovered {len(templates)} prompt templates")
    _available_templates = templates
    return templates

def _load_prompt_template(category: str) -> str:
    """Load a prompt template from the resources directory."""
    # Check the cache first
    if category in _prompt_cache:
        logger.debug(f"Using cached prompt for category: {category}")
        return _prompt_cache[category]
    
    # Discover available templates
    templates = discover_prompt_templates()
    
    # Try to find a matching template (exact or suffix match)
    template_path = None
    for template_key, path in templates.items():
        if template_key == category or category.endswith(template_key):
            template_path = path
            logger.info(f"Found matching template: {template_key} for {category}")
            break
    
    # Try to load from file if found
    if template_path and template_path.exists():
        logger.info(f"Loading prompt template from file: {template_path}")
        try:
            with open(template_path, "r") as f:
                template = f.read()
                _prompt_cache[category] = template
                return template
        except Exception as e:
            logger.error(f"Error reading prompt template file: {str(e)}")
            # Continue to try other methods
    
    # If not found, load from the JSON file
    try:
        rubric_path = BASE_DIR.parent / "near_rubric_trimmed.json"
        logger.info(f"Attempting to load prompt from JSON: {rubric_path}")
        if rubric_path.exists():
            with open(rubric_path, "r") as f:
                rubric_data = json.load(f)
                
            # Find the matching category
            for item in rubric_data:
                category_name = item.get("category", "").lower().replace(" ", "_")
                if category_name.endswith(category.lower()):
                    enriched_prompt = item.get("enriched_prompt", "")
                    logger.info(f"Found matching category in JSON: {category_name}")
                    _prompt_cache[category] = enriched_prompt
                    return enriched_prompt
            
            logger.warning(f"No matching category found in JSON for: {category}")
    except Exception as e:
        logger.error(f"Error loading from JSON: {str(e)}", exc_info=True)
    
    # Fallback templates if no specific one is found
    logger.warning(f"Using fallback template for category: {category}")
    default_templates = {
        "near_integration": """
Role: You are an expert AI code auditor specializing in the NEAR Protocol ecosystem.

Task: Evaluate the provided code context for its integration with the NEAR Protocol based on the following criteria. 
Assign a score out of 20 and provide a detailed justification referencing specific code examples.

Category: NEAR Protocol Integration
Max Points: 20 pts

Scoring Guidelines:
* 16–20 pts: Deep integration with advanced features
* 10–15 pts: Moderate NEAR use, partial integrations
* 0–9 pts: Minimal to no direct integration

Look for:
- NEAR SDK usage (near-sdk-rs, near-sdk-js)
- Smart contract implementation
- Wallet integration
- NEP standards compliance
- Cross-contract calls

Input: Relevant code context (smart contracts, integration code)

Output Format:
1. Score: [Score]/20
2. Justification: [Detailed explanation with evidence]
""",
        "onchain_quality": """
Role: You are an expert AI code auditor analyzing blockchain interactions on the NEAR Protocol.

Task: Evaluate the quality and meaningfulness of the on-chain interactions in the code.
Assign a score out of 20 and provide a detailed justification.

Category: Onchain Quality
Max Points: 20 pts

Scoring Guidelines:
* 16–20 pts: Real, meaningful interactions with NEAR chain
* 10–15 pts: Occasional useful on-chain transactions
* 0–9 pts: Superficial or junk transactions

Look for:
- Core functionality implemented on-chain
- Complex contract calls
- Meaningful state changes
- Evidence of transaction flow

Output Format:
1. Score: [Score]/20
2. Justification: [Detailed explanation with evidence]
"""
    }
    
    template = default_templates.get(category)
    if template:
        _prompt_cache[category] = template
        return template
    else:
        logger.error(f"No template available for category: {category}")
        return f"No prompt template available for category: {category}."

async def generate_prompt(category: str, project_type: Optional[str] = None) -> str:
    """
    Generate an evaluation prompt for the given category and project type.
    
    Args:
        category: The category to generate a prompt for
        project_type: Optional project type (rust, javascript, mixed)
        
    Returns:
        Evaluation prompt string
    """
    logger.info(f"Generating prompt for category: {category}, project_type: {project_type}")
    
    # Load the basic template
    template = _load_prompt_template(category)
    
    # Add project type specific guidance if needed
    if project_type:
        logger.debug(f"Adding {project_type}-specific guidance to prompt")
        if project_type.lower() == "rust":
            template += "\n\nAdditional guidance for Rust projects:\n"
            template += "- Check for #[near_bindgen] attribute on contract structs\n"
            template += "- Look for near-sdk-rs imports and usage\n"
            template += "- Examine initialization and state management patterns\n"
        elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
            template += "\n\nAdditional guidance for JavaScript/TypeScript projects:\n"
            template += "- Check for near-api-js or near-sdk-js imports\n"
            template += "- Look for wallet connection implementations\n"
            template += "- Examine contract call patterns and transaction signing\n"
    
    return template

def get_missing_templates() -> List[str]:
    """
    Get a list of categories without prompt templates.
    
    Returns:
        List of category names missing templates
    """
    # Import here to avoid circular import
    from categories import get_all_categories
    
    categories = get_all_categories()
    templates = discover_prompt_templates()
    
    missing = []
    for category_key, category in categories.items():
        found = False
        for template_key in templates:
            if category_key == template_key or category_key.endswith(template_key):
                found = True
                break
        if not found:
            missing.append(category_key)
    
    return missing 