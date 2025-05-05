"""
Categories package for NEAR Rubric MCP
"""

# NEAR Rubric MCP Categories Package
"""Category implementations for NEAR Rubric evaluation."""

import logging
from typing import Dict, Type, Any

from categories.base import BaseCategory
from categories.near_integration import NEARIntegrationCategory
from categories.onchain_quality import OnchainQualityCategory
from categories.offchain_quality import OffchainQualityCategory
from categories.code_quality import CodeQualityCategory
from categories.technical_innovation import TechnicalInnovationCategory
from categories.team_activity import TeamActivityCategory
from categories.ecosystem_fit import EcosystemFitCategory

# Set up logger
logger = logging.getLogger("categories")

# Dictionary to store discovered categories
CATEGORIES = {}

# Flag to track if discovery has already been run
_discovery_completed = False

def _discover_and_register_categories():
    global CATEGORIES, _discovery_completed
    
    # Skip if discovery already completed
    if _discovery_completed:
        logger.info("Category discovery already completed, using cached results")
        return CATEGORIES
    
    # Import category discovery utilities
    try:
        from categories.category_discovery import discover_category_classes, synchronize_categories
        
        # Use auto-discovery for categories
        _discovered_categories = discover_category_classes()
        logger.info(f"DEBUG: Discovered category keys: {list(_discovered_categories.keys())}")
        
        # Just use the discovered categories
        CATEGORIES = _discovered_categories
        
        # Run synchronization check on startup
        _sync_report = synchronize_categories()
        if _sync_report.get("status") == "warnings":
            for warning in _sync_report.get("warnings", []):
                logger.warning(warning)
        
        # Log the registration with the correct count
        logger.info(f"Registered {len(CATEGORIES)} categories via auto-discovery")
        
    except ImportError:
        logger.warning("Category discovery module not found, using manual registration")
        # Fallback to manual registration if auto-discovery fails
        CATEGORIES = {
            "near_integration": NEARIntegrationCategory,
            "onchain_quality": OnchainQualityCategory,
            "offchain_quality": OffchainQualityCategory,
            "code_quality": CodeQualityCategory,
            "technical_innovation": TechnicalInnovationCategory,
            "team_activity": TeamActivityCategory,
            "ecosystem_fit": EcosystemFitCategory,
        }
        logger.info(f"Registered {len(CATEGORIES)} categories via manual registration")
    
    # Mark discovery as completed
    _discovery_completed = True
    return CATEGORIES

# Initialize categories on module import
_discover_and_register_categories()

def get_category_instance(category_name: str) -> BaseCategory:
    """
    Get a category instance by name.
    
    Args:
        category_name: The name of the category
        
    Returns:
        An instance of the category
    """
    # Ensure categories are discovered
    if not CATEGORIES:
        _discover_and_register_categories()
        
    # Normalize category name
    norm_name = category_name.lower().replace(" ", "_")
    if norm_name.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
        norm_name = norm_name[2:].strip()
    
    # Find the category
    for key, category_class in CATEGORIES.items():
        if key == norm_name or key.endswith(norm_name):
            logger.debug(f"Found category {key} for '{category_name}'")
            return category_class()
    
    # Fallback to near_integration if category not found
    logger.warning(f"Category '{category_name}' not found, falling back to near_integration")
    return NEARIntegrationCategory()
    
def get_all_categories() -> Dict[str, BaseCategory]:
    """
    Get all registered categories as instances.
    
    Returns:
        Dict mapping category keys to category instances
    """
    # Ensure categories are discovered
    if not CATEGORIES:
        _discover_and_register_categories()
    
    # Create instances for all categories
    result = {key: cls() for key, cls in CATEGORIES.items()}
    
    # Log the result for debugging
    logger.info(f"DEBUG: get_all_categories returning {len(result)} categories: {list(result.keys())}")
    
    return result 