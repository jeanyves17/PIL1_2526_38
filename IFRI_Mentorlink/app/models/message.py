from app import db
from datetime import datetime

class Conversation(db.Model):
    __tablename__   = "conversation"
    id              = db.Column(db.Integer, primary_key=True)
    id_utilisateur1 = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_utilisateur2 = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("Message", backref="conversation",
                               lazy=True, order_by="Message.date_envoi")
    user1    = db.relationship("User", foreign_keys=[id_utilisateur1])
    user2    = db.relationship("User", foreign_keys=[id_utilisateur2])

class Message(db.Model):
    __tablename__   = "message"
    id              = db.Column(db.Integer, primary_key=True)
    id_conversation = db.Column(db.Integer, db.ForeignKey("conversation.id"), nullable=False)
    id_expediteur   = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    contenu         = db.Column(db.Text, nullable=False)
    date_envoi      = db.Column(db.DateTime, default=datetime.utcnow)
    lu              = db.Column(db.Boolean, default=False)

    expediteur = db.relationship("User", foreign_keys=[id_expediteur])
