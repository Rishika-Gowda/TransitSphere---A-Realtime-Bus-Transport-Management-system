from flask import Blueprint, jsonify
from app.services.simulation_engine import simulator

simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.route("/api/simulation/state")
def state():
    return jsonify(simulator.tick())


@simulation_bp.route("/api/simulation/kpis")
def kpis():
    return jsonify(simulator.kpis())
