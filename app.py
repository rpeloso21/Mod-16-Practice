from web_socket_server import WebScoketServer, socketio, app
from flask import render_template
import json

app = WebScoketServer().create_app()
message_storage = {}
test = "test"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnect')

@socketio.on('message')
def handle_message(message):
    data = json.loads(message)
    user = data['user']
    msg = data['message']

    if user not in message_storage:
        message_storage[user] = []

    message_storage[user].append(msg)
    print(f"Received message: {message}.")
    socketio.emit('message', message)

@socketio.on('get_user_messages')
def handle_get_user_messages(data):
    user_input = json.loads(data)
    user = user_input['user']

    if user in message_storage:
        message_list = message_storage[user]
    else:
        message_list = "User not found"

    socketio.emit('get_user_messages', message_list)

@app.route('/')
def index():
    return render_template('WebSocketClients.html')

if __name__ == "__main__":
    socketio.run(app)

