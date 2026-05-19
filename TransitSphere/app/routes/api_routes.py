from flask import Blueprint, jsonify, request
from app.services.gtfs_parser import gtfs
from app.services.simulation_engine import simulator
from app.services.congestion_engine import congestion_service
from app.services.weather_service import weather_service

api_bp = Blueprint("api", __name__)


@api_bp.route("/api/routes")
def routes():
    limit = request.args.get("limit", type=int)
    featured = request.args.get("featured", "0") == "1"
    data = gtfs.featured_routes(limit or 18) if featured else gtfs.routes()
    return jsonify(data[:limit] if limit else data)


@api_bp.route("/api/stops")
def stops():
    q = request.args.get("q", "").lower()
    data = gtfs.stops()
    if q:
        data = [s for s in data if q in s["stop_name"].lower()]
    return jsonify(data)


@api_bp.route("/api/route/<route_id>")
def route_detail(route_id):
    return jsonify(gtfs.route_detail(route_id))


@api_bp.route("/api/dashboard")
def dashboard_data():
    return jsonify({"kpis": simulator.kpis(), "congestion": congestion_service.hotspots(), "fleet": simulator.snapshot()})


@api_bp.route("/api/weather")
def weather():
    return jsonify(weather_service.current())
