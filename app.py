#!/usr/bin/env python
"""
The main app. This runs everything.
"""
import os
import urlparse

from flask import Flask, render_template
from flaskext.markdown import Markdown

from connection import redis, key, get_video_id, get_video

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
    user, vid = redis.srandmember(key()).split(':')
    video = get_video(user, vid)
    video.id = get_video_id(video.link)

    return render_template('video.html', video=video)


if __name__ == '__main__':
    app.run(debug=True)