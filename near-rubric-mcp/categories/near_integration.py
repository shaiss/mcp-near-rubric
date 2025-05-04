from typing import Dict, List, Any, Optional
from .base import BaseCategory

class NEARIntegrationCategory(BaseCategory):
    """Category evaluating NEAR Protocol integration."""
    
    def __init__(self):
        """Initialize the NEAR Integration category."""
        super().__init__("NEAR Protocol Integration", 20)
        
        # Define key indicators
        self.key_indicators = [
            "NEAR SDK presence",
            "Smart contract implementation",
            "Wallet integration",
            "NEP standards compliance"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/*contract*.rs",
            "**/Cargo.toml",
            "**/*near*.{js,ts}",
            "**/src/lib.rs",
            "**/src/main.rs",
            "**/near.config.js",
            "**/wallet*.{js,ts}"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "advanced": {
                "range": [16, 20],
                "criteria": "Deep integration with advanced features such as cross-contract calls, promise chaining, advanced wallet integration, and standards compliance."
            },
            "moderate": {
                "range": [10, 15],
                "criteria": "Basic integration with standard contract methods, simple wallet connection, and basic NEAR functionality."
            },
            "minimal": {
                "range": [0, 9],
                "criteria": "Limited or no NEAR integration, minimal SDK usage, or only superficial connections."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for NEAR Integration.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an expert AI code auditor specializing in the NEAR Protocol ecosystem.

Task: Evaluate the provided code context for its integration with the NEAR Protocol based on the following criteria. 
Assign a score out of 20 and provide a detailed justification referencing specific code examples.

Category: NEAR Protocol Integration
Max Points: 20 pts

Scoring Guidelines:
* 16–20 pts: Deep integration. Demonstrates significant use of NEAR standards (NEPs), advanced features (e.g., cross-contract calls, Promises), robust wallet integration, and potentially innovative on-chain logic. Look for extensive use of NEAR SDKs (e.g., near-sdk-rs, near-sdk-js), clear contract structure, and interaction with core NEAR concepts.
* 10–15 pts: Moderate NEAR use. Shows functional integration, possibly using basic contract calls, standard wallet connections, but may lack depth or adherence to advanced standards. Look for core SDK usage but perhaps simpler contract logic or partial feature implementation.
* 0–9 pts: Minimal to no direct integration. Code shows little or no interaction with the NEAR blockchain, minimal SDK usage, or only superficial connections.

Look for:
- NEAR SDK usage (near-sdk-rs, near-sdk-js)
- Smart contract implementation
- Wallet integration
- NEP standards compliance
- Cross-contract calls
- State management

Input: Relevant code context (smart contracts, frontend integration snippets, backend interaction code).

Output Format:
1. Score: [Score]/20
2. Justification: [Detailed explanation with evidence]
"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += """
Additional guidance for Rust projects:
- Check for #[near_bindgen] attribute on contract structs
- Look for near-sdk imports (use near_sdk::{...})
- Examine initialization functions (default, new, init)
- Check for contract storage patterns (e.g., LookupMap, Vector, UnorderedMap)
- Look for cross-contract calls using Promise
- Check for proper serialization/deserialization with Borsh
"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += """
Additional guidance for JavaScript/TypeScript projects:
- Check for near-api-js or near-sdk-js imports
- Look for wallet connection implementation (connect, signIn methods)
- Examine contract call patterns (viewMethod, callMethod)
- Check for proper transaction signing and error handling
- Look for proper account management
"""
        
        return base_prompt 