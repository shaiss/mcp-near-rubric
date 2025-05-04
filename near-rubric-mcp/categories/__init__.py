# NEAR Rubric MCP Categories Package
"""Category implementations for NEAR Rubric evaluation."""

import logging
from typing import Dict, Type, Any

from .base import BaseCategory
from .near_integration import NEARIntegrationCategory
from .onchain_quality import OnchainQualityCategory
from .offchain_quality import OffchainQualityCategory
from .code_quality import CodeQualityCategory
from .technical_innovation import TechnicalInnovationCategory
from .team_activity import TeamActivityCategory
from .ecosystem_fit import EcosystemFitCategory

# Set up logger
logger = logging.getLogger("categories")

# Import category discovery utilities
try:
    from .category_discovery import discover_category_classes, synchronize_categories
    
    # Use auto-discovery for categories
    _discovered_categories = discover_category_classes()
    
    # For backward compatibility, we'll keep the manual list as a fallback
    MANUAL_CATEGORIES = {
        "near_integration": NEARIntegrationCategory,
        "onchain_quality": OnchainQualityCategory,
        "offchain_quality": OffchainQualityCategory,
        "code_quality": CodeQualityCategory,
        "technical_innovation": TechnicalInnovationCategory,
        "team_activity": TeamActivityCategory,
        "ecosystem_fit": EcosystemFitCategory,
    }
    
    # Combine both, with discovered categories taking precedence
    CATEGORIES = {**MANUAL_CATEGORIES, **_discovered_categories}
    
    # Run synchronization check on startup
    _sync_report = synchronize_categories()
    if _sync_report.get("status") == "warnings":
        for warning in _sync_report.get("warnings", []):
            logger.warning(warning)
    
    logger.info(f"Registered {len(CATEGORIES)} categories")
    
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

def get_category_instance(category_name: str) -> BaseCategory:
    """
    Get a category instance by name.
    
    Args:
        category_name: The name of the category
        
    Returns:
        An instance of the category
    """
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
    return {key: cls() for key, cls in CATEGORIES.items()} 