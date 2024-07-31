#!/usr/bin/python3
"""
7-states_list Module
"""
from flask import Flask, render_template
from models import storage, classes

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database again at the end of the request"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Display a HTML page"""
    states = [s for s in storage.all(classes['State']).values()]

    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
