import os

basedir = os.path.abspath(os.path.dirname(__file__))


def _normalize_db_url(url):
    # Some providers (Render, Heroku) still hand out DATABASE_URL with the
    # old "postgres://" scheme; SQLAlchemy 1.4+ requires "postgresql://".
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "airaware-dev-secret-key"

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.environ.get("DATABASE_URL")
    ) or "sqlite:///" + os.path.join(basedir, "instance", "airaware.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
