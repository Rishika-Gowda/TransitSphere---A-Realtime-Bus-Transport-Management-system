import os
from flask import Flask

try:
    from flask_socketio import SocketIO
except Exception:  # pragma: no cover - lets the app boot before deps are installed
    class SocketIO:
        def __init__(self, *args, **kwargs): pass
        def init_app(self, *args, **kwargs): pass
        def on(self, *args, **kwargs):
            def wrapper(fn): return fn
            return wrapper
        def emit(self, *args, **kwargs): pass
        def start_background_task(self, *args, **kwargs): pass
        def run(self, app, **kwargs): app.run(**{k: v for k, v in kwargs.items() if k in {"host", "port", "debug"}})

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "bmtc-smart-transport-dev-key")
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite:///transport.db")
    app.config["OPENWEATHER_API_KEY"] = os.getenv("OPENWEATHER_API_KEY", "")
    app.config["GTFS_PATH"] = os.getenv(
        "GTFS_PATH",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "gtfs")),
    )

    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.tracking_routes import tracking_bp
    from app.routes.analytics_routes import analytics_bp
    from app.routes.scheduling_routes import scheduling_bp
    from app.routes.simulation_routes import simulation_bp
    from app.routes.alerts_routes import alerts_bp
    from app.routes.api_routes import api_bp

    for bp in (auth_bp, dashboard_bp, tracking_bp, analytics_bp, scheduling_bp, simulation_bp, alerts_bp, api_bp):
        app.register_blueprint(bp)

    socketio.init_app(app)
    return app
