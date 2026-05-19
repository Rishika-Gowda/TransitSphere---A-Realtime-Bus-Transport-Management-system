from flask import Blueprint, render_template, jsonify
from app.services.ai_forecasting import forecast_service
from app.services.congestion_engine import congestion_service
from app.utils.auth import login_required

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html", forecasts=forecast_service.forecast())


@analytics_bp.route("/congestion")
@login_required
def congestion():
    return render_template("congestion.html", hotspots=congestion_service.hotspots())


@analytics_bp.route("/api/analytics/forecast")
def forecast_api():
    return jsonify(forecast_service.forecast())
