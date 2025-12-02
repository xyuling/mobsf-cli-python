"""Error handling for MobSF Core."""

from enum import Enum
from typing import Optional


class ErrorCause(Enum):
    """Error cause enumeration."""
    
    HTTP_CLIENT_ERROR = "HttpClientError"
    IO_ERROR = "IoError"
    INVALID_HTTP_RESPONSE = "InvalidHttpResponse"


class MobsfError(Exception):
    """MobSF Error exception."""
    
    def __init__(self, cause: ErrorCause, message: str, status_code: Optional[int] = None):
        """Initialize MobsfError.
        
        Args:
            cause: The error cause
            message: Error message
            status_code: HTTP status code if applicable
        """
        self.cause = cause
        self.message = message
        self.status_code = status_code
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format error message."""
        if self.status_code:
            return f"{self.cause.value}({self.status_code}): {self.message}"
        return f"{self.cause.value}: {self.message}"
    
    def __str__(self) -> str:
        """String representation."""
        return self._format_message()
    
    def __repr__(self) -> str:
        """Debug representation."""
        return f"MobsfError(cause={self.cause}, message={self.message}, status_code={self.status_code})"
