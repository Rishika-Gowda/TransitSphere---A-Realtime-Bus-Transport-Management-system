import os
from app import create_app, socketio
from app.services.simulation_engine import simulator

app = create_app()


@socketio.on("connect")
def handle_connect():
    socketio.emit("transport_update", simulator.tick())


def publish_live_state():
    import time
    while True:
        socketio.emit("transport_update", simulator.tick())
        time.sleep(4)


if __name__ == "__main__":
    socketio.start_background_task(publish_live_state)
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "5055")), debug=True, allow_unsafe_werkzeug=True)
