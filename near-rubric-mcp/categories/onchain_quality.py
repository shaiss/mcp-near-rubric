from typing import Dict, List, Any, Optional
from categories.base import BaseCategory

class OnchainQualityCategory(BaseCategory):
    """Category evaluating onchain quality of NEAR projects."""
    
    def __init__(self):
        """Initialize the Onchain Quality category."""
        super().__init__("Onchain Quality", 20)
        
        # Define key indicators
        self.key_indicators = [
            "Transaction meaningfulness",
            "State management",
            "Storage patterns",
            "Contract interactions"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/*contract*.rs",
            "**/*.wasm",
            "**/src/lib.rs",
            "**/*transaction*.{js,ts}",
            "**/*contract*.{js,ts}"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [16, 20],
                "criteria": "Real, meaningful interactions with NEAR chain verified through code and live usage."
            },
            "medium": {
                "range": [10, 15],
                "criteria": "Occasional useful on-chain transactions."
            },
            "low": {
                "range": [0, 9],
                "criteria": "Superficial or junk transactions."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Onchain Quality.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an expert AI code auditor analyzing blockchain interactions, specifically on the NEAR Protocol.

Task: Evaluate the quality and meaningfulness of the on-chain interactions implemented in the provided code context. 
Assess whether the transactions serve a core purpose or are superficial. 
Assign a score out of 20 and provide a detailed justification referencing specific code examples.

Category: Onchain Quality
Max Points: 20 pts

Scoring Guidelines:
* 16–20 pts: Real, meaningful interactions. Code shows evidence of transactions core to the application's purpose, verifiable logic impacting state or user experience significantly on-chain. Look for complex contract calls, state changes that reflect core functionality, and potentially verification through associated tests or live usage patterns if available.
* 10–15 pts: Occasional useful on-chain transactions. Code implements some necessary on-chain interactions, but they might be infrequent, less critical to the core loop, or simpler in nature.
* 0–9 pts: Superficial or junk transactions. Interactions seem designed merely to 'touch' the chain, lack clear purpose, are potentially low-value (e.g., simple greetings, trivial state updates), or cannot be verified as meaningful from the code.

Key Indicators:
- Core functionality implemented on-chain
- Complex contract calls
- Meaningful state changes
- Evidence of transaction flow
- Smart contract storage patterns
- Proper error handling for transactions

Input: Relevant code context (e.g., smart contract functions performing actions, backend/frontend code initiating transactions).

Output Format:
1. Score: [Score]/20
2. Justification: [Detailed explanation assessing the quality and purpose of on-chain interactions based on the code]
"""
        
        # Add project type specific guidance
        if project_type:
            if project_type.lower() == "rust":
                base_prompt += """
Additional guidance for Rust projects:
- Look for #[payable] functions indicating monetary transactions
- Examine state changes in contract storage
- Check for Promise calls and proper Promise handling
- Evaluate the complexity and meaning of transaction logic
- Check for proper access controls (require!, assert!)
"""
            elif project_type.lower() in ["javascript", "js", "typescript", "ts"]:
                base_prompt += """
Additional guidance for JavaScript/TypeScript projects:
- Look for transaction creation and signing
- Examine contract call methods (view vs. change methods)
- Check for proper error handling in transactions
- Evaluate if transactions are core to the application flow
- Check for proper gas management
"""
        
        return base_prompt 