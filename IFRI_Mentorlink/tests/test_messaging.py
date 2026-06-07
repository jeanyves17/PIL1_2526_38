import pytest
from app import db
from app.models.user import User
from app.models.message import Conversation, Message
from app.services.auth_service import hash_password
from app.services.messaging_service import get_or_create_conversation

@pytest.fixture
def deux_users(app):
    with app.app_context():
        u1 = User(nom="A", prenom="A", email="a@ifri.bj",
                  telephone="001", mot_de_passe=hash_password("x"))
        u2 = User(nom="B", prenom="B", email="b@ifri.bj",
                  telephone="002", mot_de_passe=hash_password("x"))
        db.session.add_all([u1, u2])
        db.session.commit()
        return u1.id, u2.id

def test_creer_conversation(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv = get_or_create_conversation(u1_id, u2_id)
        assert conv.id is not None
        assert Conversation.query.count() == 1

def test_pas_de_doublon_conversation(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv1 = get_or_create_conversation(u1_id, u2_id)
        conv2 = get_or_create_conversation(u1_id, u2_id)
        assert conv1.id == conv2.id
        assert Conversation.query.count() == 1

def test_conversation_bidirectionnelle(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv1 = get_or_create_conversation(u1_id, u2_id)
        conv2 = get_or_create_conversation(u2_id, u1_id)
        assert conv1.id == conv2.id

def test_ajouter_message(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv = get_or_create_conversation(u1_id, u2_id)
        msg = Message(id_conversation=conv.id,
                      id_expediteur=u1_id, contenu="Bonjour !")
        db.session.add(msg)
        db.session.commit()
        assert Message.query.count() == 1
        assert msg.lu is False

def test_marquer_message_lu(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv = get_or_create_conversation(u1_id, u2_id)
        msg = Message(id_conversation=conv.id,
                      id_expediteur=u1_id, contenu="Salut")
        db.session.add(msg)
        db.session.commit()
        Message.query.filter_by(id_conversation=conv.id, lu=False).update({"lu": True})
        db.session.commit()
        assert Message.query.filter_by(lu=True).count() == 1

def test_ordre_messages_chronologique(app, deux_users):
    with app.app_context():
        u1_id, u2_id = deux_users
        conv = get_or_create_conversation(u1_id, u2_id)
        for texte in ["Premier", "Deuxième", "Troisième"]:
            db.session.add(Message(id_conversation=conv.id,
                                   id_expediteur=u1_id, contenu=texte))
        db.session.commit()
        messages = Message.query.filter_by(
            id_conversation=conv.id).order_by(Message.date_envoi).all()
        assert messages[0].contenu == "Premier"
        assert messages[-1].contenu == "Troisième"
