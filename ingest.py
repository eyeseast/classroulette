#!/usr/bin/env python
"""
Pull in YouTube videos from a list of feeds and store them in redis.
"""
from gevent import monkey
monkey.patch_all()

import argparse
import csv
import logging
import urllib
import urllib2

import feedparser
import gevent

from connection import redis, key
from youtube import get_video_id, get_feed_url, get_edu_tags, get_courses, get_lectures

# hard-coding this for now
# should be able to change this for a different sort of roulette
FEEDS_URL = "https://docs.google.com/spreadsheet/pub?" \
    "key=0AprNP7zjIYS1dDFwS3BCRExNVERzVkpVVENacXd1ekE&single=true&gid=0&output=csv"

log = logging.getLogger(__file__)

def ingest_edu():
    """
    Pull in categories and feeds from YouTube EDU.
    """
    print "Fetching tags..."
    tags = get_edu_tags()

    # get all courses, using greenlets
    print "Fetching course lists..."
    tag_list = [gevent.spawn(get_courses, tag['term']) for tag in tags]
    gevent.joinall(tag_list)

    # each course_list is a list of courses
    for course_list in tag_list:
        # walk down the list
        # get all lectures for this course list
        courses = [gevent.spawn(get_lectures, c.yt_playlistid) for c in course_list.value]
        gevent.joinall(courses)

        # each lect_list is a list of lectures
        for lect_list in courses:
            # now we can loop through lect_list for videos
            for video in lect_list.value:
                # do something interesting
                store_video(video)

    print "Total videos: %i" % redis.scard(key())


def update():
    """
    Do the update. Feeds can be for a YouTube user,
    or for a specific feed, like a playlist.
    """
    print "Updating feeds..."
    resp = urllib2.urlopen(FEEDS_URL)
    reader = csv.DictReader(resp)

    for row in reader:
        # get the user or alternate feed
        user = row['User']
        url = row['Feed'] or get_feed_url(user)
                
        # parse whichever we have
        feed = feedparser.parse(url)

        for video in feed.entries:
            store_video(video)

    print "Total videos: %i" % redis.scard(key())


def store_video(video):
    """
    Store a video in a redis set.
    """
    # get the video id from the URL
    # there are other ways, but this always works
    vid = get_video_id(video.link)

    # save the username and video id as a key-value pair
    # in our set, so we have both available later
    uid = '%s:%s' % (video.author, vid)

    # save the uid to our redis set
    # printing the video title if it's added to the set
    if redis.sadd(key(), uid):
        log.info(video.title)

# arg parsing
parser = argparse.ArgumentParser()
parser.add_argument('source', default='feeds', nargs='?')
parser.add_argument('-l', '--log-level', dest='loglevel', default='INFO')

if __name__ == '__main__':
    args = parser.parse_args()
    level = getattr(logging, args.loglevel.upper())
    logging.basicConfig(level=level)

    if args.source == "edu":
        ingest_edu()
    else:
        update()
