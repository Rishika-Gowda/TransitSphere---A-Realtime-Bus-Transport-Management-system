from flask import Blueprint, render_template, jsonify
from app.services.scheduling_engine import scheduling_service
from app.utils.auth import login_required

scheduling_bp = Blueprint("scheduling", __name__)


@scheduling_bp.route("/scheduling")
@login_required
def scheduling():
    return render_template("scheduling.html", plan=scheduling_service.plan())


@scheduling_bp.route("/api/scheduling/recommendations")
def recommendations():
    return jsonify(scheduling_service.plan())
