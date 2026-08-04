from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm
from app.auth import auth


@auth.route("/")
def home():
    return render_template("index.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))

    form = RegisterForm()

    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()

        if existing:
            flash("That email is already registered.", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard.dashboard_page"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.home"))
