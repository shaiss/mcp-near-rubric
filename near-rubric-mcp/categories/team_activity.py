from typing import Dict, List, Any, Optional
from categories.base import BaseCategory

class TeamActivityCategory(BaseCategory):
    """Category evaluating team activity and project maturity of NEAR projects."""
    
    def __init__(self):
        """Initialize the Team Activity category."""
        super().__init__("Team Activity & Project Maturity", 10)
        
        # Define key indicators
        self.key_indicators = [
            "Commit frequency",
            "Code comments with dates",
            "Version history",
            "Multiple contributors"
        ]
        
        # Define file patterns
        self.file_patterns = [
            "**/README.md",
            "**/.git/**",
            "**/CHANGELOG.md",
            "**/TODO.md"
        ]
        
        # Define scoring tiers
        self.scoring_tiers = {
            "high": {
                "range": [8, 10],
                "criteria": "Active commits, ongoing development, clear roadmap."
            },
            "medium": {
                "range": [4, 7],
                "criteria": "Occasional updates, partial roadmap."
            },
            "low": {
                "range": [0, 3],
                "criteria": "Dormant project, unclear future."
            }
        }
    
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for Team Activity.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        base_prompt = """
Role: You are an AI project analyst evaluating project health and development velocity based on available evidence.

Task: Assess the project's activity level and maturity based primarily on information derivable from the provided context. This might include code structure hinting at ongoing development (e.g., versioning, TODOs, modularity for future expansion), documentation (e.g., roadmap sections in README), or metadata if provided (e.g., commit summaries, recent file changes). 
Assign a score out of 10 and provide a justification. Acknowledge if the assessment is limited due to relying solely on code/docs without full repository history.

Category: Team Activity & Project Maturity
Max Points: 10 pts

Scoring Guidelines:
* 8–10 pts: Strong indicators of active, ongoing development and maturity. Code appears well-maintained, possibly includes versioning, comments suggest recent activity or future plans (TODOs, FIXMEs being addressed), documentation might include a clear roadmap or recent updates. (If repo metadata is available: frequent, meaningful commits).
* 4–7 pts: Some signs of activity or structure suggesting past development, but potentially stalled or progressing slowly. Code might be reasonably structured but lack recent updates or clear future plans in comments/docs. (If repo metadata is available: occasional updates, partial roadmap).
* 0–3 pts: Few signs of recent activity or a mature development process. Code might appear abandoned (e.g., old style, unresolved TODOs from long ago), lack structure for growth, or documentation is outdated/missing. (If repo metadata is available: dormant commit history, unclear future).

Key Indicators:
- Evidence of ongoing development (version numbers, dates in comments)
- Presence of roadmap or future plans in documentation
- Multiple contributors visible in code/comments
- Structure indicating long-term planning
- Release notes or changelog entries
- Clear development process evident from organization

Input: Relevant code context, documentation (e.g., README), and potentially repository metadata summaries (if available and provided).

Output Format:
1. Score: [Score]/10
2. Justification: [Detailed explanation based on evidence found (or lack thereof) in the code, comments, documentation, or provided metadata. Explicitly mention limitations if relying only on static code.]
"""
        
        # No specific language guidance for team activity as it's largely language-agnostic
        
        return base_prompt 