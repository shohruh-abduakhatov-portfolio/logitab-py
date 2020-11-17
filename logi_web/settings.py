import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent

dev_config_path = BASE_DIR / 'conf' / 'conf.yaml'

prod_config_path = BASE_DIR / 'conf' / 'prod.yaml'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


def load_conf(debug):
    if not debug:
        return get_config(prod_config_path)
    else:
        return get_config(dev_config_path)


config = get_config(dev_config_path)