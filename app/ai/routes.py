from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms import SymptomLogForm
from app.models import HealthLog, RiskAssessment
from app.ai import ai


CONDITION_ADVICE = {
    "asthma": "Keep your rescue inhaler within reach and avoid known triggers like smoke, dust, and cold air.",
    "copd": "Pace physical activity, avoid smoky or polluted air, and keep medication on hand.",
    "pollen allergy": "Check pollen forecasts before outdoor plans and consider antihistamines ahead of exposure.",
    "hay fever": "Check pollen forecasts before outdoor plans and consider antihistamines ahead of exposure.",
    "eczema": "Avoid overheating, sweat, and known irritants; keep moisturizer on hand.",
    "migraine": "Watch for bright light, strong smells, and heat; keep any prescribed medication with you.",
}


@ai.route("/assistant", methods=["GET", "POST"])
@login_required
def assistant():
    form = SymptomLogForm()

    if form.validate_on_submit():
        entry = HealthLog(
            user_id=current_user.id,
            severity=int(form.severity.data),
            symptoms=form.symptoms.data,
            notes=form.notes.data,
        )
        db.session.add(entry)
        db.session.commit()
        flash("Logged — thanks for checking in.", "success")
        return redirect(url_for("ai.assistant"))

    logs = (
        HealthLog.query.filter_by(user_id=current_user.id)
        .order_by(HealthLog.logged_at.desc())
        .limit(30)
        .all()
    )

    recent = [l for l in logs if l.logged_at >= datetime.utcnow() - timedelta(days=7)]
    trend = None
    if recent:
        avg = sum(l.severity for l in recent) / len(recent)
        trend = f"Average severity over the last 7 days: {avg:.1f}/5 across {len(recent)} check-in(s)."

    disease = (current_user.disease or "").lower()
    condition_tip = None
    for condition, tip in CONDITION_ADVICE.items():
        if condition in disease:
            condition_tip = tip
            break

    last_check = (
        RiskAssessment.query.filter_by(user_id=current_user.id)
        .order_by(RiskAssessment.checked_at.desc())
        .first()
    )

    return render_template(
        "assistant.html",
        form=form,
        logs=logs[:10],
        trend=trend,
        condition_tip=condition_tip,
        last_check=last_check,
    )
