"""
Logging utilities for the demo chatbot.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

from demo_chatbot.config.settings import settings


def setup_logger(
    name: str = "demo_chatbot",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup and configure logger."""
    
    # Use settings if not provided
    log_level = level or settings.LOG_LEVEL
    log_file_path = log_file or settings.LOG_FILE
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler with rich
    console = Console()
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        rich_tracebacks=True
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log file is specified
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logger()