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
from blueprints.chat import chatController
import models

app.register_blueprint(authenticationController)
app.register_blueprint(chatController)


## Same user enqueued problem -- email matching? 
## Next functionality

if __name__ == "__main__":
    socketio.run(app, debug=True)
