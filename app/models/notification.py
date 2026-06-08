from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notification"
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    contenu       = db.Column(db.String(255), nullable=False)
    lue           = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
