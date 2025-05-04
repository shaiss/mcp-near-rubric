from typing import Dict, List, Any, Optional

class BaseCategory:
    """Base class for evaluation categories."""
    
    def __init__(self, name: str, max_points: int = 20):
        """
        Initialize a category.
        
        Args:
            name: The name of the category
            max_points: The maximum points for this category
        """
        self.name = name
        self.max_points = max_points
        self.key_indicators = []
        self.file_patterns = []
        self.scoring_tiers = {}
        
    def get_key_indicators(self) -> List[str]:
        """Get key indicators for this category."""
        return self.key_indicators
        
    def get_file_patterns(self) -> List[str]:
        """Get file patterns for this category."""
        return self.file_patterns
        
    def get_scoring_tiers(self) -> Dict[str, Any]:
        """Get scoring tiers for this category."""
        return self.scoring_tiers
        
    async def get_evaluation_framework(self, project_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the evaluation framework for this category.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Dict containing the evaluation framework
        """
        return {
            "category": self.name,
            "max_points": self.max_points,
            "key_indicators": self.get_key_indicators(),
            "file_patterns": self.get_file_patterns(),
            "scoring_tiers": self.get_scoring_tiers(),
            "evaluation_prompt": self.get_evaluation_prompt(project_type)
        }
        
    def get_evaluation_prompt(self, project_type: Optional[str] = None) -> str:
        """
        Get the evaluation prompt for this category.
        
        Args:
            project_type: Optional project type (rust, javascript, mixed)
            
        Returns:
            Evaluation prompt string
        """
        raise NotImplementedError("Subclasses must implement get_evaluation_prompt") 