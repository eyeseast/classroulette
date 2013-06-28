#!/usr/bin/env python
"""
The main app. This runs everything.
"""
import os
import urlparse

from flask import Flask, render_template, redirect, url_for
from flaskext.markdown import Markdown

from connection import redis, key
from youtube import get_video_id, get_video

# the app itself
app = Flask(__name__)
app.debug = bool(os.environ.get('DEBUG', False))

# addons
Markdown(app)

@app.route('/')
def index():
    """
    Show a random video, pulled from our redis set.
    """
    user, id = redis.srandmember(key()).split(':')
    return redirect(url_for('video', user=user, id=id))

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
    video = get_video(user, id)
    video.id = get_video_id(video.link)

    return render_template('video.html', video=video)


if __name__ == '__main__':
    app.run(debug=True)