from flask import Blueprint, render_template
from app.services.gtfs_parser import gtfs
from app.utils.auth import login_required

tracking_bp = Blueprint("tracking", __name__)


@tracking_bp.route("/tracking")
@tracking_bp.route("/live-tracking")
@login_required
def tracking():
    return render_template("tracking.html", routes=gtfs.featured_routes(18))
