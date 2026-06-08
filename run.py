import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

env       = os.getenv("FLASK_ENV", "development")
flask_app = create_app(env)

if __name__ == "__main__":
    host  = os.getenv("FLASK_HOST", "0.0.0.0")
    port  = int(os.getenv("FLASK_PORT", 5000))
    debug = (env == "development")

    print("=" * 55)
    print("        IFRI_MentorLink — Serveur Flask")
    print("=" * 55)
    print(f"  Environnement : {env}")
    print(f"  Adresse       : http://localhost:{port}")
    print(f"  Debug         : {debug}")
    print(f"  Base de données : {os.getenv('DATABASE_URL', 'non définie !')}")
    print("=" * 55)

    flask_app.run(host=host, port=port, debug=debug)

