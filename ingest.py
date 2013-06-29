#!/usr/bin/env python
"""
Pull in YouTube videos from a list of feeds and store them in redis.
"""
import csv
import urllib2

import feedparser

from connection import redis, key
from youtube import get_video_id, get_feed_url

FEEDS_URL = "https://docs.google.com/spreadsheet/pub?" \
    "key=0AprNP7zjIYS1dDFwS3BCRExNVERzVkpVVENacXd1ekE&single=true&gid=0&output=csv"


def update():
    """
    Do the update. Feeds can be for a YouTube user,
    or for a specific feed, like a playlist.
    """
    with open('./feeds.txt') as f:
        feeds = [line.strip() for line in f]

    resp = urllib2.urlopen(FEEDS_URL)
    reader = csv.DictReader(resp)

    for row in reader:
        # get the user or alternate feed
        user = row['User']
        url = row['Feed'] or get_feed_url(user)
                
        # parse whichever we have
        feed = feedparser.parse(url)

        for video in feed.entries:

            # get the video id from the URL
            # there are other ways, but this always works
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
