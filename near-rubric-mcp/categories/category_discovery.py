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

from .base import BaseCategory

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
    
    # Get the prompts directory
    base_dir = Path(__file__).parent.parent
    prompts_dir = base_dir / "resources" / "prompts"
    
    if not prompts_dir.exists():
        logger.warning(f"Prompts directory not found: {prompts_dir}")
        return templates
    
    # Find all .txt files in the directory
    for file_path in prompts_dir.glob("*.txt"):
        category_key = file_path.stem
        templates[category_key] = str(file_path)
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
    
    # Check for missing templates
    for category_key in discovered_categories:
        # Normalize the key for comparison
        norm_key = category_key.lower().replace(" ", "_")
        if norm_key not in prompt_templates:
            missing_templates.append(category_key)
            warnings.append(f"Category '{category_key}' is missing a prompt template")
    
    # Check for orphaned templates
    for template_key in prompt_templates:
        # Try to find a matching category (exact or suffix)
        found = False
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
    # Discover categories and templates
    categories = discover_category_classes()
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