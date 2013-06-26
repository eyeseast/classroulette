#!/usr/bin/env python
"""
Pull in YouTube videos from a list of feeds and store them in redis.
"""
import feedparser
import logging

from connection import redis, key

URL = "http://gdata.youtube.com/feeds/base/users/%(user)s/uploads?" \
      "alt=rss&v=2&orderby=published&client=ytapi-youtube-profile"

log = logging.getLogger(__file__)

def update():
    """
    Do the update.
    """
    with open('./feeds.txt') as f:
        feeds = [line.strip() for line in f]

    for user in feeds:
        url = URL % {'user': user}
        feed = feedparser.parse(url)

        for video in feed.entries:
            redis.sadd(key(), video.link)
            print video.title, video.link


if __name__ == '__main__':
    update()
