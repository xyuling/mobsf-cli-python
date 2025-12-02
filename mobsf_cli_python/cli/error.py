"""CLI error handling."""

from mobsf_core.error import MobsfError


class AppError(Exception):
    """Application error."""
    
    def __init__(self, message: str):
        """Initialize AppError.
        
        Args:
            message: Error message
        """
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        """String representation."""
        return self.message
    
    @classmethod
    def from_mobsf_error(cls, error: MobsfError) -> "AppError":
        """Create AppError from MobsfError.
        
        Args:
            error: MobsfError instance
            
        Returns:
            AppError instance
        """
        return cls(str(error))
