import pytest
from datetime import time
from app import db
from app.models.user import User
from app.models.profile import Profile, Competence, Disponibilite, profil_competence
from app.services.auth_service import hash_password
from app.services.matching_service import (
    score_competences, score_filiere,
    score_disponibilite, calculer_score
)

@pytest.fixture
def profiles(app):
    with app.app_context():
        python = Competence(libelle="Python")
        sql    = Competence(libelle="SQL")
        algo   = Competence(libelle="Algorithmique")
        db.session.add_all([python, sql, algo])
        db.session.commit()

        u1 = User(nom="A", prenom="A", email="a@ifri.bj",
                  telephone="001", mot_de_passe=hash_password("x"))
        u2 = User(nom="B", prenom="B", email="b@ifri.bj",
                  telephone="002", mot_de_passe=hash_password("x"))
        db.session.add_all([u1, u2])
        db.session.commit()

        p1 = Profile(user_id=u1.id, filiere="GL", niveau="L1")
        p2 = Profile(user_id=u2.id, filiere="GL", niveau="L1")
        db.session.add_all([p1, p2])
        db.session.commit()

        db.session.execute(profil_competence.insert().values(
            profil_id=p1.id, competence_id=python.id, type="fort"))
        db.session.execute(profil_competence.insert().values(
            profil_id=p1.id, competence_id=sql.id, type="fort"))
        db.session.execute(profil_competence.insert().values(
            profil_id=p2.id, competence_id=python.id, type="faible"))
        db.session.execute(profil_competence.insert().values(
            profil_id=p2.id, competence_id=algo.id, type="faible"))

        db.session.add(Disponibilite(profil_id=p1.id, jour="Lundi",
            heure_debut=time(8, 0), heure_fin=time(10, 0)))
        db.session.add(Disponibilite(profil_id=p2.id, jour="Lundi",
            heure_debut=time(8, 0), heure_fin=time(10, 0)))
        db.session.commit()

def test_score_competences_partiel(app, profiles):
    with app.app_context():
        p1, p2 = Profile.query.all()
        s = score_competences(p1, p2)
        assert 0 < s <= 1

def test_score_filiere_meme(app, profiles):
    with app.app_context():
        p1, p2 = Profile.query.all()
        assert score_filiere(p1, p2) == 1.0

def test_score_filiere_different(app, profiles):
    with app.app_context():
        p1, p2 = Profile.query.all()
        p2.filiere = "IA"
        db.session.commit()
        assert score_filiere(p1, p2) == 0.5

def test_score_disponibilite_commun(app, profiles):
    with app.app_context():
        p1, p2 = Profile.query.all()
        assert score_disponibilite(p1, p2) == 1.0

def test_calculer_score_entre_0_et_100(app, profiles):
    with app.app_context():
        p1, p2 = Profile.query.all()
        s = calculer_score(p1, p2)
        assert 0 <= s <= 100

def test_score_sans_competences(app):
    with app.app_context():
        u = User(nom="C", prenom="C", email="c@ifri.bj",
                 telephone="003", mot_de_passe=hash_password("x"))
        db.session.add(u)
        db.session.commit()
        p = Profile(user_id=u.id, filiere="SI", niveau="L1")
        db.session.add(p)
        db.session.commit()
        assert score_competences(p, p) == 0.0
        assert score_disponibilite(p, p) == 0.0
