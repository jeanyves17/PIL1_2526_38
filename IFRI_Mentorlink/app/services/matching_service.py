from app import db, socketio
from app.models.user import User
from app.models.profile import Profile, profil_competence
from app.models.match import Matching

POIDS_COMPETENCE = 0.5
POIDS_FILIERE    = 0.3
POIDS_DISPO      = 0.2

def score_competences(mentor: Profile, mentore: Profile) -> float:
    forts_mentor = {row.competence_id for row in db.session.execute(
        db.select(profil_competence.c.competence_id)
        .where(profil_competence.c.profil_id == mentor.id)
        .where(profil_competence.c.type == "fort")
    )}
    faibles_mentore = {row.competence_id for row in db.session.execute(
        db.select(profil_competence.c.competence_id)
        .where(profil_competence.c.profil_id == mentore.id)
        .where(profil_competence.c.type == "faible")
    )}
    if not faibles_mentore:
        return 0.0
    return len(forts_mentor & faibles_mentore) / len(faibles_mentore)

def score_filiere(mentor: Profile, mentore: Profile) -> float:
    return 1.0 if mentor.filiere == mentore.filiere else 0.5

def score_disponibilite(mentor: Profile, mentore: Profile) -> float:
    dispos_mentor  = {(d.jour, d.heure_debut, d.heure_fin) for d in mentor.disponibilites}
    dispos_mentore = {(d.jour, d.heure_debut, d.heure_fin) for d in mentore.disponibilites}
    if not dispos_mentore:
        return 0.0
    return len(dispos_mentor & dispos_mentore) / len(dispos_mentore)

def calculer_score(mentor: Profile, mentore: Profile) -> float:
    return round((
        score_competences(mentor, mentore) * POIDS_COMPETENCE +
        score_filiere(mentor, mentore)     * POIDS_FILIERE    +
        score_disponibilite(mentor, mentore) * POIDS_DISPO
    ) * 100, 2)

def calculer_matchings(user_id: int, seuil: float = 30.0):
    mentore_profile = Profile.query.filter_by(user_id=user_id).first()
    if not mentore_profile:
        return []

    resultats = []
    for m in Profile.query.filter(Profile.user_id != user_id).all():
        score = calculer_score(m, mentore_profile)
        if score >= seuil:
            existing = Matching.query.filter_by(
                id_mentor=m.user_id, id_mentore=user_id).first()
            if not existing:
                db.session.add(Matching(id_mentor=m.user_id,
                                        id_mentore=user_id, score=score))
            resultats.append({"profil": m, "score": score})

    db.session.commit()
    return sorted(resultats, key=lambda x: x["score"], reverse=True)
