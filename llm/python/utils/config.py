"""
Configuration loader for Minecraft RL system.
Loads and manages configuration from rl_config.yaml
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for RL system"""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration

        Args:
            config_path: Path to config YAML file. If None, uses default path
        """
        if config_path is None:
            # Default to rl_config.yaml in config directory
            config_dir = Path(__file__).parent.parent.parent / "config"
            config_path = config_dir / "rl_config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Expand relative paths
        self._expand_paths(config)
        return config

    def _expand_paths(self, config: Dict[str, Any]):
        """Expand relative paths to absolute paths"""
        base_dir = Path(__file__).parent.parent.parent

        # Memory database path
        if 'memory' in config and 'long_term' in config['memory']:
            db_path = config['memory']['long_term'].get('database_path')
            if db_path and not os.path.isabs(db_path):
                config['memory']['long_term']['database_path'] = str(base_dir / db_path)

        # Craft discovery database
        if 'craft_discovery' in config:
            db_path = config['craft_discovery'].get('database_path')
            if db_path and not os.path.isabs(db_path):
                config['craft_discovery']['database_path'] = str(base_dir / db_path)

        # Logging directories
        if 'logging' in config:
            for log_type in ['tensorboard', 'file']:
                if log_type in config['logging']:
                    log_dir = config['logging'][log_type].get('log_dir')
                    if log_dir and not os.path.isabs(log_dir):
                        if log_type == 'tensorboard':
                            config['logging']['tensorboard']['log_dir'] = str(base_dir / log_dir)
                        else:
                            config['logging']['file']['log_dir'] = str(base_dir / log_dir)

        # Checkpointing
        if 'checkpointing' in config:
            save_dir = config['checkpointing'].get('save_dir')
            if save_dir and not os.path.isabs(save_dir):
                config['checkpointing']['save_dir'] = str(base_dir / save_dir)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated key

        Args:
            key: Dot-separated key (e.g., 'agent.learning_rate')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value by dot-separated key

        Args:
            key: Dot-separated key (e.g., 'agent.learning_rate')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self, path: str = None):
        """
        Save configuration to YAML file

        Args:
            path: Path to save config. If None, uses original path
        """
        save_path = path or self.config_path

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access"""
        return self.get(key)

    def __setitem__(self, key: str, value: Any):
        """Allow dictionary-style assignment"""
        self.set(key, value)

    # Convenience methods for common config sections

    @property
    def env_config(self) -> Dict[str, Any]:
        """Get environment configuration"""
        return self.config.get('environment', {})

    @property
    def agent_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.config.get('agent', {})

    @property
    def training_config(self) -> Dict[str, Any]:
        """Get training configuration"""
        return self.config.get('training', {})

    @property
    def memory_config(self) -> Dict[str, Any]:
        """Get memory configuration"""
        return self.config.get('memory', {})

    @property
    def reward_config(self) -> Dict[str, Any]:
        """Get reward configuration"""
        return self.config.get('rewards', {})

    @property
    def craft_discovery_config(self) -> Dict[str, Any]:
        """Get craft discovery configuration"""
        return self.config.get('craft_discovery', {})

    @property
    def bridge_config(self) -> Dict[str, Any]:
        """Get bridge configuration"""
        return self.config.get('bridge', {})


# Global config instance
_config = None


def get_config(config_path: str = None) -> Config:
    """
    Get global configuration instance

    Args:
        config_path: Path to config file (only used on first call)

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reload_config(config_path: str = None) -> Config:
    """
    Reload configuration from file

    Args:
        config_path: Path to config file

    Returns:
        New Config instance
    """
    global _config
    _config = Config(config_path)
    return _config
