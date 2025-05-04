from typing import Dict, List, Any, Optional
from .base import BaseCategory

class TechnicalInnovationCategory(BaseCategory):
    """Category evaluating technical innovation and uniqueness of NEAR projects."""
    
    def __init__(self):
        """Initialize the Technical Innovation category."""
        super().__init__("Technical Innovation/Uniqueness", 15)
        
        # Define key indicators
        self.key_indicators = [
            "Novel algorithms",
            "Unique architecture",
            "Advanced techniques",
            "Performance optimizations"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/*.rs",
            "**/*.{js,ts}",
            "**/README.md",
            "**/architecture.md",
            "**/design.md"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [12, 15],
                "criteria": "Highly novel solution, advances state-of-the-art."
            },
            "medium": {
                "range": [7, 11],
                "criteria": "Some innovative elements, derivative model."
            },
            "low": {
                "range": [0, 6],
                "criteria": "Little/no innovation."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Technical Innovation.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an AI technology analyst with expertise in software development and blockchain technology.

Task: Assess the technical innovation and uniqueness demonstrated in the provided code context. Compare the approaches used against standard practices or existing solutions in the relevant domain (e.g., DeFi, NFTs, tooling on NEAR). 
Assign a score out of 15 and provide a justification explaining the innovative aspects or lack thereof, referencing specific techniques, algorithms, or architectural choices found in the code.

Category: Technical Innovation/Uniqueness
Max Points: 15 pts

Scoring Guidelines:
* 12–15 pts: Highly novel solution or approach. Introduces new techniques, significantly improves upon existing methods, or applies technology in a unique way that potentially advances the state-of-the-art within its niche. Look for unique algorithms, clever contract interactions, novel off-chain/on-chain coordination, or solutions to previously unaddressed problems.
* 7–11 pts: Some innovative elements. May incorporate existing technologies in creative ways, offer incremental improvements, or apply a known model to a new area, but isn't fundamentally groundbreaking. Look for interesting feature combinations or solid implementations of moderately complex concepts.
* 0–6 pts: Little or no apparent innovation. Relies heavily on standard patterns, basic implementations of common features, or forks/clones existing projects with minimal modification.

Key Indicators:
- Novel algorithms or data structures
- Unique architectural approaches
- Creative solutions to technical challenges
- Non-standard contract interaction patterns
- Advanced optimization techniques
- Innovative uses of NEAR Protocol features

Input: Relevant code context (potentially including project descriptions or READMEs if provided, highlighting intended innovation).

Output Format:
1. Score: [Score]/15
2. Justification: [Detailed explanation of the perceived technical innovation, referencing specific code sections, architectural designs, or algorithms that support the assessment. Compare to standard practices where possible.]

Note: Assessing true state-of-the-art requires broad knowledge; focus on novel applications or combinations of techniques evident within the provided context relative to common patterns.
"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += """
Additional guidance for Rust projects:
- Look for innovative uses of Rust's type system and safety features
- Check for unique approaches to smart contract design
- Assess novel cross-contract interaction patterns
- Evaluate custom algorithms and data structures
- Look for optimizations that improve gas efficiency or performance
"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += """
Additional guidance for JavaScript/TypeScript projects:
- Look for novel frontend architectures or interaction patterns
- Check for unique approaches to state management
- Assess innovative ways of interacting with NEAR contracts
- Evaluate custom algorithms for client-side processing
- Look for creative UX solutions specific to blockchain challenges
"""
        
        return base_prompt 