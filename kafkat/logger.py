"""Logging configuration for Kafkat."""

import logging
import sys
from typing import Optional


def setup_logging(verbose: bool = False, quiet: bool = False) -> logging.Logger:
    """Setup logging configuration.
    
    Args:
        verbose: Enable debug logging
        quiet: Disable all logging except errors
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('kafkat')
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set log level
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(log_level)
    
    # Create formatter
    if verbose:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name or 'kafkat')
