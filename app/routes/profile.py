from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.profile import Profile, Competence, Disponibilite, profil_competence
from app.services.upload_service import sauvegarder_photo

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard/index.html", user=current_user)

@profile_bp.route("/profile/<int:user_id>")
@login_required
def view(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first_or_404()
    return render_template("profile/view.html", profile=profile)

@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit():
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if request.method == "POST":
        filiere = request.form.get("filiere")
        niveau  = request.form.get("niveau")
        bio     = request.form.get("bio")
        forts   = request.form.getlist("points_forts")
        faibles = request.form.getlist("points_faibles")
        photo   = request.files.get("photo_profil")

        if not profile:
            profile = Profile(user_id=current_user.id,
                              filiere=filiere, niveau=niveau, bio=bio)
            db.session.add(profile)
        else:
            profile.filiere = filiere
            profile.niveau  = niveau
            profile.bio     = bio

        # Gestion de la photo
        if photo and photo.filename:
            nom_fichier = sauvegarder_photo(photo, current_user.id)
            if nom_fichier:
                profile.photo_profil = nom_fichier
            else:
                flash("Format de photo non autorisé (jpg, png, webp).", "warning")

        db.session.commit()

        # Mise à jour des compétences
        db.session.execute(
            profil_competence.delete().where(
                profil_competence.c.profil_id == profile.id
            )
        )
        for cid in forts:
            db.session.execute(profil_competence.insert().values(
                profil_id=profile.id, competence_id=int(cid), type="fort"))
        for cid in faibles:
            db.session.execute(profil_competence.insert().values(
                profil_id=profile.id, competence_id=int(cid), type="faible"))

        db.session.commit()
        flash("Profil mis à jour !", "success")
        return redirect(url_for("profile.view", user_id=current_user.id))

    competences = Competence.query.all()
    return render_template("profile/edit.html",
                           profile=profile, competences=competences)
