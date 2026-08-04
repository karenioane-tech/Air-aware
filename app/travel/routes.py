from flask import render_template
from flask_login import login_required, current_user

from app import db
from app.forms import TravelCheckForm
from app.models import RiskAssessment
from app.services.risk_engine import assess_risk
from app.services.recommendations import build_recommendations
from app.travel import travel


@travel.route("/travel", methods=["GET", "POST"])
@login_required
def travel_page():
    form = TravelCheckForm()
    result = None

    if form.validate_on_submit():
        risk_level, reasons = assess_risk(
            current_user, form.air_quality_level.data, form.pollen_level.data
        )
        tips = build_recommendations(risk_level, current_user)

        assessment = RiskAssessment(
            user_id=current_user.id,
            destination=form.destination.data,
            air_quality_level=form.air_quality_level.data,
            pollen_level=form.pollen_level.data,
            risk_level=risk_level,
            reasons="; ".join(reasons),
        )
        db.session.add(assessment)
        db.session.commit()

        result = {
            "destination": form.destination.data,
            "risk_level": risk_level,
            "reasons": reasons,
            "tips": tips,
        }

    history = (
        RiskAssessment.query.filter_by(user_id=current_user.id)
        .order_by(RiskAssessment.checked_at.desc())
        .limit(5)
        .all()
    )

    return render_template("travel.html", form=form, result=result, history=history)
