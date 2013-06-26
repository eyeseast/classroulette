#!/usr/bin/env python
"""
The main app. This runs everything.
"""
import urlparse
from flask import Flask, render_template
from oembed import DefaultOEmbedConsumer as o

from connection import redis, key

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    """
    Show a random video, pulled from our redis set.
    """
    url = redis.srandmember(key())
    video = o.embed(url).getData()
    video['url'] = url
    video['id'] = get_video_id(url)

    return render_template('video.html', video=video)


def get_video_id(url):
    """
    Extract YouTube video ID from a URL.
    """
    parts = urlparse.urlparse(url)
    qs = urlparse.parse_qs(parts.query)

    if qs.get('v'):
        return qs['v'][0]


if __name__ == '__main__':
    app.run()