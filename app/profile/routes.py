from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms import HealthProfileForm
from app.profile import profile


@profile.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    form = HealthProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.disease = form.disease.data
        current_user.medication = form.medication.data
        current_user.trigger = form.trigger.data

        db.session.commit()

        flash("Health profile updated.", "success")
        return redirect(url_for("profile.profile_page"))

    return render_template("profile.html", form=form)
