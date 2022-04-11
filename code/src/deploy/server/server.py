from flask import Flask, request, jsonify, render_template
from flask_socketio import emit
from flask_socketio import SocketIO
from flask_ngrok import run_with_ngrok
# Bibliografía.
# https://stackoverflow.com/questions/51970072/real-time-video-stabilization-opencv

app = Flask(__name__, template_folder = "templates")

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
sensors = None

class Server:
    def __init__(self, sensors, port=5000):
        self.port = port
        self.sensors = sensors
        

    def start_server(self):
        # app.run(port=self.port, debug=True)
        global sensors
        sensors = self.sensors
        run_with_ngrok(socketio.run(app, host='0.0.0.0', port = self.port, debug=True))
        sensors.start_reading()


@socketio.on("get_sensors")
def get_sensors(data):
    try: 
        sensor_data = sensors.read_sensors()
        print("Serial received: " + str(sensor_data))
        emit('receive_sensors', sensor_data)
    except Exception as e:
        print(str(e))
        emit('receive_sensors', str(e))

@socketio.on("on_client")
def on_client(data):
    print(data)

@app.route('/')
def home():
    # show the index.html page
    return  render_template("index.html")


