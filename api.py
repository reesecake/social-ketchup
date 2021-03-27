from flask import Flask, render_template
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
import models

app.register_blueprint(authenticationController)

@app.route("/chat")
def render_chat():
    return render_template('social.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, debug=True)
