"""
Utilities for dealing with the YouTube v2 API
"""
import logging
import urllib
import urlparse

import feedparser

EDU_CATEGORIES = "http://gdata.youtube.com/schemas/2007/educategories.cat"

log = logging.getLogger(__name__)

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


def get_courses(category_id):
    """
    Fetch courses for a given category.
    """
    params = {
        'v': 2,
        'category': category_id,
        'max-results': 50,
        'hl': 'en'
    }
    base = "http://gdata.youtube.com/feeds/api/edu/courses?"
    url = base + urllib.urlencode(params)
    courses = feedparser.parse(url)
    log.debug('Fetched courses: %s', courses.feed.get('title', category_id))
    return courses.entries


def get_lectures(course_id):
    """
    Get lectures for a given course.
    """
    params = {
        'v': 2, # v2 API
        'course': course_id,
        'max-results': 50,
        'hl': 'en' # english only, for now
    }
    base = "http://gdata.youtube.com/feeds/api/edu/lectures?"
    url = base + urllib.urlencode(params)
    lectures = feedparser.parse(url)
    log.debug('Fetched %i lectures: %s', len(lectures.entries), lectures.get('title', course_id))
    return lectures.entries


def get_edu_tags():
    """
    Get a list of tags for YouTube EDU.
    """
    cats = feedparser.parse(EDU_CATEGORIES)
    tags = cats.feed.tags
    return tags


