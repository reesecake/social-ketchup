from flask import Flask, render_template
from blueprints.authentication import authenticationController
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(authenticationController)
# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode='eventlet')
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', {'data': 42})

@app.route("/chat", methods=["GET"])
def render_chat():
    return render_template('social.html')

if __name__ == "__main__":
    socketio.run(app)
    app.run(debug=True, host='0.0.0.0')
    
