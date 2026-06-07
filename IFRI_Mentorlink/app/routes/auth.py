from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom       = request.form.get("nom")
        prenom    = request.form.get("prenom")
        email     = request.form.get("email")
        telephone = request.form.get("telephone")
        mdp       = request.form.get("mot_de_passe")

        if User.query.filter_by(email=email).first():
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(telephone=telephone).first():
            flash("Ce numéro est déjà utilisé.", "danger")
            return redirect(url_for("auth.register"))

        user = User(nom=nom, prenom=prenom, email=email,
                    telephone=telephone, mot_de_passe=hash_password(mdp))
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifiant = request.form.get("identifiant")
        mdp         = request.form.get("mot_de_passe")

        user = User.query.filter(
            (User.email == identifiant) | (User.telephone == identifiant)
        ).first()

        if user and verify_password(mdp, user.mot_de_passe):
            login_user(user)
            return redirect(url_for("profile.dashboard"))

        flash("Identifiant ou mot de passe incorrect.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
