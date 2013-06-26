"""
Container module so one redis instance and connection pool
can be imported from different places in the app.
"""
import os
from redis import StrictRedis

DEFAULT_URL = "redis://localhost:6379/0"
REDIS_URL = os.environ.get('REDIS_URL', DEFAULT_URL)

KEY = "roulette:videos"

def key(uid=None):
    """
    Make a simple redis key
    """
    if uid:
        return KEY + ':' + uid
    return KEY

# one connection to rule them all
redis = StrictRedis.from_url(REDIS_URL)