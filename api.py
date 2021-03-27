from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
dbmongo = MongoEngine(app)
bootstrap = Bootstrap(app)

from flask_socketio import SocketIO, join_room, leave_room, send, emit, rooms, close_room
socketio = SocketIO(app)
from collections import deque
import uuid
import json
from app import routes
from blueprints.authentication import authenticationController
import models

app.register_blueprint(authenticationController)


queue = deque([])


## Same user enqueued problem -- email matching? 
## Next functionality


@app.route("/chat")
def render_chat():
    return render_template('social.html')


@socketio.on('message')
def message(data, methods=['GET', 'POST']):
    print(data)
    room_id = data['room']
    emit('message', data['message'], room=room_id, include_self=False)



@socketio.on('pair me')
def pairIfPossible(data, methods=['GET', 'POST']):
    #data = json.loads(data)
    if queue:
        #we found a match
        waiting_user, room_id = queue.popleft()
        # Todo - waiting_user != data['username'] --> enqueue again
        join_room(room_id)
        info = {'p1':waiting_user, 'p2':data['username'], 'room_id':room_id}
        emit('introduction', info, room=room_id, json = True)
    else:
        #keep user in waiting queue
        room_id = str(uuid.uuid4())
        join_room(room_id)
        queue.append((data['username'],room_id))
    
    print(queue)


@socketio.on('client disconnecting')
def disconnect_details(data):
    print(data)
    room_id = data['room']
    emit('partner disconnected', room=room_id, include_self=False)
    close_room(room_id)


@socketio.on('disconnect')
def test_disconnect():
    print("Client has disconnected!")



    



if __name__ == "__main__":
    socketio.run(app, debug=True)
