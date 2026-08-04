from flask import render_template
from flask_login import login_required, current_user

from app.dashboard import dashboard


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html", user=current_user)
