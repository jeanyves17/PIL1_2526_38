from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.match import Matching
from app.models.mentorship import OffreMentorat
from app.models.profile import Competence
from app.services.matching_service import calculer_matchings

matching_bp = Blueprint("matching", __name__)

@matching_bp.route("/match")
@login_required
def match():
    matchings = calculer_matchings(current_user.id)
    return render_template("matching/results.html", matchings=matchings)

@matching_bp.route("/match/respond/<int:match_id>/<string:reponse>")
@login_required
def respond(match_id, reponse):
    m = Matching.query.get_or_404(match_id)
    if reponse in ("accepte", "refuse"):
        m.statut = reponse
        db.session.commit()
        flash(f"Match {reponse} avec succès.", "success")
    return redirect(url_for("matching.match"))

@matching_bp.route("/offers")
@login_required
def offers():
    offres = OffreMentorat.query.filter_by(statut="actif").all()
    return render_template("matching/offers.html", offres=offres)

@matching_bp.route("/offers/new", methods=["GET", "POST"])
@login_required
def new_offer():
    if request.method == "POST":
        offre = OffreMentorat(
            user_id=current_user.id,
            type=request.form.get("type"),
            description=request.form.get("description"),
            format=request.form.get("format")
        )
        db.session.add(offre)
        db.session.commit()
        for cid in request.form.getlist("competences"):
            c = Competence.query.get(int(cid))
            if c:
                offre.competences.append(c)
        db.session.commit()
        flash("Offre publiée !", "success")
        return redirect(url_for("matching.offers"))

    competences = Competence.query.all()
    return render_template("matching/offers.html",
                           competences=competences, new=True)
