from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    """
    Show a random video.
    """
    return "Oh, hi there."


if __name__ == '__main__':
    app.run()