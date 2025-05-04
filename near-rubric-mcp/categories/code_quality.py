from typing import Dict, List, Any, Optional
from .base import BaseCategory

class CodeQualityCategory(BaseCategory):
    """Category evaluating code quality and documentation of NEAR projects."""
    
    def __init__(self):
        """Initialize the Code Quality category."""
        super().__init__("Code Quality & Documentation", 15)
        
        # Define key indicators
        self.key_indicators = [
            "Documentation presence",
            "Test coverage",
            "Code organization",
            "Error handling"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/tests/**",
            "**/README.md",
            "**/docs/**",
            "**/*.rs",
            "**/*.{js,ts,jsx,tsx}"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [12, 15],
                "criteria": "Clean, modular, tested code; extensive documentation."
            },
            "medium": {
                "range": [7, 11],
                "criteria": "Moderate clarity, some tests/docs."
            },
            "low": {
                "range": [0, 6],
                "criteria": "Poorly organized, minimal/no documentation."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Code Quality.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an expert AI code reviewer assessing code structure, readability, maintainability, testing practices, and documentation.

Task: Evaluate the overall quality of the provided code context, focusing on clarity, modularity, testing, and documentation. 
Assign a score out of 15 and provide a detailed justification with specific examples from the code.

Category: Code Quality & Documentation
Max Points: 15 pts

Scoring Guidelines:
* 12–15 pts: Clean, modular, well-structured code. Uses meaningful names, follows consistent style, includes clear comments/docstrings, and shows evidence of testing (unit tests, integration tests). Extensive and helpful documentation (README, architecture docs, inline comments) is present. Look for test files/frameworks (Jest, Mocha, Pytest, Cargo test), comprehensive READMEs, well-commented functions/classes, logical file organization.
* 7–11 pts: Moderate clarity and organization. Some parts may be well-structured, while others are less clear. Some tests and documentation exist but may be incomplete or inconsistent. Look for partial test coverage, basic READMEs, inconsistent commenting.
* 0–6 pts: Poorly organized, difficult-to-read code. Lack of modularity (e.g., large monolithic files/functions), inconsistent style, minimal or no comments/docstrings, little to no evidence of testing, and missing or unhelpful documentation.

Key Indicators:
- Test file presence and coverage
- Documentation quality (inline comments, READMEs, docs)
- Code organization and modularity
- Consistent naming conventions and style
- Error handling thoroughness
- Function/component size and complexity
- Use of type systems (if applicable)

Input: Relevant code context (e.g., source code files across different modules/components, test files, documentation files).

Output Format:
1. Score: [Score]/15
2. Justification: [Detailed explanation of code quality aspects (readability, modularity, testing, documentation), referencing specific examples]
"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += """
Additional guidance for Rust projects:
- Check for proper doc comments (///, //!)
- Look for unit tests and integration tests
- Assess use of Rust idioms and patterns
- Check for proper error handling with Result and Option
- Evaluate consistent code organization
- Look for cargo test integration
"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += """
Additional guidance for JavaScript/TypeScript projects:
- Check for properly configured testing frameworks (Jest, Mocha)
- Look for JSDoc or TSDoc comments
- Assess TypeScript type usage and quality
- Check for consistent component patterns
- Evaluate ESLint/Prettier configuration and adherence
- Look for proper error boundary handling
"""
        
        return base_prompt 