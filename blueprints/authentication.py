from flask import Blueprint

authenticationController = Blueprint("authentication", __name__)

@authenticationController.route("/signup", methods=["GET"])
def signup():
    return "Hello World"
