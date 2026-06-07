import os
import uuid
from flask import current_app
from PIL import Image

EXTENSIONS_AUTORISEES = {"png", "jpg", "jpeg", "webp"}

def extension_autorisee(filename: str) -> bool:
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in EXTENSIONS_AUTORISEES

def sauvegarder_photo(fichier, user_id: int) -> str | None:
    """
    Redimensionne et sauvegarde la photo de profil.
    Retourne le nom du fichier sauvegardé, ou None si format invalide.
    """
    if not extension_autorisee(fichier.filename):
        return None

    ext          = fichier.filename.rsplit(".", 1)[1].lower()
    nom_fichier  = f"avatar_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    dossier      = os.path.join(current_app.root_path,
                                current_app.config["UPLOAD_FOLDER"])

    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)

    # Redimensionnement 200x200 avec Pillow
    img = Image.open(fichier)
    img = img.convert("RGB")
    img.thumbnail((200, 200))
    img.save(chemin)

    return nom_fichier
