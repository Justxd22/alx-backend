#!/usr/bin/env python3
"""Flask Application."""
from flask import Flask, render_template, make_response, jsonify, request, g
from flask_babel import Babel, format_datetime
import pytz
import datetime

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
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.errorhandler(404)
def not_found(error):
    """404 Error.

    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


@babel.localeselector
def get_locale():
    """Choose the best match language."""
    priority = [
        request.args.get('locale'),
        g.user.get('locale', None) if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        Config.BABEL_DEFAULT_LOCALE
    ]
    for locale in priority:
        if locale and locale in Config.LANGUAGES:
            return locale

@babel.timezoneselector
def get_timezone():
    """Choose timezone."""
    priority = [
        request.args.get('timezone'),
        g.user.get('timezone', None) if g.user else None,
        Config.BABEL_DEFAULT_TIMEZONE
    ]
    for timezone in priority:
        try:
            if timezone and pytz.timezone(timezone).zone:
                return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass


def get_user():
    """Get user from dict."""
    user = request.args.get('login_as')
    if user:
        return users.get(int(user))
    return None


@app.before_request
def before_request() -> None:
    """Things to run before response."""
    setattr(g, 'user', get_user())
    setattr(g, 'time', format_datetime(datetime.datetime.now()))


@app.route('/')
def hello_world():
    """Root Handle."""
    return render_template('index.html')


if __name__ == "__main__":
    """Main Function."""
    app.run(threaded=True)
