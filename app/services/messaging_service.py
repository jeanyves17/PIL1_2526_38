from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import db, socketio
from app.models.message import Conversation, Message

def get_or_create_conversation(user1_id: int, user2_id: int) -> Conversation:
    conv = Conversation.query.filter(
        ((Conversation.id_utilisateur1 == user1_id) &
         (Conversation.id_utilisateur2 == user2_id)) |
        ((Conversation.id_utilisateur1 == user2_id) &
         (Conversation.id_utilisateur2 == user1_id))
    ).first()
    if not conv:
        conv = Conversation(id_utilisateur1=user1_id, id_utilisateur2=user2_id)
        db.session.add(conv)
        db.session.commit()
    return conv

@socketio.on("rejoindre")
def on_rejoindre(data):
    join_room(str(data.get("conv_id")))
    emit("statut", {"msg": "Connecté"}, room=str(data.get("conv_id")))

@socketio.on("quitter")
def on_quitter(data):
    leave_room(str(data.get("conv_id")))

@socketio.on("envoyer_message")
def on_envoyer_message(data):
    conv_id = data.get("conv_id")
    contenu = data.get("contenu", "").strip()
    if not contenu or not conv_id:
        return
    msg = Message(id_conversation=conv_id,
                  id_expediteur=current_user.id, contenu=contenu)
    db.session.add(msg)
    db.session.commit()
    emit("nouveau_message", {
        "id":         msg.id,
        "contenu":    msg.contenu,
        "expediteur": current_user.id,
        "prenom":     current_user.prenom,
        "nom":        current_user.nom,
        "date":       msg.date_envoi.strftime("%H:%M")
    }, room=str(conv_id))

@socketio.on("en_train_d_ecrire")
def on_typing(data):
    emit("utilisateur_ecrit", {"prenom": current_user.prenom},
         room=str(data.get("conv_id")), include_self=False)
