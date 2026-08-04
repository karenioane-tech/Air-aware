from datetime import datetime

from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Health profile — used by the risk engine to flag travel triggers
    disease = db.Column(db.String(100))
    medication = db.Column(db.String(100))
    trigger = db.Column(db.String(150))

    def __repr__(self):
        return f"<User {self.email}>"


class HealthLog(db.Model):
    """A symptom check-in. Logged over time so the assistant can spot trends,
    not just react to a single snapshot."""

    __tablename__ = "health_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    severity = db.Column(db.Integer, nullable=False)  # 1 (mild) .. 5 (emergency-level)
    symptoms = db.Column(db.String(200))
    notes = db.Column(db.String(300))

    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HealthLog user={self.user_id} severity={self.severity}>"


class RiskAssessment(db.Model):
    """A saved travel/occasion risk check. Kept so the assistant and dashboard
    can reference what was checked before, not just the current one."""

    __tablename__ = "risk_assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    destination = db.Column(db.String(150), nullable=False)
    air_quality_level = db.Column(db.String(20))
    pollen_level = db.Column(db.String(20))

    risk_level = db.Column(db.String(20))
    reasons = db.Column(db.String(400))

    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RiskAssessment {self.destination} risk={self.risk_level}>"
