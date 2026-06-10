"""
IFRI_MentorLink - Backend Flask
Application de mise en relation mentor/mentoré pour les étudiants de l'IFRI.
"""
import os
import sqlite3
import hashlib
import secrets
from datetime import datetime
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mentorlink.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "..", "database", "schema_sqlite.sql")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

app = Flask(__name__, static_folder=None)
CORS(app, supports_credentials=True)

# ---------- DB helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(_e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    if os.path.exists(DB_PATH):
        return
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql = f.read()
    con = sqlite3.connect(DB_PATH)
    con.executescript(sql)
    con.commit()
    con.close()
    print(f"[init_db] Base créée: {DB_PATH}")

# ---------- Auth helpers ----------
def hash_password(pw: str, salt: str = None):
    salt = salt or secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${h}"

def verify_password(pw: str, stored: str) -> bool:
    try:
        salt, _ = stored.split("$", 1)
        return hash_password(pw, salt) == stored
    except Exception:
        return False

def create_token(user_id: int):
    token = secrets.token_urlsafe(32)
    db = get_db()
    db.execute("INSERT INTO sessions(token, user_id, created_at) VALUES(?,?,?)",
               (token, user_id, datetime.utcnow().isoformat()))
    db.commit()
    return token

def current_user():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "): return None
    token = auth[7:]
    db = get_db()
    row = db.execute("""SELECT u.* FROM users u JOIN sessions s ON s.user_id=u.id
                        WHERE s.token=?""", (token,)).fetchone()
    return dict(row) if row else None

def require_auth():
    u = current_user()
    if not u:
        return None, (jsonify({"error": "Non authentifié"}), 401)
    return u, None

# ---------- Auth routes ----------
@app.post("/api/register")
def register():
    d = request.get_json() or {}
    required = ["nom", "prenom", "email", "telephone", "password"]
    if not all(d.get(k) for k in required):
        return jsonify({"error": "Champs manquants"}), 400
    db = get_db()
    exists = db.execute("SELECT 1 FROM users WHERE email=? OR telephone=?",
                        (d["email"], d["telephone"])).fetchone()
    if exists:
        return jsonify({"error": "Email ou téléphone déjà utilisé"}), 409
    cur = db.execute("""INSERT INTO users(nom,prenom,email,telephone,password_hash,
                        filiere,niveau,bio,photo_url,disponibilites,competences,lacunes)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                     (d["nom"], d["prenom"], d["email"], d["telephone"],
                      hash_password(d["password"]),
                      d.get("filiere",""), d.get("niveau",""),
                      d.get("bio",""), d.get("photo_url",""),
                      d.get("disponibilites",""),
                      ",".join(d.get("competences",[])) if isinstance(d.get("competences"), list) else d.get("competences",""),
                      ",".join(d.get("lacunes",[])) if isinstance(d.get("lacunes"), list) else d.get("lacunes","")))
    db.commit()
    uid = cur.lastrowid
    token = create_token(uid)
    return jsonify({"token": token, "user_id": uid})

@app.post("/api/login")
def login():
    d = request.get_json() or {}
    ident = d.get("identifiant", "")
    pw = d.get("password", "")
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email=? OR telephone=?",
                     (ident, ident)).fetchone()
    if not row or not verify_password(pw, row["password_hash"]):
        return jsonify({"error": "Identifiants invalides"}), 401
    token = create_token(row["id"])
    return jsonify({"token": token, "user_id": row["id"]})

@app.post("/api/logout")
def logout():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        db = get_db()
        db.execute("DELETE FROM sessions WHERE token=?", (auth[7:],))
        db.commit()
    return jsonify({"ok": True})

# ---------- Profile ----------
@app.get("/api/me")
def me():
    u, err = require_auth()
    if err: return err
    u.pop("password_hash", None)
    return jsonify(u)

@app.put("/api/me")
def update_me():
    u, err = require_auth()
    if err: return err
    d = request.get_json() or {}
    fields = ["nom","prenom","filiere","niveau","bio","photo_url",
              "disponibilites","competences","lacunes"]
    sets, vals = [], []
    for f in fields:
        if f in d:
            v = d[f]
            if isinstance(v, list): v = ",".join(v)
            sets.append(f"{f}=?"); vals.append(v)
    if not sets: return jsonify({"ok": True})
    vals.append(u["id"])
    db = get_db()
    db.execute(f"UPDATE users SET {','.join(sets)} WHERE id=?", vals)
    db.commit()
    return jsonify({"ok": True})

@app.get("/api/users/<int:uid>")
def get_user(uid):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    if not row: return jsonify({"error": "Introuvable"}), 404
    d = dict(row); d.pop("password_hash", None)
    return jsonify(d)

# ---------- Offres / demandes ----------
@app.post("/api/offres")
def create_offre():
    u, err = require_auth()
    if err: return err
    d = request.get_json() or {}
    db = get_db()
    cur = db.execute("""INSERT INTO offres(user_id, type, matiere, description,
                        disponibilites, format, created_at)
                        VALUES(?,?,?,?,?,?,?)""",
                     (u["id"], d.get("type","offre"), d.get("matiere",""),
                      d.get("description",""), d.get("disponibilites",""),
                      d.get("format","les_deux"), datetime.utcnow().isoformat()))
    db.commit()
    return jsonify({"id": cur.lastrowid})

@app.get("/api/offres")
def list_offres():
    db = get_db()
    type_ = request.args.get("type")
    q = request.args.get("q","").strip()
    sql = """SELECT o.*, u.nom, u.prenom, u.filiere, u.photo_url
             FROM offres o JOIN users u ON u.id=o.user_id WHERE 1=1"""
    params = []
    if type_: sql += " AND o.type=?"; params.append(type_)
    if q: sql += " AND (o.matiere LIKE ? OR o.description LIKE ?)"; params += [f"%{q}%", f"%{q}%"]
    sql += " ORDER BY o.created_at DESC"
    rows = [dict(r) for r in db.execute(sql, params).fetchall()]
    return jsonify(rows)

# ---------- Matching ----------
def _set(s): return {x.strip().lower() for x in (s or "").split(",") if x.strip()}

@app.get("/api/match")
def match():
    u, err = require_auth()
    if err: return err
    db = get_db()
    me_comp = _set(u["competences"])
    me_lac = _set(u["lacunes"])
    me_dispo = _set(u["disponibilites"])
    rows = db.execute("SELECT * FROM users WHERE id != ?", (u["id"],)).fetchall()
    results = []
    for r in rows:
        d = dict(r); d.pop("password_hash", None)
        comp = _set(d["competences"])
        lac = _set(d["lacunes"])
        dispo = _set(d["disponibilites"])
        # Compatibilité : mes lacunes ∩ ses compétences (il peut m'aider)
        #               + mes compétences ∩ ses lacunes (je peux l'aider)
        peut_maider = me_lac & comp
        je_peux_aider = me_comp & lac
        matiere_score = len(peut_maider) + len(je_peux_aider)
        dispo_score = len(me_dispo & dispo)
        filiere_score = 1 if d["filiere"] == u["filiere"] else 0
        total = matiere_score * 3 + dispo_score * 2 + filiere_score
        if total > 0:
            d["score"] = total
            d["matieres_communes"] = sorted(peut_maider | je_peux_aider)
            d["disponibilites_communes"] = sorted(me_dispo & dispo)
            d["role_propose"] = "mentor" if peut_maider else "mentoré"
            results.append(d)
    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results[:30])

# ---------- Messagerie ----------
def _get_or_create_conversation(db, u1, u2):
    a, b = sorted([u1, u2])
    row = db.execute("SELECT id FROM conversations WHERE user_a=? AND user_b=?",
                     (a, b)).fetchone()
    if row: return row["id"]
    cur = db.execute("INSERT INTO conversations(user_a, user_b, created_at) VALUES(?,?,?)",
                     (a, b, datetime.utcnow().isoformat()))
    db.commit()
    return cur.lastrowid

@app.post("/api/conversations")
def start_conv():
    u, err = require_auth()
    if err: return err
    d = request.get_json() or {}
    other = int(d.get("user_id", 0))
    if not other or other == u["id"]:
        return jsonify({"error": "Utilisateur invalide"}), 400
    db = get_db()
    cid = _get_or_create_conversation(db, u["id"], other)
    return jsonify({"conversation_id": cid})

@app.get("/api/conversations")
def list_conv():
    u, err = require_auth()
    if err: return err
    db = get_db()
    rows = db.execute("""
      SELECT c.id, c.created_at,
        CASE WHEN c.user_a=? THEN c.user_b ELSE c.user_a END AS other_id,
        (SELECT contenu FROM messages WHERE conversation_id=c.id ORDER BY id DESC LIMIT 1) AS last_message,
        (SELECT created_at FROM messages WHERE conversation_id=c.id ORDER BY id DESC LIMIT 1) AS last_at
      FROM conversations c WHERE c.user_a=? OR c.user_b=?
      ORDER BY last_at DESC NULLS LAST""", (u["id"], u["id"], u["id"])).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        other = db.execute("SELECT id,nom,prenom,photo_url FROM users WHERE id=?",
                           (d["other_id"],)).fetchone()
        d["other"] = dict(other) if other else None
        out.append(d)
    return jsonify(out)

@app.get("/api/conversations/<int:cid>/messages")
def get_messages(cid):
    u, err = require_auth()
    if err: return err
    db = get_db()
    conv = db.execute("SELECT * FROM conversations WHERE id=?", (cid,)).fetchone()
    if not conv or u["id"] not in (conv["user_a"], conv["user_b"]):
        return jsonify({"error": "Accès refusé"}), 403
    after = int(request.args.get("after", 0))
    rows = db.execute("""SELECT * FROM messages WHERE conversation_id=? AND id>?
                         ORDER BY id ASC""", (cid, after)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.post("/api/conversations/<int:cid>/messages")
def post_message(cid):
    u, err = require_auth()
    if err: return err
    db = get_db()
    conv = db.execute("SELECT * FROM conversations WHERE id=?", (cid,)).fetchone()
    if not conv or u["id"] not in (conv["user_a"], conv["user_b"]):
        return jsonify({"error": "Accès refusé"}), 403
    contenu = (request.get_json() or {}).get("contenu","").strip()
    if not contenu: return jsonify({"error": "Message vide"}), 400
    cur = db.execute("""INSERT INTO messages(conversation_id, sender_id, contenu, created_at)
                        VALUES(?,?,?,?)""",
                     (cid, u["id"], contenu, datetime.utcnow().isoformat()))
    db.commit()
    return jsonify({"id": cur.lastrowid})

# ---------- Frontend serving ----------
@app.route("/")
def index_html():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
