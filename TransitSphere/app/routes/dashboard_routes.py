from flask import Blueprint, render_template
from app.services.gtfs_parser import gtfs
from app.services.simulation_engine import simulator
from app.services.ai_forecasting import forecast_service
from app.services.congestion_engine import congestion_service
from app.utils.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def landing():
    return render_template("landing.html")


@dashboard_bp.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        kpis=simulator.kpis(),
        routes=gtfs.featured_routes(18),
        insights=forecast_service.insights(),
        alerts=congestion_service.alerts(),
    )


@dashboard_bp.route("/user-dashboard")
@login_required
def user_dashboard():
    return render_template("user_dashboard.html", kpis=simulator.kpis(), routes=gtfs.featured_routes(8))
