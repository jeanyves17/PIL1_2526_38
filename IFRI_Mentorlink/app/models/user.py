from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id               = db.Column(db.Integer, primary_key=True)
    nom              = db.Column(db.String(100), nullable=False)
    prenom           = db.Column(db.String(100), nullable=False)
    email            = db.Column(db.String(150), unique=True, nullable=False)
    telephone        = db.Column(db.String(20),  unique=True, nullable=False)
    mot_de_passe     = db.Column(db.String(255), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    profile       = db.relationship("Profile", backref="user", uselist=False)
    offres        = db.relationship("OffreMentorat", backref="auteur", lazy=True)
    notifications = db.relationship("Notification", backref="destinataire", lazy=True)

    def __repr__(self):
        return f"<User {self.prenom} {self.nom}>"
