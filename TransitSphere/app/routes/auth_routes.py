from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

USERS = {
    "admin@bmtc.ai": {"password": "admin123", "role": "Admin", "name": "BMTC Admin"},
    "dispatcher@bmtc.ai": {"password": "dispatch123", "role": "Dispatcher", "name": "Route Dispatcher"},
    "operator@bmtc.ai": {"password": "operator123", "role": "Transport Operator", "name": "Transport Operator"},
}

PUBLIC_USERS = {email: user for email, user in USERS.items() if user["role"] != "Admin"}


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = PUBLIC_USERS.get(email)
        if user and user["password"] == password:
            session["user"] = {"email": email, **user}
            return redirect(request.args.get("next") or url_for("dashboard.user_dashboard"))
        error = "Invalid operator credentials. Admins should use the admin login page."
    return render_template("login.html", error=error, admin_login=False)


@auth_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = USERS.get(email)
        if user and user["role"] == "Admin" and user["password"] == password:
            session["user"] = {"email": email, **user}
            return redirect(request.args.get("next") or url_for("dashboard.dashboard"))
        error = "Invalid admin credentials. Try admin@bmtc.ai / admin123"
    return render_template("login.html", error=error, admin_login=True)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["user"] = {
            "email": request.form.get("email", "new.user@bmtc.ai"),
            "name": request.form.get("name", "New Operator"),
            "role": request.form.get("role", "Transport Operator"),
            "password": "",
        }
        return redirect(url_for("dashboard.user_dashboard"))
    return render_template("register.html")


@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("dashboard.landing"))
