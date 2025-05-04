#!/usr/bin/env python
"""
Category creation script for NEAR Rubric MCP.
This script helps users generate new categories, including creating the category class, 
prompt template, and updating configuration files.
"""

import os
import sys
import json
import yaml
import shutil
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("category_creator")

# Define the base paths
BASE_DIR = Path(__file__).parent.parent
CATEGORIES_DIR = BASE_DIR / "categories"
PROMPTS_DIR = BASE_DIR / "resources" / "prompts"
CONFIG_DIR = BASE_DIR / "config"
RUBRIC_PATH = CONFIG_DIR / "rubric.yaml"
PATTERNS_PATH = CONFIG_DIR / "patterns.yaml"

CATEGORY_TEMPLATE = """from typing import Dict, List, Any, Optional
from .base import BaseCategory

class {class_name}(BaseCategory):
    \"""Category evaluating {category_name}.\"""
    
    def __init__(self):
        \"""Initialize the {category_name} category.\"""
        super().__init__("{category_name}", {max_points})
        
        # Define key indicators
        self.key_indicators = [
            "{indicator1}",
            "{indicator2}",
            "{indicator3}",
            "{indicator4}"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "{file_pattern1}",
            "{file_pattern2}",
            "{file_pattern3}"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [{high_min}, {max_points}],
                "criteria": "{high_criteria}"
            },
            "medium": {
                "range": [{medium_min}, {high_min-1}],
                "criteria": "{medium_criteria}"
            },
            "low": {
                "range": [0, {medium_min-1}],
                "criteria": "{low_criteria}"
            }
        }
        
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        \"""
        Get the evaluation prompt for this category.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        \"""
        base_prompt = \"""
Role: You are an expert AI code auditor specializing in the NEAR Protocol ecosystem.

Task: Evaluate the provided code context for {category_name} based on the following criteria. 
Assign a score out of {max_points} and provide a detailed justification referencing specific code examples.

Category: {category_name}
Max Points: {max_points} pts

Scoring Guidelines:
* {high_min}–{max_points} pts: {high_criteria}
* {medium_min}–{high_min-1} pts: {medium_criteria}
* 0–{medium_min-1} pts: {low_criteria}

Look for:
- {indicator1}
- {indicator2}
- {indicator3}
- {indicator4}

Input: Relevant code context

Output Format:
1. Score: [Score]/{max_points}
2. Justification: [Detailed explanation with evidence]
\"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += \"""
Additional guidance for Rust projects:
- Check for Rust-specific implementations
- Look for NEAR SDK usage
\"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += \"""
Additional guidance for JavaScript/TypeScript projects:
- Check for JS/TS specific implementations
- Look for NEAR JS API usage
\"""
        
        return base_prompt
"""

PROMPT_TEMPLATE = """Role: You are an expert AI code auditor specializing in the NEAR Protocol ecosystem.

Task: Evaluate the provided code context for {category_name} based on the following criteria. 
Assign a score out of {max_points} and provide a detailed justification referencing specific code examples.

Category: {category_name}
Max Points: {max_points} pts

Scoring Guidelines:
* {high_min}–{max_points} pts: {high_criteria}
* {medium_min}–{high_min-1} pts: {medium_criteria}
* 0–{medium_min-1} pts: {low_criteria}

Look for:
- {indicator1}
- {indicator2}
- {indicator3}
- {indicator4}

Input: Relevant code context

Output Format:
1. Score: [Score]/{max_points}
2. Justification: [Detailed explanation with evidence]
"""

def normalize_name(name: str) -> str:
    """Normalize a category name for file and class names."""
    # Remove any numbering prefix
    if name.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
        name = name[2:].strip()
    
    return name

def to_class_name(name: str) -> str:
    """Convert a category name to a class name."""
    normalized = normalize_name(name)
    
    # Convert to CamelCase
    parts = normalized.replace("-", " ").replace("_", " ").title().split()
    class_name = "".join(parts) + "Category"
    
    return class_name

def to_file_name(name: str) -> str:
    """Convert a category name to a file name."""
    normalized = normalize_name(name)
    
    # Convert to snake_case
    file_name = normalized.lower().replace(" ", "_").replace("-", "_")
    
    return file_name

def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Load a YAML file."""
    if not path.exists():
        logger.warning(f"⚠️  File not found: {path}")
        return {}
    
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"❌ Error loading YAML file: {str(e)}")
        return {}

def save_yaml_file(path: Path, data: Dict[str, Any]) -> bool:
    """Save a YAML file."""
    try:
        # Create a backup first
        if path.exists():
            backup_path = path.with_suffix(f".yaml.bak")
            shutil.copy2(path, backup_path)
            logger.info(f"✅ Created backup: {backup_path}")
        
        # Save the file
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        logger.info(f"✅ Saved YAML file: {path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving YAML file: {str(e)}")
        return False

def create_category_class(
    category_name: str, 
    max_points: int, 
    indicators: List[str], 
    file_patterns: List[str],
    high_criteria: str,
    medium_criteria: str,
    low_criteria: str
) -> bool:
    """Create a new category class file."""
    # Prepare parameters
    class_name = to_class_name(category_name)
    file_name = to_file_name(category_name)
    file_path = CATEGORIES_DIR / f"{file_name}.py"
    
    # Calculate scoring tier thresholds
    high_min = int(max_points * 0.75)
    medium_min = int(max_points * 0.4)
    
    # Ensure we have enough indicators and file patterns
    while len(indicators) < 4:
        indicators.append(f"Key indicator {len(indicators) + 1}")
    
    while len(file_patterns) < 3:
        file_patterns.append(f"**/*.{len(file_patterns) + 1}")
    
    # Create the category class file
    try:
        content = CATEGORY_TEMPLATE.format(
            class_name=class_name,
            category_name=category_name,
            max_points=max_points,
            indicator1=indicators[0],
            indicator2=indicators[1],
            indicator3=indicators[2],
            indicator4=indicators[3],
            file_pattern1=file_patterns[0],
            file_pattern2=file_patterns[1],
            file_pattern3=file_patterns[2],
            high_min=high_min,
            medium_min=medium_min,
            high_criteria=high_criteria,
            medium_criteria=medium_criteria,
            low_criteria=low_criteria
        )
        
        with open(file_path, "w") as f:
            f.write(content)
        
        logger.info(f"✅ Created category class: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating category class: {str(e)}")
        return False

def create_prompt_template(
    category_name: str, 
    max_points: int, 
    indicators: List[str],
    high_criteria: str,
    medium_criteria: str,
    low_criteria: str
) -> bool:
    """Create a new prompt template file."""
    # Prepare parameters
    file_name = to_file_name(category_name)
    file_path = PROMPTS_DIR / f"{file_name}.txt"
    
    # Calculate scoring tier thresholds
    high_min = int(max_points * 0.75)
    medium_min = int(max_points * 0.4)
    
    # Ensure we have enough indicators
    while len(indicators) < 4:
        indicators.append(f"Key indicator {len(indicators) + 1}")
    
    # Create the prompt template file
    try:
        content = PROMPT_TEMPLATE.format(
            category_name=category_name,
            max_points=max_points,
            indicator1=indicators[0],
            indicator2=indicators[1],
            indicator3=indicators[2],
            indicator4=indicators[3],
            high_min=high_min,
            medium_min=medium_min,
            high_criteria=high_criteria,
            medium_criteria=medium_criteria,
            low_criteria=low_criteria
        )
        
        with open(file_path, "w") as f:
            f.write(content)
        
        logger.info(f"✅ Created prompt template: {file_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating prompt template: {str(e)}")
        return False

def update_rubric_config(
    category_name: str, 
    max_points: int, 
    indicators: List[str], 
    file_patterns: List[str],
    high_criteria: str,
    medium_criteria: str,
    low_criteria: str
) -> bool:
    """Update the rubric.yaml file with the new category."""
    # Load the current rubric config
    rubric_config = load_yaml_file(RUBRIC_PATH)
    
    # Get the categories section
    categories = rubric_config.get("categories", {})
    
    # Calculate scoring tier thresholds
    high_min = int(max_points * 0.75)
    medium_min = int(max_points * 0.4)
    
    # Create the category configuration
    file_name = to_file_name(category_name)
    
    # Prepare the category configuration
    categories[file_name] = {
        "max_points": max_points,
        "evaluation_type": "hybrid",
        "key_indicators": indicators,
        "file_patterns": file_patterns,
        "scoring_tiers": {
            "high": {
                "range": [high_min, max_points],
                "criteria": high_criteria
            },
            "medium": {
                "range": [medium_min, high_min - 1],
                "criteria": medium_criteria
            },
            "low": {
                "range": [0, medium_min - 1],
                "criteria": low_criteria
            }
        }
    }
    
    # Update the rubric config
    rubric_config["categories"] = categories
    
    # Save the updated config
    return save_yaml_file(RUBRIC_PATH, rubric_config)

def update_patterns_config(
    category_name: str, 
    patterns: Dict[str, List[str]]
) -> bool:
    """Update the patterns.yaml file with the new category."""
    # Load the current patterns config
    patterns_config = load_yaml_file(PATTERNS_PATH)
    
    # Get the patterns section
    all_patterns = patterns_config.get("patterns", {})
    
    # Create the patterns configuration
    file_name = to_file_name(category_name)
    
    # Update the patterns config
    all_patterns[file_name] = patterns
    
    # Update the patterns config
    patterns_config["patterns"] = all_patterns
    
    # Save the updated config
    return save_yaml_file(PATTERNS_PATH, patterns_config)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Create a new category for NEAR Rubric MCP")
    
    parser.add_argument("--name", required=True, help="The name of the category (e.g., 'NEAR Integration')")
    parser.add_argument("--points", type=int, default=20, help="The maximum points for the category (default: 20)")
    
    parser.add_argument("--indicators", nargs="+", default=[], help="Key indicators for the category (at least 1)")
    parser.add_argument("--file-patterns", nargs="+", default=[], help="File patterns for the category (at least 1)")
    
    parser.add_argument("--high-criteria", help="Criteria for high scores")
    parser.add_argument("--medium-criteria", help="Criteria for medium scores")
    parser.add_argument("--low-criteria", help="Criteria for low scores")
    
    parser.add_argument("--rust-patterns", nargs="+", default=[], help="Rust-specific patterns")
    parser.add_argument("--js-patterns", nargs="+", default=[], help="JavaScript-specific patterns")
    parser.add_argument("--common-patterns", nargs="+", default=[], help="Common patterns")
    
    parser.add_argument("--skip-class", action="store_true", help="Skip creating the category class")
    parser.add_argument("--skip-prompt", action="store_true", help="Skip creating the prompt template")
    parser.add_argument("--skip-rubric", action="store_true", help="Skip updating the rubric.yaml file")
    parser.add_argument("--skip-patterns", action="store_true", help="Skip updating the patterns.yaml file")
    
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Set default values
    category_name = args.name
    max_points = args.points
    
    indicators = args.indicators or [
        f"Key indicator 1 for {category_name}",
        f"Key indicator 2 for {category_name}",
        f"Key indicator 3 for {category_name}",
        f"Key indicator 4 for {category_name}"
    ]
    
    file_patterns = args.file_patterns or [
        "**/README.md",
        "**/*.rs",
        "**/*.{js,ts}"
    ]
    
    high_criteria = args.high_criteria or f"Excellent {category_name}"
    medium_criteria = args.medium_criteria or f"Good {category_name}"
    low_criteria = args.low_criteria or f"Poor {category_name}"
    
    patterns = {
        "rust": args.rust_patterns or ["trait", "impl", "#\\[test\\]"],
        "javascript": args.js_patterns or ["function", "class", "import"],
        "common": args.common_patterns or ["test", "README", "documentation"]
    }
    
    # Create the necessary files and update configurations
    success = True
    
    # Create the category class
    if not args.skip_class:
        success = success and create_category_class(
            category_name, max_points, indicators, file_patterns,
            high_criteria, medium_criteria, low_criteria
        )
    
    # Create the prompt template
    if not args.skip_prompt:
        success = success and create_prompt_template(
            category_name, max_points, indicators,
            high_criteria, medium_criteria, low_criteria
        )
    
    # Update the rubric.yaml file
    if not args.skip_rubric:
        success = success and update_rubric_config(
            category_name, max_points, indicators, file_patterns,
            high_criteria, medium_criteria, low_criteria
        )
    
    # Update the patterns.yaml file
    if not args.skip_patterns:
        success = success and update_patterns_config(
            category_name, patterns
        )
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"Category Creation Summary for '{category_name}'")
    print("=" * 80 + "\n")
    
    file_name = to_file_name(category_name)
    class_name = to_class_name(category_name)
    
    print(f"Category Key: {file_name}")
    print(f"Class Name: {class_name}")
    print(f"Max Points: {max_points}")
    print(f"Indicators: {', '.join(indicators[:4])}")
    print(f"File Patterns: {', '.join(file_patterns[:3])}")
    print(f"High Criteria: {high_criteria}")
    print(f"Medium Criteria: {medium_criteria}")
    print(f"Low Criteria: {low_criteria}")
    print()
    
    if success:
        print("✅ Category creation completed successfully!")
        
        # Provide guidance on next steps
        print("\nNext Steps:")
        print(f"1. Run the validation script: python scripts/validate_config.py")
        print(f"2. Review the generated files:")
        if not args.skip_class:
            print(f"   - categories/{file_name}.py")
        if not args.skip_prompt:
            print(f"   - resources/prompts/{file_name}.txt")
        if not args.skip_rubric:
            print(f"   - config/rubric.yaml")
        if not args.skip_patterns:
            print(f"   - config/patterns.yaml")
    else:
        print("⚠️  Category creation completed with warnings. Please check the logs.")
    
    print("\n" + "=" * 80)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 