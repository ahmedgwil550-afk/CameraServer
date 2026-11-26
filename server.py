import eventlet
eventlet.monkey_patch()
import os
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/device')
def device_connect():
    print("[+] Phone Connected!")
    socketio.emit('device_status', {'status': 'online'}, namespace='/dashboard')

@socketio.on('disconnect', namespace='/device')
def device_disconnect():
    print("[-] Phone Disconnected")
    socketio.emit('device_status', {'status': 'offline'}, namespace='/dashboard')

@socketio.on('frame', namespace='/device')
def handle_frame(data):
    socketio.emit('frame', data, namespace='/dashboard')

if __name__ == '__main__':
    # Render يعطيك بورت تلقائي، لازم نستخدمه
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)