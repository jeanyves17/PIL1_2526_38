-- 0. Nettoyage (suppression dans l'ordre inverse des dépendances)

DROP TABLE IF EXISTS messages                  CASCADE;
DROP TABLE IF EXISTS conversations             CASCADE;
DROP TABLE IF EXISTS resultats_correspondance  CASCADE;
DROP TABLE IF EXISTS sessions_mentorat         CASCADE;
DROP TABLE IF EXISTS reponses_mentorat         CASCADE;
DROP TABLE IF EXISTS demandes_mentorat         CASCADE;
DROP TABLE IF EXISTS offres_mentorat           CASCADE;
DROP TABLE IF EXISTS creneaux_offre            CASCADE;
DROP TABLE IF EXISTS competences_offre         CASCADE;
DROP TABLE IF EXISTS creneaux_demande          CASCADE;
DROP TABLE IF EXISTS competences_demande       CASCADE;
DROP TABLE IF EXISTS disponibilites_utilisateur CASCADE;
DROP TABLE IF EXISTS lacunes_utilisateur       CASCADE;
DROP TABLE IF EXISTS competences_utilisateur   CASCADE;
DROP TABLE IF EXISTS competences               CASCADE;
DROP TABLE IF EXISTS creneaux_horaires         CASCADE;
DROP TABLE IF EXISTS utilisateurs              CASCADE;
DROP TABLE IF EXISTS filieres                  CASCADE;
DROP TYPE  IF EXISTS niveau_etudes             CASCADE;
DROP TYPE  IF EXISTS format_session            CASCADE;
DROP TYPE  IF EXISTS statut_demande            CASCADE;
DROP TYPE  IF EXISTS statut_offre              CASCADE;
DROP TYPE  IF EXISTS statut_conversation       CASCADE;


-- 1. TYPES ÉNUMÉRÉS


-- Niveaux d'études possibles
CREATE TYPE niveau_etudes AS ENUM (
    'Licence 1', 'Licence 2', 'Licence 3',
    'Master 1',  'Master 2'
);

-- Format d'une session de mentorat
CREATE TYPE format_session AS ENUM (
    'présentiel', 'en ligne', 'les deux'
);

-- Statut d'une demande de mentorat
CREATE TYPE statut_demande AS ENUM (
    'ouverte', 'en cours', 'clôturée', 'annulée'
);

-- Statut d'une offre de mentorat
CREATE TYPE statut_offre AS ENUM (
    'ouverte', 'en cours', 'clôturée', 'annulée'
);

-- Statut d'une conversation
CREATE TYPE statut_conversation AS ENUM (
    'active', 'archivée'
);


-- 2. FILIÈRES


CREATE TABLE filieres (
    id          SERIAL       PRIMARY KEY,
    code        VARCHAR(20)  NOT NULL UNIQUE,   -- ex. 'IA', 'GL', 'SI'
    intitule    VARCHAR(100) NOT NULL            -- ex. 'Intelligence Artificielle'
);

-- Données de base des filières de l'IFRI
INSERT INTO filieres (code, intitule) VALUES
    ('IA',     'Intelligence Artificielle'),
    ('IM',     'Ingénierie Mathématique'),
    ('GL',     'Génie Logiciel'),
    ('SE_IoT', 'Systèmes Embarqués & IoT'),
    ('SI',     'Systèmes d''Information');


-- 3. UTILISATEURS


CREATE TABLE utilisateurs (
    id                  SERIAL        PRIMARY KEY,
    nom                 VARCHAR(100)  NOT NULL,
    prenom              VARCHAR(100)  NOT NULL,
    email               VARCHAR(255)  NOT NULL UNIQUE,
    telephone           VARCHAR(20)   NOT NULL UNIQUE,
    mot_de_passe_hash   VARCHAR(255)  NOT NULL,           -- stocké en bcrypt/argon2, jamais en clair
    filiere_id          INT           REFERENCES filieres(id) ON DELETE SET NULL,
    niveau              niveau_etudes,
    photo_url           VARCHAR(500),                     -- chemin ou URL de la photo de profil
    biographie          TEXT,                             -- courte présentation
    centres_interet     TEXT,                             -- centres d'intérêt académiques
    jeton_reinitialisation  VARCHAR(255),                 -- pour réinitialiser le mot de passe
    expiration_jeton        TIMESTAMPTZ,                  -- date d'expiration du jeton
    est_actif           BOOLEAN       NOT NULL DEFAULT TRUE,
    cree_le             TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    modifie_le          TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- Index pour accélérer les recherches fréquentes
CREATE INDEX idx_utilisateurs_email     ON utilisateurs(email);
CREATE INDEX idx_utilisateurs_telephone ON utilisateurs(telephone);
CREATE INDEX idx_utilisateurs_filiere   ON utilisateurs(filiere_id);


-- 4. COMPÉTENCES / MATIÈRES


CREATE TABLE competences (
    id          SERIAL       PRIMARY KEY,
    intitule    VARCHAR(150) NOT NULL,
    categorie   VARCHAR(100),                    -- ex. 'Programmation', 'Mathématiques'
    cree_par    INT          REFERENCES utilisateurs(id) ON DELETE SET NULL,
    -- Index unique insensible à la casse pour éviter les doublons (ex. 'python' et 'Python')
    CONSTRAINT competences_intitule_unique UNIQUE (intitule)
);

CREATE UNIQUE INDEX idx_competences_intitule_lower ON competences(LOWER(intitule));

-- Points forts d'un utilisateur (compétences maîtrisées)
CREATE TABLE competences_utilisateur (
    id              SERIAL  PRIMARY KEY,
    utilisateur_id  INT     NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    competence_id   INT     NOT NULL REFERENCES competences(id)  ON DELETE CASCADE,
    UNIQUE (utilisateur_id, competence_id)
);

-- Lacunes d'un utilisateur (matières où il a besoin d'aide)
CREATE TABLE lacunes_utilisateur (
    id              SERIAL  PRIMARY KEY,
    utilisateur_id  INT     NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    competence_id   INT     NOT NULL REFERENCES competences(id)  ON DELETE CASCADE,
    UNIQUE (utilisateur_id, competence_id)
);


-- 5. CRÉNEAUX HORAIRES & DISPONIBILITÉS


-- Plages horaires de référence (ex. Lundi 8h-10h)
CREATE TABLE creneaux_horaires (
    id           SERIAL   PRIMARY KEY,
    jour_semaine SMALLINT NOT NULL CHECK (jour_semaine BETWEEN 1 AND 7),
    -- 1 = Lundi, 2 = Mardi, ..., 7 = Dimanche
    heure_debut  TIME     NOT NULL,
    heure_fin    TIME     NOT NULL,
    CHECK (heure_fin > heure_debut)
);

-- Disponibilités hebdomadaires habituelles d'un utilisateur
CREATE TABLE disponibilites_utilisateur (
    id              SERIAL  PRIMARY KEY,
    utilisateur_id  INT     NOT NULL REFERENCES utilisateurs(id)     ON DELETE CASCADE,
    creneau_id      INT     NOT NULL REFERENCES creneaux_horaires(id) ON DELETE CASCADE,
    UNIQUE (utilisateur_id, creneau_id)
);


-- 6. OFFRES ET DEMANDES DE MENTORAT


-- Offres : un mentor propose de l'aide
CREATE TABLE offres_mentorat (
    id              SERIAL         PRIMARY KEY,
    mentor_id       INT            NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    description     TEXT,
    format          format_session NOT NULL DEFAULT 'les deux',
    statut          statut_offre   NOT NULL DEFAULT 'ouverte',
    cree_le         TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    modifie_le      TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);

-- Compétences proposées dans une offre (relation N-N)
CREATE TABLE competences_offre (
    offre_id        INT NOT NULL REFERENCES offres_mentorat(id) ON DELETE CASCADE,
    competence_id   INT NOT NULL REFERENCES competences(id)     ON DELETE CASCADE,
    PRIMARY KEY (offre_id, competence_id)
);

-- Créneaux horaires proposés dans une offre
CREATE TABLE creneaux_offre (
    offre_id    INT NOT NULL REFERENCES offres_mentorat(id)   ON DELETE CASCADE,
    creneau_id  INT NOT NULL REFERENCES creneaux_horaires(id) ON DELETE CASCADE,
    PRIMARY KEY (offre_id, creneau_id)
);

-- Demandes : un mentoré cherche de l'aide
CREATE TABLE demandes_mentorat (
    id              SERIAL          PRIMARY KEY,
    mentore_id      INT             NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    description     TEXT,
    format          format_session  NOT NULL DEFAULT 'les deux',
    statut          statut_demande  NOT NULL DEFAULT 'ouverte',
    cree_le         TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    modifie_le      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

-- Compétences recherchées dans une demande
CREATE TABLE competences_demande (
    demande_id      INT NOT NULL REFERENCES demandes_mentorat(id) ON DELETE CASCADE,
    competence_id   INT NOT NULL REFERENCES competences(id)       ON DELETE CASCADE,
    PRIMARY KEY (demande_id, competence_id)
);

-- Créneaux horaires souhaités dans une demande
CREATE TABLE creneaux_demande (
    demande_id  INT NOT NULL REFERENCES demandes_mentorat(id) ON DELETE CASCADE,
    creneau_id  INT NOT NULL REFERENCES creneaux_horaires(id) ON DELETE CASCADE,
    PRIMARY KEY (demande_id, creneau_id)
);


-- 7. RÉPONSES AUX OFFRES / DEMANDES

-- Un utilisateur répond à une offre ou une demande existante.
-- Exactement l'un des deux (offre_id ou demande_id) doit être renseigné.

CREATE TABLE reponses_mentorat (
    id              SERIAL      PRIMARY KEY,
    repondant_id    INT         NOT NULL REFERENCES utilisateurs(id)   ON DELETE CASCADE,
    offre_id        INT         REFERENCES offres_mentorat(id)         ON DELETE CASCADE,
    demande_id      INT         REFERENCES demandes_mentorat(id)       ON DELETE CASCADE,
    message         TEXT,
    acceptee        BOOLEAN,    -- NULL = en attente, TRUE = acceptée, FALSE = refusée
    cree_le         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- Une seule réponse par utilisateur par offre ou demande
    UNIQUE (repondant_id, offre_id),
    UNIQUE (repondant_id, demande_id),
    -- Contrainte : soit offre_id, soit demande_id, pas les deux
    CHECK (
        (offre_id IS NOT NULL AND demande_id IS NULL) OR
        (offre_id IS NULL AND demande_id IS NOT NULL)
    )
);


-- 8. ALGORITHME DE CORRESPONDANCE – RÉSULTATS


CREATE TABLE resultats_correspondance (
    id                      SERIAL       PRIMARY KEY,
    mentor_id               INT          NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    mentore_id              INT          NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    score_competences       NUMERIC(5,2) NOT NULL DEFAULT 0,  -- compatibilité des compétences (0-100)
    score_disponibilites    NUMERIC(5,2) NOT NULL DEFAULT 0,  -- compatibilité des horaires    (0-100)
    score_filiere           NUMERIC(5,2) NOT NULL DEFAULT 0,  -- proximité filière/niveau      (0-100)
    -- Score total calculé automatiquement : 50% compétences + 30% horaires + 20% filière
    score_total             NUMERIC(5,2) GENERATED ALWAYS AS (
                                ROUND(score_competences * 0.50 + score_disponibilites * 0.30 + score_filiere * 0.20, 2)
                            ) STORED,
    calcule_le              TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    -- Un mentor ne peut pas être son propre mentoré
    CHECK (mentor_id <> mentore_id),
    UNIQUE (mentor_id, mentore_id)
);

-- Index pour trier rapidement par score décroissant
CREATE INDEX idx_correspondance_score ON resultats_correspondance(score_total DESC);


-- 9. SESSIONS DE MENTORAT


CREATE TABLE sessions_mentorat (
    id                  SERIAL         PRIMARY KEY,
    mentor_id           INT            NOT NULL REFERENCES utilisateurs(id)            ON DELETE CASCADE,
    mentore_id          INT            NOT NULL REFERENCES utilisateurs(id)            ON DELETE CASCADE,
    correspondance_id   INT            REFERENCES resultats_correspondance(id)         ON DELETE SET NULL,
    planifiee_le        TIMESTAMPTZ    NOT NULL,               -- date et heure de la session
    duree_minutes       SMALLINT       NOT NULL DEFAULT 60 CHECK (duree_minutes > 0),
    format              format_session NOT NULL DEFAULT 'en ligne',
    notes               TEXT,
    est_terminee        BOOLEAN        NOT NULL DEFAULT FALSE,
    cree_le             TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);


-- 10. MESSAGERIE


-- Une conversation regroupe exactement deux utilisateurs
CREATE TABLE conversations (
    id              SERIAL              PRIMARY KEY,
    utilisateur1_id INT                 NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    utilisateur2_id INT                 NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    statut          statut_conversation NOT NULL DEFAULT 'active',
    cree_le         TIMESTAMPTZ         NOT NULL DEFAULT NOW(),
    -- utilisateur1_id toujours inférieur à utilisateur2_id pour éviter les doublons
    CHECK (utilisateur1_id < utilisateur2_id),
    UNIQUE (utilisateur1_id, utilisateur2_id)
);

CREATE TABLE messages (
    id              SERIAL      PRIMARY KEY,
    conversation_id INT         NOT NULL REFERENCES conversations(id)  ON DELETE CASCADE,
    expediteur_id   INT         NOT NULL REFERENCES utilisateurs(id)   ON DELETE CASCADE,
    contenu         TEXT        NOT NULL CHECK (TRIM(contenu) <> ''),  -- message non vide
    est_lu          BOOLEAN     NOT NULL DEFAULT FALSE,
    envoye_le       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index pour charger rapidement l'historique d'une conversation
CREATE INDEX idx_messages_conversation ON messages(conversation_id, envoye_le DESC);
CREATE INDEX idx_messages_expediteur   ON messages(expediteur_id);
-- Index partiel : uniquement les messages non lus (pour les notifications)
CREATE INDEX idx_messages_non_lus      ON messages(conversation_id) WHERE est_lu = FALSE;


-- 11. TRIGGER – mise à jour automatique de modifie_le


-- Fonction appelée automatiquement avant chaque UPDATE
CREATE OR REPLACE FUNCTION maj_modifie_le()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.modifie_le = NOW();  -- met à jour la date de modification
    RETURN NEW;              -- applique la modification
END;
$$;

-- Trigger sur la table utilisateurs
CREATE TRIGGER declencheur_utilisateurs_modifie
    BEFORE UPDATE ON utilisateurs
    FOR EACH ROW EXECUTE FUNCTION maj_modifie_le();

-- Trigger sur la table offres_mentorat
CREATE TRIGGER declencheur_offres_modifie
    BEFORE UPDATE ON offres_mentorat
    FOR EACH ROW EXECUTE FUNCTION maj_modifie_le();

-- Trigger sur la table demandes_mentorat
CREATE TRIGGER declencheur_demandes_modifie
    BEFORE UPDATE ON demandes_mentorat
    FOR EACH ROW EXECUTE FUNCTION maj_modifie_le();


-- 12. VUES UTILES


-- Vue : profil complet d'un utilisateur avec sa filière
CREATE OR REPLACE VIEW vue_profils_utilisateurs AS
SELECT
    u.id,
    u.nom,
    u.prenom,
    u.email,
    u.telephone,
    u.photo_url,
    u.biographie,
    u.centres_interet,
    u.niveau,
    f.code      AS code_filiere,
    f.intitule  AS filiere,
    u.est_actif,
    u.cree_le
FROM utilisateurs u
LEFT JOIN filieres f ON f.id = u.filiere_id;

-- Vue : offres de mentorat ouvertes avec infos du mentor
CREATE OR REPLACE VIEW vue_offres_ouvertes AS
SELECT
    o.id            AS offre_id,
    o.description,
    o.format,
    o.statut,
    o.cree_le,
    u.id            AS mentor_id,
    u.prenom        AS mentor_prenom,
    u.nom           AS mentor_nom,
    u.photo_url,
    f.intitule      AS filiere_mentor,
    u.niveau        AS niveau_mentor
FROM offres_mentorat o
JOIN utilisateurs u     ON u.id = o.mentor_id
LEFT JOIN filieres f    ON f.id = u.filiere_id
WHERE o.statut = 'ouverte';

-- Vue : demandes de mentorat ouvertes avec infos du mentoré
CREATE OR REPLACE VIEW vue_demandes_ouvertes AS
SELECT
    d.id            AS demande_id,
    d.description,
    d.format,
    d.statut,
    d.cree_le,
    u.id            AS mentore_id,
    u.prenom        AS mentore_prenom,
    u.nom           AS mentore_nom,
    u.photo_url,
    f.intitule      AS filiere_mentore,
    u.niveau        AS niveau_mentore
FROM demandes_mentorat d
JOIN utilisateurs u     ON u.id = d.mentore_id
LEFT JOIN filieres f    ON f.id = u.filiere_id
WHERE d.statut = 'ouverte';

-- Vue : meilleures correspondances (score >= 50), triées par score décroissant
CREATE OR REPLACE VIEW vue_meilleures_correspondances AS
SELECT
    c.id,
    c.score_total,
    c.score_competences,
    c.score_disponibilites,
    c.score_filiere,
    c.calcule_le,
    -- Informations du mentor
    mentor.id           AS mentor_id,
    mentor.prenom       AS mentor_prenom,
    mentor.nom          AS mentor_nom,
    mentor.photo_url    AS mentor_photo,
    fm.intitule         AS mentor_filiere,
    mentor.niveau       AS mentor_niveau,
    -- Informations du mentoré
    mentore.id          AS mentore_id,
    mentore.prenom      AS mentore_prenom,
    mentore.nom         AS mentore_nom,
    mentore.photo_url   AS mentore_photo,
    fme.intitule        AS mentore_filiere,
    mentore.niveau      AS mentore_niveau
FROM resultats_correspondance c
JOIN utilisateurs mentor    ON mentor.id  = c.mentor_id
JOIN utilisateurs mentore   ON mentore.id = c.mentore_id
LEFT JOIN filieres fm       ON fm.id  = mentor.filiere_id
LEFT JOIN filieres fme      ON fme.id = mentore.filiere_id
WHERE c.score_total >= 50
ORDER BY c.score_total DESC;

-- Vue : messages non lus avec expéditeur et destinataire
CREATE OR REPLACE VIEW vue_messages_non_lus AS
SELECT
    conv.id             AS conversation_id,
    msg.id              AS message_id,
    msg.contenu,
    msg.envoye_le,
    exp.id              AS expediteur_id,
    exp.prenom          AS expediteur_prenom,
    exp.nom             AS expediteur_nom,
    -- Le destinataire est l'autre participant de la conversation
    CASE
        WHEN conv.utilisateur1_id = msg.expediteur_id THEN conv.utilisateur2_id
        ELSE conv.utilisateur1_id
    END AS destinataire_id
FROM messages msg
JOIN conversations conv ON conv.id = msg.conversation_id
JOIN utilisateurs exp   ON exp.id  = msg.expediteur_id
WHERE msg.est_lu = FALSE;




