"""
Automatic category discovery and registration utilities.
This module provides functions to automatically discover and register category classes.
"""

import os
import inspect
import logging
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Tuple

from categories.base import BaseCategory

logger = logging.getLogger("category_discovery")

def discover_category_classes() -> Dict[str, Type[BaseCategory]]:
    """
    Automatically discover all BaseCategory subclasses in the categories directory.
    
    Returns:
        Dict mapping category keys to category classes
    """
    logger.info("Discovering category classes...")
    categories = {}
    
    # Get the current directory (categories/)
    categories_dir = Path(__file__).parent
    
    # Find all Python files in the directory
    for file_path in categories_dir.glob("*.py"):
        # Skip __init__.py, this file, and other special files
        if file_path.name in ["__init__.py", "__pycache__", "category_discovery.py", "base.py"]:
            continue
            
        logger.debug(f"Checking file: {file_path}")
        
        try:
            # Load the module
            module_name = file_path.stem
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                logger.warning(f"Could not load spec for {file_path}")
                continue
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find all classes in the module that are subclasses of BaseCategory
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, BaseCategory) and 
                    obj != BaseCategory):
                    
                    # Create instance to get the name
                    instance = obj()
                    category_key = instance.name.lower().replace(" ", "_")
                    
                    # Store with normalized name
                    categories[category_key] = obj
                    logger.info(f"Discovered category: {category_key} ({name})")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}", exc_info=True)
    
    logger.info(f"Discovered {len(categories)} categories")
    return categories

def discover_prompt_templates() -> Dict[str, str]:
    """
    Discover all prompt templates in the resources/prompts directory.
    
    Returns:
        Dict mapping category keys to template file paths
    """
    logger.info("Discovering prompt templates...")
    templates = {}
    
    # Define mapping for template files to standardized category keys
    template_category_mapping = {
        "code_quality": "code_quality_&_documentation",
        "ecosystem_fit": "grant_impact_&_ecosystem_fit",
        "near_integration": "near_protocol_integration",
        "team_activity": "team_activity_&_project_maturity",
        "technical_innovation": "technical_innovation/uniqueness",
        "offchain_quality": "offchain_quality",
        "onchain_quality": "onchain_quality"
    }
    
    # Get the prompts directory
    base_dir = Path(__file__).parent.parent
    prompts_dir = base_dir / "resources" / "prompts"
    
    if not prompts_dir.exists():
        logger.warning(f"Prompts directory not found: {prompts_dir}")
        return templates
    
    # Find all .txt files in the directory
    for file_path in prompts_dir.glob("*.txt"):
        template_key = file_path.stem
        # Use the mapping if available to get the standardized category key
        category_key = template_category_mapping.get(template_key, template_key)
        templates[template_key] = str(file_path)
        logger.debug(f"Found template for {category_key}: {file_path}")
    
    logger.info(f"Discovered {len(templates)} prompt templates")
    return templates

def validate_category_config(
    discovered_categories: Dict[str, Type[BaseCategory]], 
    prompt_templates: Dict[str, str]
) -> Tuple[List[str], List[str], List[str]]:
    """
    Validate that all discovered categories have prompt templates and configuration.
    
    Args:
        discovered_categories: Dict of discovered category classes
        prompt_templates: Dict of discovered prompt templates
        
    Returns:
        Tuple containing:
        - List of categories missing prompt templates
        - List of orphaned prompt templates (no matching category)
        - List of warnings about the configuration
    """
    logger.info("Validating category configuration...")
    missing_templates = []
    orphaned_templates = []
    warnings = []
    
    # Create mapping dictionaries for easier lookup
    category_template_mapping = {
        "code_quality_&_documentation": "code_quality",
        "grant_impact_&_ecosystem_fit": "ecosystem_fit",
        "near_protocol_integration": "near_integration",
        "team_activity_&_project_maturity": "team_activity",
        "technical_innovation/uniqueness": "technical_innovation",
        "offchain_quality": "offchain_quality",
        "onchain_quality": "onchain_quality"
    }
    
    # Check for missing templates
    for category_key in discovered_categories:
        # Normalize the key for comparison
        norm_key = category_key.lower().replace(" ", "_")
        
        # Use the mapping if available
        template_key = category_template_mapping.get(norm_key, norm_key)
        
        if template_key not in prompt_templates:
            missing_templates.append(category_key)
            warnings.append(f"Category '{category_key}' is missing a prompt template")
    
    # Check for orphaned templates
    for template_key in prompt_templates:
        # Try to find a matching category using the reverse mapping
        found = False
        for cat_key, temp_key in category_template_mapping.items():
            if temp_key == template_key:
                found = True
                break
        
        # If not found using the mapping, try direct matching
        if not found:
            for category_key in discovered_categories:
                norm_cat_key = category_key.lower().replace(" ", "_")
                if template_key == norm_cat_key or norm_cat_key.endswith(template_key):
                    found = True
                    break
        
        if not found:
            orphaned_templates.append(template_key)
            warnings.append(f"Prompt template '{template_key}' has no matching category")
    
    logger.info(f"Validation complete. {len(missing_templates)} missing templates, "
                f"{len(orphaned_templates)} orphaned templates")
    
    return missing_templates, orphaned_templates, warnings

def synchronize_categories() -> Dict[str, Any]:
    """
    Discover categories, prompt templates, validate, and prepare a report.
    
    Returns:
        Dict containing the synchronization report
    """
    # Use the previously discovered categories instead of discovering again
    from categories import CATEGORIES
    categories = {key: val.__class__ for key, val in CATEGORIES.items()}
    
    # Discover templates
    templates = discover_prompt_templates()
    
    # Validate configuration
    missing_templates, orphaned_templates, warnings = validate_category_config(
        categories, templates
    )
    
    # Prepare report
    report = {
        "discovered_categories": list(categories.keys()),
        "discovered_templates": list(templates.keys()),
        "missing_templates": missing_templates,
        "orphaned_templates": orphaned_templates,
        "warnings": warnings,
        "status": "success" if not warnings else "warnings"
    }
    
    return report 