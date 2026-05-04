from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models import ActivityLog, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.is_active and user.check_password(password):
            login_user(user)
            db.session.add(
                ActivityLog(
                    user_id=user.id,
                    action="login",
                    entity_name="User",
                    entity_id=user.id,
                    description="Вход в админ-панель",
                    ip_address=request.remote_addr,
                )
            )
            db.session.commit()
            return redirect(url_for("admin.dashboard"))

        flash("Неверный email или пароль.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    db.session.add(
        ActivityLog(
            user_id=current_user.id,
            action="logout",
            entity_name="User",
            entity_id=current_user.id,
            description="Выход из админ-панели",
            ip_address=request.remote_addr,
        )
    )
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))
