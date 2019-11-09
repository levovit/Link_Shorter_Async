from pathlib import Path
import yaml


def load_config(config_file=None):
    default_file = Path(__file__).parent / 'config.yaml'
    with open(default_file) as f:
        config = yaml.safe_load(f)

    config_dict = {}
    if config_file:
        config_dict = yaml.safe_load(config_file)
    config.update(**config_dict)

    return config
