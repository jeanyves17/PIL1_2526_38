-- IFRI_MentorLink - Schéma SQLite (dev local)
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nom TEXT NOT NULL,
  prenom TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  telephone TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  filiere TEXT,
  niveau TEXT,
  bio TEXT,
  photo_url TEXT,
  disponibilites TEXT,  -- ex: "lundi-matin,mardi-soir"
  competences TEXT,     -- liste séparée par des virgules
  lacunes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL
);

CREATE TABLE offres (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK(type IN ('offre','demande')),
  matiere TEXT NOT NULL,
  description TEXT,
  disponibilites TEXT,
  format TEXT CHECK(format IN ('presentiel','en_ligne','les_deux')) DEFAULT 'les_deux',
  created_at TEXT NOT NULL
);

CREATE TABLE conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_a INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  user_b INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL,
  UNIQUE(user_a, user_b)
);

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  contenu TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE INDEX idx_messages_conv ON messages(conversation_id, id);
CREATE INDEX idx_offres_type ON offres(type);
