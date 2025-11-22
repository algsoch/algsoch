"""Utility functions for AI engine."""

import os
from typing import Any, Dict
import json


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to file."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def ensure_dir(directory: str) -> None:
    """Ensure directory exists."""
    os.makedirs(directory, exist_ok=True)


class Logger:
    """Simple logger for AI operations."""
    
    def __init__(self, name: str):
        self.name = name
    
    def info(self, message: str) -> None:
        """Log info message."""
        print(f"[{self.name}] INFO: {message}")
    
    def error(self, message: str) -> None:
        """Log error message."""
        print(f"[{self.name}] ERROR: {message}")
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        print(f"[{self.name}] WARNING: {message}")
