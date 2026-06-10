-- IFRI_MentorLink - Schéma MySQL/MariaDB (production)
CREATE DATABASE IF NOT EXISTS mentorlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mentorlink;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(80) NOT NULL,
  prenom VARCHAR(80) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  telephone VARCHAR(30) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  filiere VARCHAR(50),
  niveau VARCHAR(20),
  bio TEXT,
  photo_url VARCHAR(255),
  disponibilites VARCHAR(255),
  competences VARCHAR(500),
  lacunes VARCHAR(500),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE sessions (
  token VARCHAR(64) PRIMARY KEY,
  user_id INT NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE offres (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  type ENUM('offre','demande') NOT NULL,
  matiere VARCHAR(150) NOT NULL,
  description TEXT,
  disponibilites VARCHAR(255),
  format ENUM('presentiel','en_ligne','les_deux') DEFAULT 'les_deux',
  created_at DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX(type)
) ENGINE=InnoDB;

CREATE TABLE conversations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_a INT NOT NULL,
  user_b INT NOT NULL,
  created_at DATETIME NOT NULL,
  UNIQUE KEY uniq_pair (user_a, user_b),
  FOREIGN KEY (user_a) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (user_b) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  conversation_id INT NOT NULL,
  sender_id INT NOT NULL,
  contenu TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
  FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX(conversation_id, id)
) ENGINE=InnoDB;
