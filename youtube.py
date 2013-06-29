"""
Utilities for dealing with the YouTube v2 API
"""

import urlparse

import feedparser

def get_feed_url(user):
    """
    Get a feed URL for a user. Specify the v2 API.
    """
    URL = "http://gdata.youtube.com/feeds/base/users/%(user)s/uploads?v=2"
    return URL % {'user': user}


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


def get_video_id(url):
    """
    Extract YouTube video ID from a URL.
    """
    parts = urlparse.urlparse(url)
    qs = urlparse.parse_qs(parts.query)

    if qs.get('v'):
        return qs['v'][0]

