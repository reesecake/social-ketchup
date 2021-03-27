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

from app import routes
from blueprints.authentication import authenticationController
import models

app.register_blueprint(authenticationController)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
