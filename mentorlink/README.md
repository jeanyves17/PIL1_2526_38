# IFRI_MentorLink

Application web de mise en relation mentor / mentoré pour les étudiants de l'IFRI
(Université d'Abomey-Calavi). Projet intégrateur 2025-2026.

## Stack
- **Frontend** : HTML / CSS / JavaScript (vanilla, sans framework)
- **Backend** : Python 3 + Flask
- **Base de données** : SQLite (dev local) — schéma MySQL fourni pour la production

## Modules livrés
1. Gestion des comptes & profils (inscription, connexion, profil éditable, mot de passe hashé PBKDF2)
2. Offres / demandes de mentorat + recherche
3. Algorithme de matching (compétences ∩ lacunes, disponibilités, filière)
4. Messagerie instantanée (polling 2,5 s) + bouton **Contacter** depuis les résultats de matching ET les offres

## Structure
```
mentorlink/
├── backend/
│   ├── app.py              # Serveur Flask + API REST
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/                 # api, auth, profil, offres, match, messages, app
├── database/
│   ├── schema_sqlite.sql   # Utilisé automatiquement au démarrage
│   └── schema_mysql.sql    # Pour déploiement production
└── README.md
```

## Démarrage rapide (local)
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Ouvrir <http://localhost:5000>

La base SQLite `mentorlink.db` est créée automatiquement au premier lancement
à partir de `database/schema_sqlite.sql`.

## Déploiement avec MySQL
1. Importer `database/schema_mysql.sql` dans MySQL.
2. Adapter `backend/app.py` pour utiliser `mysql-connector-python` ou
   `SQLAlchemy` à la place de `sqlite3` (les requêtes sont compatibles SQL standard).

## API principales
| Méthode | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Inscription |
| POST | /api/login | Connexion (email ou téléphone) |
| GET/PUT | /api/me | Profil courant |
| GET/POST | /api/offres | Lister / publier offres & demandes |
| GET | /api/match | Profils compatibles (matching) |
| POST | /api/conversations | Ouvrir une conversation avec un utilisateur |
| GET | /api/conversations | Liste des conversations |
| GET/POST | /api/conversations/:id/messages | Lire / envoyer des messages |

## Auteurs
Groupe IFRI — Projet intégrateur 2025-2026.
