"""
Structured logging system for Minecraft RL agent.
Supports both console and file logging with JSON/text formats.
"""

import logging
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import contextmanager

from .config import get_config


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        return json.dumps(log_data)


class Logger:
    """
    Structured logger for Minecraft RL system
    """

    _loggers: Dict[str, logging.Logger] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize logging system"""
        if cls._initialized:
            return

        config = get_config()

        # Get logging configuration
        log_level = config.get('logging.level', 'INFO')
        log_format = config.get('logging.format', 'json')
        file_enabled = config.get('logging.file.enabled', True)
        file_log_dir = config.get('logging.file.log_dir', './data/logs')
        max_size = config.get('logging.file.max_size', '10MB')
        backup_count = config.get('logging.file.backup_count', 5)

        # Create log directory
        log_dir = Path(file_log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))

        # Clear existing handlers
        root_logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)

        if log_format == 'json':
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )

        root_logger.addHandler(console_handler)

        # File handler with rotation
        if file_enabled:
            from logging.handlers import RotatingFileHandler

            # Parse max_size (e.g., "10MB")
            size_bytes = cls._parse_size(max_size)

            file_handler = RotatingFileHandler(
                log_dir / 'minecraft_rl.log',
                maxBytes=size_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )

            if log_format == 'json':
                file_handler.setFormatter(JSONFormatter())
            else:
                file_handler.setFormatter(
                    logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
                )

            root_logger.addHandler(file_handler)

        cls._initialized = True

    @classmethod
    def _parse_size(cls, size_str: str) -> int:
        """
        Parse size string (e.g., "10MB") to bytes

        Args:
            size_str: Size string

        Returns:
            Size in bytes
        """
        size_str = size_str.upper().strip()

        multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024,
        }

        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                number = size_str[:-len(suffix)]
                try:
                    return int(float(number) * multiplier)
                except ValueError:
                    break

        # Default to bytes if no suffix
        try:
            return int(size_str)
        except ValueError:
            return 10 * 1024 * 1024  # Default 10MB

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create logger with specified name

        Args:
            name: Logger name (typically __name__ of module)

        Returns:
            Logger instance
        """
        if not cls._initialized:
            cls.initialize()

        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)

        return cls._loggers[name]

    @classmethod
    @contextmanager
    def context(cls, **kwargs):
        """
        Context manager for adding contextual information to logs

        Args:
            **kwargs: Contextual key-value pairs

        Example:
            with Logger.context(episode_id=123, step=456):
                logger.info("Action executed")
        """
        # Add context to all log records
        old_factory = logging.getLogRecordFactory()

        def record_factory(*args, **factory_kwargs):
            record = old_factory(*args, **factory_kwargs)
            record.extra = kwargs
            return record

        logging.setLogRecordFactory(record_factory)

        try:
            yield
        finally:
            logging.setLogRecordFactory(old_factory)


# Convenience functions

def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return Logger.get_logger(name)


def log_episode_start(logger: logging.Logger, episode_id: int, info: Dict[str, Any]):
    """Log episode start"""
    logger.info(f"Episode {episode_id} started", extra={'extra': info})


def log_episode_end(logger: logging.Logger, episode_id: int, info: Dict[str, Any]):
    """Log episode end"""
    logger.info(f"Episode {episode_id} ended", extra={'extra': info})


def log_step(logger: logging.Logger, episode_id: int, step: int, info: Dict[str, Any]):
    """Log step"""
    logger.debug(f"Episode {episode_id}, Step {step}", extra={'extra': info})


def log_craft_discovery(logger: logging.Logger, recipe: Dict[str, Any]):
    """Log craft discovery"""
    logger.info(f"New recipe discovered: {recipe}", extra={'extra': recipe})


def log_reward(logger: logging.Logger, reward: float, info: Dict[str, Any]):
    """Log reward"""
    logger.debug(f"Reward: {reward:.2f}", extra={'extra': info})


def log_error(logger: logging.Logger, error: Exception, context: Dict[str, Any] = None):
    """Log error with context"""
    extra = {'extra': context} if context else {}
    logger.error(f"Error: {str(error)}", exc_info=True, extra=extra)
