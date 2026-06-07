from app import db
from datetime import datetime

class Matching(db.Model):
    __tablename__ = "matching"
    id         = db.Column(db.Integer, primary_key=True)
    id_mentor  = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    id_mentore = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score      = db.Column(db.Numeric(5, 2), nullable=False)
    statut     = db.Column(db.String(15), default="propose")
    date_match = db.Column(db.DateTime, default=datetime.utcnow)

    mentor  = db.relationship("User", foreign_keys=[id_mentor])
    mentore = db.relationship("User", foreign_keys=[id_mentore])
