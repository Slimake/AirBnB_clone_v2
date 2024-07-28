#!/usr/bin/python3
"""
1-hello_route Module
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """Route for Homepage"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Route for hbnb"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
