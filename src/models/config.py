from pathlib import Path
import yaml

here = Path(__file__).resolve().parents[2] #gets a parent dir 2 levels up
with open(here / './config.yaml', 'r') as stream:
    config_dict = yaml.safe_load(stream)


class Struct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Struct(**value)
            else:
                self.__dict__[key] = value


settings = Struct(**config_dict)
