"""Infrastructure-layer exceptions."""


class InfrastructureError(Exception):
    """Base class for infra issues."""


class ExternalAPIError(InfrastructureError):
    """Raised when external service requests fail after retries."""
