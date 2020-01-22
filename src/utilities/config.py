"""
Methods to read config files.
"""
from typing import Any, Dict

import yaml


def load_config(file_name: str) -> Dict[str, Any]:
    """
    Load configuration file, either YAML or JSON.
    :param file_name: Path to file
    :return: Dict
    """
    with open(file_name, 'r') as file_stream:
        return yaml.load(file_stream.read(), Loader=yaml.SafeLoader)
