import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
dbmongo = MongoEngine(app)
bootstrap = Bootstrap(app)

from flask_socketio import SocketIO

socketio = SocketIO(app)

from app import routes
from blueprints.authentication import authenticationController
from blueprints.chat import chatBlueprint
import models

app.register_blueprint(authenticationController)
app.register_blueprint(chatBlueprint)

# Todo: Same user enqueued problem -- email matching?
# Todo(DONE): empty message being sent -- bugfix
# Todo(DONE): scrollable div with autoscroll to bottom

# Todo: Add specific university support

# Reese is -- adding auth for chat route
# Todo: give unique identities to clients
# Making the scrolling look normal


if __name__ == "__main__":
    socketio.run(app, port=int(os.environ.get('PORT', '5000')))
