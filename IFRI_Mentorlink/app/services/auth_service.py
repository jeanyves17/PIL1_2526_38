from flask_bcrypt import generate_password_hash, check_password_hash

def hash_password(mdp: str) -> str:
    return generate_password_hash(mdp).decode("utf-8")

def verify_password(mdp: str, hash: str) -> bool:
    return check_password_hash(hash, mdp)
