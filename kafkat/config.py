"""Configuration management for Kafkat."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for Kafkat."""
    
    DEFAULT_CONFIG = {
        "bootstrap_servers": "localhost:9092",
        "auto_commit": True,
        "auto_offset_reset": "earliest",
        "separator": ",",
        "prettify": False,
        "timeout_ms": 10000,
        "max_messages": 1000,
        "consumer_timeout_ms": 5000
    }
    
    def __init__(self):
        self.config_file = Path.home() / ".kafkat" / "config.json"
        self._config = self.DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        self.config_file.parent.mkdir(exist_ok=True)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def update(self, **kwargs) -> None:
        """Update multiple configuration values."""
        self._config.update(kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()
