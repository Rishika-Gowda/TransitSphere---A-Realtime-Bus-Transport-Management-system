from flask import Blueprint, render_template, jsonify
from app.services.congestion_engine import congestion_service
from app.utils.auth import login_required

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html", alerts=congestion_service.alerts())


@alerts_bp.route("/api/alerts")
def alerts_api():
    return jsonify(congestion_service.alerts())
