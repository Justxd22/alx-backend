#!/usr/bin/python3
"""Flask Application."""
from flask import Flask, render_template, make_response, jsonify
from flask_babel import Babel


class Config:
    """Babel Config class."""

    JSONIFY_PRETTYPRINT_REGULAR = True
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@app.errorhandler(404)
def not_found(error):
    """404 Error.

    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


@app.route('/')
def hello_world():
    """Root Handle."""
    return render_template('0-index.html')


if __name__ == "__main__":
    """Main Function."""
    app.run(threaded=True)