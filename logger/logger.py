import logging.config

import yaml

import logging

with open('./logger/logging.yaml', 'r') as f:
    print("configuration happends")
    config = yaml.safe_load(f.read())

    logging.config.dictConfig(config)


def get_logger(name: str):
    return logging.getLogger(name)
