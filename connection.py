"""
Container module so one redis instance and connection pool
can be imported from different places in the app.
"""
import os
import urlparse

import feedparser
from redis import StrictRedis

DEFAULT_URL = "redis://localhost:6379/0"
REDIS_URL = os.environ.get('REDIS_URL', DEFAULT_URL)

KEY = "roulette:videos"

# one connection to rule them all
redis = StrictRedis.from_url(REDIS_URL)


def key(uid=None):
    """
    Make a simple redis key
    """
    if uid:
        return KEY + ':' + uid
    return KEY


def get_video_id(url):
    """
    Extract YouTube video ID from a URL.
    """
    parts = urlparse.urlparse(url)
    qs = urlparse.parse_qs(parts.query)

    if qs.get('v'):
        return qs['v'][0]


def get_video(user, vid):
    """
    Fetch video details from the YouTube v2 API.
    """
    url = "https://gdata.youtube.com/feeds/api/users/%(user)s/uploads/%(vid)s" % {
        'user': user,
        'vid': vid
    }

    video = feedparser.parse(url)
    if video.entries:
        video = video.entries[0]

    return video
