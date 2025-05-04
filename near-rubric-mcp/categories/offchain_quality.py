from typing import Dict, List, Any, Optional
from .base import BaseCategory

class OffchainQualityCategory(BaseCategory):
    """Category evaluating offchain quality of NEAR projects."""
    
    def __init__(self):
        """Initialize the Offchain Quality category."""
        super().__init__("Offchain Quality", 15)
        
        # Define key indicators
        self.key_indicators = [
            "Architecture complexity",
            "UI/UX implementation",
            "External integrations",
            "State management"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/src/*.{js,ts,jsx,tsx}",
            "**/pages/*.{js,ts,jsx,tsx}",
            "**/components/*.{js,ts,jsx,tsx}",
            "**/package.json",
            "**/webpack.config.js",
            "**/tsconfig.json"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "complex": {
                "range": [12, 15],
                "criteria": "Dedicated standalone app, complex architecture, robust back-end integrations."
            },
            "moderate": {
                "range": [7, 11],
                "criteria": "Browser extension, moderate complexity."
            },
            "simple": {
                "range": [0, 6],
                "criteria": "Simple off-chain scripts, minimal complexity."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Offchain Quality.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an expert AI software architect evaluating the complexity and quality of off-chain components supporting a blockchain application.

Task: Analyze the provided code context representing the off-chain parts of the project (e.g., frontend, backend, scripts). 
Assess its architectural complexity, robustness, and integration quality. 
Assign a score out of 15 and provide a detailed justification referencing specific code examples.

Category: Offchain Quality
Max Points: 15 pts

Scoring Guidelines:
* 12–15 pts: Dedicated standalone application (web app, mobile app, desktop app) with complex architecture (e.g., distinct frontend/backend, microservices), robust integrations (databases, external APIs, sophisticated state management), suggesting significant development effort. Look for frameworks (React, Vue, Angular, Node.js, Django, etc.), clear separation of concerns, build systems, API definitions.
* 7–11 pts: Moderate complexity, such as a browser extension, a moderately complex single-page application, or a backend with some specific integrations but not a full-scale complex system. Look for evidence of structure beyond simple scripts.
* 0–6 pts: Simple off-chain scripts, command-line tools with minimal complexity, basic frontend with limited functionality, or lack of discernible off-chain architecture.

Key Indicators:
- Use of frontend frameworks (React, Vue, Angular)
- Backend API complexity and organization
- State management approaches
- Build and deployment configuration
- External service integration
- Responsive design and UI/UX quality

Input: Relevant code context (e.g., frontend application code, backend API code, utility scripts, configuration files).

Output Format:
1. Score: [Score]/15
2. Justification: [Detailed explanation of the off-chain architecture's complexity and quality]
"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += """
Additional guidance for Rust projects:
- Look for backend frameworks like Actix, Rocket, or Axum
- Examine data models and database integration
- Assess error handling and middleware implementation
- Check for API endpoint organization
- Evaluate build configuration (Cargo.toml)
"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += """
Additional guidance for JavaScript/TypeScript projects:
- Evaluate component architecture in frontend frameworks
- Look for state management solutions (Redux, Context API, MobX)
- Assess the routing implementation
- Check for API client structure
- Evaluate build and bundling configuration (webpack, vite)
- Look for TypeScript type definitions quality
"""
        
        return base_prompt 