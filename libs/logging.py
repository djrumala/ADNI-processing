"""
Logging utilities for tracking pipeline execution.
"""

import logging
from pathlib import Path
from datetime import datetime

from .config import LOG_DIR, LOG_FILE


def setup_logging(name: str, log_level=logging.INFO):
    """
    Setup logging configuration.
    
    Args:
        name: Logger name
        log_level: Logging level
        
    Returns:
        Configured logger instance
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # File handler
    fh = logging.FileHandler(
        LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    fh.setLevel(log_level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


class ProcessingLogger:
    """Context manager for logging processing operations."""
    
    def __init__(self, step_name: str):
        self.step_name = step_name
        self.logger = setup_logging(step_name.replace(" ", "_"))
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting: {self.step_name}")
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        if exc_type:
            self.logger.error(f"Error in {self.step_name}: {exc_val}")
        else:
            self.logger.info(f"Completed {self.step_name} in {duration:.2f}s")
