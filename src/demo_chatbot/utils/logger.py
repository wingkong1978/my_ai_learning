"""
Logging utilities for the demo chatbot.

Provides comprehensive logging functionality with:
- Rich console output with color coding
- File logging with rotation support
- Performance monitoring
- Context-aware logging
"""

import logging
import logging.handlers
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager

from rich.logging import RichHandler
from rich.console import Console
from rich.traceback import install

# Install rich tracebacks globally
install(show_locals=True)

try:
    from ..config.settings import get_settings
except ImportError:
    # Fallback for direct execution
    class MockSettings:
        log_level = "INFO"
        log_file = None
        working_directory = Path(".")
        debug = False
    
    def get_settings():
        return MockSettings()


def setup_logger(
    name: str = "demo_chatbot",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup and configure logger with enhanced features.
    
    Args:
        name: Logger name
        level: Log level override
        log_file: Log file path override
        
    Returns:
        Configured logger instance
    """
    try:
        settings = get_settings()
        log_level = level or getattr(settings, "log_level", "INFO")
        log_file_path = log_file or getattr(settings, "log_file", None)
    except Exception:
        log_level = level or "INFO"
        log_file_path = log_file
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Convert string log level to logging constant
    if isinstance(log_level, str):
        log_level = getattr(logging, log_level.upper(), logging.INFO)
    else:
        log_level = getattr(logging, str(log_level).upper(), logging.INFO)
    
    logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    logger.propagate = False
    
    # Setup console handler
    console = Console(stderr=True)  # Use stderr for logging
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=True,
        rich_tracebacks=True,
        markup=True,
        log_time_format="[%X]",
    )
    
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Setup file handler with rotation if specified
    if log_file_path:
        try:
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                filename=str(log_file_path),
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
            
            file_formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            # Fallback to console logging if file setup fails
            logger.warning(f"Failed to setup file logging: {e}")
    
    return logger


@contextmanager
def log_performance(logger: logging.Logger, operation: str, **extra_fields):
    """Context manager for performance logging.
    
    Args:
        logger: Logger instance
        operation: Name of the operation being measured
        **extra_fields: Additional fields to include in log
    """
    start_time = time.time()
    
    try:
        logger.info(f"Starting operation: {operation}")
        yield
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Operation failed: {operation} (duration: {duration:.3f}s) - {e}")
        raise
    
    else:
        duration = time.time() - start_time
        logger.info(f"Operation completed: {operation} (duration: {duration:.3f}s)")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with consistent configuration.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def configure_third_party_loggers() -> None:
    """Configure third-party library loggers to reduce noise."""
    # Reduce noise from common libraries
    noisy_loggers = [
        "urllib3",
        "requests",
        "asyncio",
        "httpx",
        "openai",
        "langchain"
    ]
    
    for logger_name in noisy_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)


# Setup global logger configuration
def setup_global_logging() -> None:
    """Setup global logging configuration."""
    # Configure third-party loggers
    configure_third_party_loggers()
    
    # Setup root logger
    root_logger = setup_logger("demo_chatbot")
    
    # Log startup information
    root_logger.info("Demo Chatbot logging system initialized")
    
    try:
        settings = get_settings()
        root_logger.debug(f"Log level: {getattr(settings, 'log_level', 'INFO')}")
        
        if hasattr(settings, "log_file") and settings.log_file:
            root_logger.debug(f"Log file: {settings.log_file}")
    except Exception:
        root_logger.debug("Settings not available during logger setup")


# Global logger instance with enhanced configuration
logger = setup_logger()

# Initialize global logging configuration
if __name__ != "__main__":
    try:
        setup_global_logging()
    except Exception:
        pass  # Silently ignore setup errors during import