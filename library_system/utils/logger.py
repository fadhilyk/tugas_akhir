"""
Logging configuration untuk Library Management System.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logger(name: str = "library_system", log_dir: str = "logs") -> logging.Logger:
    """
    Setup logger dengan rotating file handler.
    
    Args:
        name: Nama logger
        log_dir: Direktori untuk menyimpan log files
        
    Returns:
        Configured logger instance
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
    
    log_file = log_path / "library.log"
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_action(logger: logging.Logger, action: str, details: str, user: Optional[str] = None) -> None:
    """
    Log action dengan format konsisten.
    
    Args:
        logger: Logger instance
        action: Jenis action (LOGIN, LOGOUT, ADD_BOOK, dll)
        details: Detail action
        user: Username yang melakukan action (optional)
    """
    if user:
        logger.info(f"[{action}] User: {user} | {details}")
    else:
        logger.info(f"[{action}] {details}")


def log_error(logger: logging.Logger, error: Exception, context: str) -> None:
    """
    Log error dengan context.
    
    Args:
        logger: Logger instance
        error: Exception yang terjadi
        context: Context dimana error terjadi
    """
    logger.error(f"[ERROR] {context} | {type(error).__name__}: {str(error)}")
