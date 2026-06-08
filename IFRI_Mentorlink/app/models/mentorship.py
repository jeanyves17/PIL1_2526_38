from app import db
from datetime import datetime

offre_competence = db.Table("offre_competence",
    db.Column("offre_id",      db.Integer, db.ForeignKey("offre_mentorat.id"), primary_key=True),
    db.Column("competence_id", db.Integer, db.ForeignKey("competence.id"),     primary_key=True)
)

class OffreMentorat(db.Model):
    __tablename__ = "offre_mentorat"
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type          = db.Column(db.String(10), nullable=False)
    description   = db.Column(db.Text)
    format        = db.Column(db.String(15), nullable=False)
    statut        = db.Column(db.String(15), default="actif")
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    competences = db.relationship("Competence", secondary=offre_competence, lazy="subquery")
