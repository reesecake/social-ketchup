from flask import Flask
from blueprints.authentication import authenticationController
app = Flask(__name__)
app.register_blueprint(authenticationController)

from app import routes

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = 5000, debug=True)