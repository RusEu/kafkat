"""Custom exceptions for Kafkat."""


class KafkatError(Exception):
    """Base exception for Kafkat."""
    pass


class ConnectionError(KafkatError):
    """Raised when unable to connect to Kafka."""
    pass


class TopicError(KafkatError):
    """Raised when topic-related operations fail."""
    pass


class SearchError(KafkatError):
    """Raised when search operations fail."""
    pass


class ConfigurationError(KafkatError):
    """Raised when configuration is invalid."""
    pass
