#!/usr/bin/env python
"""
Pull in YouTube videos from a list of feeds and store them in redis.
"""
import feedparser
import logging

from connection import redis, key
from youtube import get_video_id, get_feed_url

log = logging.getLogger(__file__)
 

def update():
    """
    Do the update.
    """
    with open('./feeds.txt') as f:
        feeds = [line.strip() for line in f]

    for user in feeds:
        url = get_feed_url(user)
        feed = feedparser.parse(url)

        for video in feed.entries:

            # get the video id from the URL
            vid = get_video_id(video.link)

            # save the username and video id as a key-value pair
            # in our set, so we have both available later
            uid = '%s:%s' % (user, vid)

            # save the uid to our redis set
            # printing the video title if it's added to the set
            if redis.sadd(key(), uid):
                print video.title

    print "Total videos: %i" % redis.scard(key())


if __name__ == '__main__':
    update()
