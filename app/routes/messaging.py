from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.message import Conversation, Message
from app.services.messaging_service import get_or_create_conversation

messaging_bp = Blueprint("messaging", __name__)

@messaging_bp.route("/messages")
@login_required
def inbox():
    conversations = Conversation.query.filter(
        (Conversation.id_utilisateur1 == current_user.id) |
        (Conversation.id_utilisateur2 == current_user.id)
    ).order_by(Conversation.date_creation.desc()).all()
    return render_template("messaging/inbox.html", conversations=conversations)

@messaging_bp.route("/messages/<int:conv_id>")
@login_required
def conversation(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    Message.query.filter_by(id_conversation=conv_id, lu=False).filter(
        Message.id_expediteur != current_user.id
    ).update({"lu": True})
    db.session.commit()
    return render_template("messaging/conversation.html", conv=conv)

@messaging_bp.route("/messages/start/<int:user_id>")
@login_required
def start(user_id):
    conv = get_or_create_conversation(current_user.id, user_id)
    return redirect(url_for("messaging.conversation", conv_id=conv.id))
