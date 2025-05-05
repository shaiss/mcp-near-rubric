from typing import Dict, List, Any, Optional
from categories.base import BaseCategory

class EcosystemFitCategory(BaseCategory):
    """Category evaluating ecosystem fit and grant impact of NEAR projects."""
    
    def __init__(self):
        """Initialize the Ecosystem Fit category."""
        super().__init__("Grant Impact & Ecosystem Fit", 5)
        
        # Define key indicators
        self.key_indicators = [
            "NEAR ecosystem references",
            "Integration with other NEAR projects",
            "NEAR community participation",
            "NEAR-specific use cases"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/README.md",
            "**/documentation/**",
            "**/docs/**"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [4, 5],
                "criteria": "Strong ecosystem alignment, clear beneficial impact."
            },
            "medium": {
                "range": [2, 3],
                "criteria": "Moderate alignment, niche impact."
            },
            "low": {
                "range": [0, 1],
                "criteria": "Weak fit, unclear impact."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Ecosystem Fit.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an AI ecosystem analyst evaluating how well a software project aligns with the goals and needs of a specific ecosystem (NEAR Protocol).

Task: Assess the potential impact of the project and its alignment with the NEAR ecosystem based on the provided code context and any accompanying documentation (like a README or project description). Consider the problem the code aims to solve and its relevance to NEAR users or developers. 
Assign a score out of 5 and provide a justification.

Category: Grant Impact & Ecosystem Fit
Max Points: 5 pts

Scoring Guidelines:
* 4–5 pts: Strong ecosystem alignment and clear potential impact. The project addresses a recognized need or opportunity within the NEAR ecosystem (e.g., improves developer tooling, enhances user experience, fills a DeFi/NFT niche, supports core infra). The code's purpose clearly benefits NEAR. Look for explicit mentions in docs or infer from the functionality implemented in the code (e.g., building on specific NEAR primitives, integrating with key NEAR projects).
* 2–3 pts: Moderate alignment or niche impact. The project has some relevance but may target a smaller user group, address a less critical need, or have an indirect connection to core NEAR goals. The code provides some value but perhaps not broadly applicable.
* 0–1 pts: Weak fit or unclear impact. The project's relevance to the NEAR ecosystem is unclear from the code and documentation, it might be a generic tool with incidental NEAR usage, or its potential impact seems minimal or poorly defined.

Key Indicators:
- Direct references to NEAR ecosystem needs
- Integration with existing NEAR projects
- Addressing known gaps in the NEAR ecosystem
- Enhancing usability of NEAR Protocol
- Potential user base within NEAR community
- Contribution to NEAR's ecosystem growth

Input: Relevant code context, documentation (e.g., README, project description outlining goals).

Output Format:
1. Score: [Score]/5
2. Justification: [Detailed explanation of the project's perceived fit and impact within the NEAR ecosystem, based on the code's functionality and any provided descriptions. Reference specific features or stated goals.]
"""
        
        # No specific language guidance for ecosystem fit as it's largely language-agnostic
        
        return base_prompt 