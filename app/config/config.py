import os
import yaml
from typing import Dict, Any


def load_yaml_config(config_path: str, 
                     key: str = "default") -> Dict[str, Any]:
    """Load 'key' configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get(key, {})