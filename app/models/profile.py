from app import db

profil_competence = db.Table("profil_competence",
    db.Column("profil_id",     db.Integer, db.ForeignKey("profile.id"), primary_key=True),
    db.Column("competence_id", db.Integer, db.ForeignKey("competence.id"), primary_key=True),
    db.Column("type", db.String(10), primary_key=True)
)

class Competence(db.Model):
    __tablename__ = "competence"
    id      = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100), unique=True, nullable=False)

class Disponibilite(db.Model):
    __tablename__ = "disponibilite"
    id          = db.Column(db.Integer, primary_key=True)
    profil_id   = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)
    jour        = db.Column(db.String(10), nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin   = db.Column(db.Time, nullable=False)

class Profile(db.Model):
    __tablename__ = "profile"
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    photo_profil = db.Column(db.String(255), default="default_avatar.png")
    filiere      = db.Column(db.String(50),  nullable=False)
    niveau       = db.Column(db.String(10),  nullable=False)
    bio          = db.Column(db.Text)

    competences    = db.relationship("Competence", secondary=profil_competence, lazy="subquery")
    disponibilites = db.relationship("Disponibilite", backref="profil", lazy=True)
