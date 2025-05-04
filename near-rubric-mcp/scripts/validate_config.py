#!/usr/bin/env python
"""
Validation script for NEAR Rubric MCP configuration.
This script checks for consistency between categories, prompt templates, and configuration files.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("config_validator")

def find_category_files() -> List[str]:
    """Find all category modules in the categories directory."""
    categories_dir = Path(__file__).parent.parent / "categories"
    category_files = []
    
    for file_path in categories_dir.glob("*.py"):
        if file_path.name not in ["__init__.py", "__pycache__", "category_discovery.py", "base.py"]:
            category_files.append(str(file_path))
    
    return category_files

def find_prompt_templates() -> List[str]:
    """Find all prompt template files in the resources/prompts directory."""
    prompts_dir = Path(__file__).parent.parent / "resources" / "prompts"
    template_files = []
    
    for file_path in prompts_dir.glob("*.txt"):
        template_files.append(str(file_path))
    
    return template_files

def check_yaml_config() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Check for existence and load YAML config files."""
    config_dir = Path(__file__).parent.parent / "config"
    rubric_path = config_dir / "rubric.yaml"
    patterns_path = config_dir / "patterns.yaml"
    
    rubric_config = None
    patterns_config = None
    
    # Check rubric.yaml
    if not rubric_path.exists():
        logger.error(f"❌ rubric.yaml file not found at {rubric_path}")
    else:
        try:
            import yaml
            with open(rubric_path, "r") as f:
                rubric_config = yaml.safe_load(f)
            logger.info(f"✅ rubric.yaml loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading rubric.yaml: {str(e)}")
    
    # Check patterns.yaml
    if not patterns_path.exists():
        logger.error(f"❌ patterns.yaml file not found at {patterns_path}")
    else:
        try:
            import yaml
            with open(patterns_path, "r") as f:
                patterns_config = yaml.safe_load(f)
            logger.info(f"✅ patterns.yaml loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading patterns.yaml: {str(e)}")
    
    return rubric_config or {}, patterns_config or {}

def get_category_keys() -> List[str]:
    """Get all category keys from the category registry."""
    try:
        from categories import get_all_categories
        categories = get_all_categories()
        return list(categories.keys())
    except ImportError:
        logger.error("❌ Could not import get_all_categories from categories module")
        return []

def validate_config() -> Dict[str, Any]:
    """
    Validate the entire configuration and return a report.
    
    Returns:
        Dict containing the validation report
    """
    # Find all category files
    category_files = find_category_files()
    logger.info(f"Found {len(category_files)} category files")
    
    # Find all prompt templates
    template_files = find_prompt_templates()
    logger.info(f"Found {len(template_files)} prompt template files")
    
    # Check YAML config files
    rubric_config, patterns_config = check_yaml_config()
    
    # Get category keys from registry
    category_keys = get_category_keys()
    logger.info(f"Found {len(category_keys)} registered categories")
    
    # Check for missing prompt templates
    template_keys = [Path(path).stem for path in template_files]
    missing_templates = []
    
    for category_key in category_keys:
        # Try to find a matching template (exact or suffix)
        found = False
        for template_key in template_keys:
            if category_key == template_key or category_key.endswith(template_key):
                found = True
                break
        
        if not found:
            missing_templates.append(category_key)
            logger.warning(f"❌ Category '{category_key}' has no matching prompt template")
    
    # Check for categories missing from rubric.yaml
    rubric_categories = rubric_config.get("categories", {}).keys()
    missing_from_rubric = []
    
    for category_key in category_keys:
        # Try to find a matching rubric category
        found = False
        for rubric_key in rubric_categories:
            if category_key == rubric_key or category_key.endswith(rubric_key):
                found = True
                break
        
        if not found:
            missing_from_rubric.append(category_key)
            logger.warning(f"❌ Category '{category_key}' is missing from rubric.yaml")
    
    # Check for categories missing from patterns.yaml
    patterns_categories = patterns_config.get("patterns", {}).keys()
    missing_from_patterns = []
    
    for category_key in category_keys:
        # Try to find a matching patterns category
        found = False
        for pattern_key in patterns_categories:
            if category_key == pattern_key or category_key.endswith(pattern_key):
                found = True
                break
        
        if not found:
            missing_from_patterns.append(category_key)
            logger.warning(f"❌ Category '{category_key}' is missing from patterns.yaml")
    
    # Prepare the validation report
    report = {
        "category_files": category_files,
        "template_files": template_files,
        "registered_categories": category_keys,
        "rubric_categories": list(rubric_categories),
        "pattern_categories": list(patterns_categories),
        "missing_templates": missing_templates,
        "missing_from_rubric": missing_from_rubric,
        "missing_from_patterns": missing_from_patterns,
        "status": "success" if not (missing_templates or missing_from_rubric or missing_from_patterns) else "warnings"
    }
    
    return report

def print_report(report: Dict[str, Any]) -> None:
    """Print a formatted validation report."""
    print("\n" + "=" * 80)
    print("NEAR Rubric MCP Configuration Validation Report")
    print("=" * 80 + "\n")
    
    print(f"Status: {'✅ SUCCESS' if report['status'] == 'success' else '⚠️  WARNINGS'}\n")
    
    print(f"Found {len(report['category_files'])} category files")
    print(f"Found {len(report['template_files'])} prompt template files")
    print(f"Found {len(report['registered_categories'])} registered categories")
    print(f"Found {len(report['rubric_categories'])} categories in rubric.yaml")
    print(f"Found {len(report['pattern_categories'])} categories in patterns.yaml\n")
    
    if report['missing_templates']:
        print("⚠️  Categories missing prompt templates:")
        for category in report['missing_templates']:
            print(f"   - {category}")
        print()
    
    if report['missing_from_rubric']:
        print("⚠️  Categories missing from rubric.yaml:")
        for category in report['missing_from_rubric']:
            print(f"   - {category}")
        print()
    
    if report['missing_from_patterns']:
        print("⚠️  Categories missing from patterns.yaml:")
        for category in report['missing_from_patterns']:
            print(f"   - {category}")
        print()
    
    if report['status'] == 'success':
        print("✅ All category files, prompt templates, and configuration files are in sync!")
    
    print("\n" + "=" * 80)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate NEAR Rubric MCP configuration files")
    parser.add_argument("--json", action="store_true", help="Output the report in JSON format")
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_args()
    
    try:
        report = validate_config()
        
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_report(report)
        
        # Exit with a non-zero code if there are warnings
        sys.exit(0 if report["status"] == "success" else 1)
    except Exception as e:
        logger.error(f"Error validating configuration: {str(e)}", exc_info=True)
        sys.exit(2)

if __name__ == "__main__":
    main() 