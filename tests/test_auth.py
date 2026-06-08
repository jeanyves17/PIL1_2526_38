import pytest
from app import db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_test(app):
    with app.app_context():
        u = User(nom="Koffi", prenom="Ama", email="ama@ifri.bj",
                 telephone="97000001", mot_de_passe=hash_password("test1234"))
        db.session.add(u)
        db.session.commit()

def test_hash_password():
    h = hash_password("monmotdepasse")
    assert h != "monmotdepasse"

def test_verify_password_correct():
    h = hash_password("monmotdepasse")
    assert verify_password("monmotdepasse", h) is True

def test_verify_password_incorrect():
    h = hash_password("monmotdepasse")
    assert verify_password("mauvais", h) is False

def test_register_succes(client):
    r = client.post("/register", data={
        "nom": "Dossou", "prenom": "Brice",
        "email": "brice@ifri.bj", "telephone": "97000002",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert r.status_code == 200

def test_register_email_duplique(client, user_test):
    r = client.post("/register", data={
        "nom": "Autre", "prenom": "Personne",
        "email": "ama@ifri.bj",
        "telephone": "97000099",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert "déjà utilisé" in r.data.decode("utf-8")

def test_register_telephone_duplique(client, user_test):
    r = client.post("/register", data={
        "nom": "Autre", "prenom": "Personne",
        "email": "nouveau@ifri.bj",
        "telephone": "97000001",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert "déjà utilisé" in r.data.decode("utf-8")

def test_login_succes_email(client, user_test):
    r = client.post("/login", data={
        "identifiant": "ama@ifri.bj",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert r.status_code == 200

def test_login_succes_telephone(client, user_test):
    r = client.post("/login", data={
        "identifiant": "97000001",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert r.status_code == 200

def test_login_mauvais_mdp(client, user_test):
    r = client.post("/login", data={
        "identifiant": "ama@ifri.bj",
        "mot_de_passe": "mauvais"
    }, follow_redirects=True)
    assert "incorrect" in r.data.decode("utf-8")

def test_login_utilisateur_inexistant(client):
    r = client.post("/login", data={
        "identifiant": "inconnu@ifri.bj",
        "mot_de_passe": "test1234"
    }, follow_redirects=True)
    assert "incorrect" in r.data.decode("utf-8")
