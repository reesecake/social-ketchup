import uuid
from collections import deque

from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user
from flask_socketio import emit, join_room, close_room

from api import socketio

chatController = Blueprint("chat", __name__)

queue = deque([])


@chatController.route("/chat")
def render_chat():
    if current_user.is_anonymous:
        flash('You need to be logged in to chat.')
        return redirect(url_for('index'))

    return render_template('social.html')


@socketio.on('message')
def message(data, methods=['GET', 'POST']):
    print(data)
    room_id = data['room']
    emit('message', data['message'], room=room_id, include_self=False)


@socketio.on('pair me')
def pairIfPossible(data, methods=['GET', 'POST']):
    # data = json.loads(data)
    if queue:
        # we found a match
        waiting_user, room_id = queue.popleft()
        # Todo - waiting_user != data['username'] --> enqueue again
        join_room(room_id)
        info = {'p1': waiting_user, 'p2': data['username'], 'room_id': room_id}
        emit('introduction', info, room=room_id, json=True)
    else:
        # keep user in waiting queue
        room_id = str(uuid.uuid4())
        join_room(room_id)
        queue.append((data['username'], room_id))

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
