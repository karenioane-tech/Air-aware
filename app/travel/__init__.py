from flask import Blueprint

travel = Blueprint("travel", __name__)

from app.travel import routes  # noqa: E402,F401
