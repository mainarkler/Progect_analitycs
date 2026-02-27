"""Domain-level errors.

These exceptions represent pure business failures that are independent
from transport/framework concerns.
"""


class DomainError(Exception):
    """Base class for domain failures."""


class InvalidCalculationInputError(DomainError):
    """Raised when financial input data violates business constraints."""
