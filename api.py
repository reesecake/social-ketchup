from flask import Flask, render_template
# from blueprints.authentication import authenticationController
from flask_socketio import SocketIO
# from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.register_blueprint(authenticationController)
# socketio = SocketIO(app)
socketio = SocketIO(app)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/chat")
def render_chat():
    return render_template('social.html')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))

if __name__ == "__main__":
    socketio.run(app, debug=True)
