from functools import wraps
from flask import redirect, request, session, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user:
            return redirect(url_for("auth.admin_login", next=request.path))
        if user.get("role") != "Admin":
            return redirect(url_for("dashboard.dashboard"))
        return view(*args, **kwargs)

    return wrapped
