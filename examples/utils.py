import logging
import os
from string import Template


def log_config(debug: bool = False):
    # Define log format
    default_formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    default_handler = logging.StreamHandler()
    default_handler.setFormatter(default_formatter)
    logging.basicConfig(
        handlers=[default_handler],
        level=logging.DEBUG if debug else logging.INFO
    )

    # Disable aioredlock.redis logger
    logging.getLogger('aioredlock.redis').disabled = True


redis = [
    Template('rediss://:${redis_password}@${redis_host}:${redis_port}').substitute(
        redis_password=os.environ['REDIS_SERVER_PASSWORD'],
        redis_host=os.environ['REDIS_HOST'],
        redis_port=os.environ['REDIS_PORT']
    )
]
