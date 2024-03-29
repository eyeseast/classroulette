#!/usr/bin/env python
"""
The main app. This runs everything.
"""
import datetime
import os
import urlparse

from flask import Flask, redirect, render_template, request, url_for
from flaskext.markdown import Markdown

from connection import redis, key
from youtube import get_video_id, get_video

# constants
REDIRECT_HOSTS = {
    'class-roulette.herokuapp.com': 'www.classroulette.co'
}

# the app itself
app = Flask(__name__)
app.debug = bool(os.environ.get('DEBUG', False))

# addons
Markdown(app)

# middleware

@app.before_request
def redirect_host():
    """
    Redirect hosts if necessary. Useful for Heroku.
    """
    host = request.host
    if host in REDIRECT_HOSTS:
        url = request.url
        dest = REDIRECT_HOSTS[host]
        dest = url.replace(host, dest)

        return redirect(dest, 301)

def get_random_video():
    """
    Get a random video, pulled from our redis set.

    For stats, increment each video in a sorted set.
    By doing this here, we're checking the randomness
    of videos returned from redis, not the popularity
    of shared videos.
    """
    # get a random video
    uid = redis.srandmember(key())
    user, id = uid.split(':')

    # store stats
    with redis.pipeline() as pipe:
        pipe.zincrby(key('stats'), uid, 1)
        pipe.zincrby(key('stats:users'), user, 1)
        pipe.execute()

    # send us along
    return url_for('video', user=user, id=id)

@app.route('/')
def index():
    """
    Redirect to a random video.
    """
    url = get_random_video()
    return redirect(url)

#@app.route('/<user>')
def channel(user):
    """
    Show videos from one channel.
    """

@app.route('/<user>/<id>')
def video(user, id):
    """
    Show a video.
    """
    video = get_video(id)
    video.id = get_video_id(video.link)

    if getattr(video, 'yt_duration'):
        video.duration = datetime.timedelta(
            seconds=int(video.yt_duration.get('seconds', 0)))

    next = get_random_video()
    return render_template('video.html', video=video, next=next)


if __name__ == '__main__':
    app.run(debug=True)