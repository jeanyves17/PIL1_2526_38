-- =============================================================
--  IFRI_MentorLink – Données de test (seed.sql)
--  Matières basées sur le programme officiel L1 S1 IFRI
--  À exécuter APRÈS schema.sql
-- =============================================================

-- -------------------------------------------------------------
-- 1. CRÉNEAUX HORAIRES
-- -------------------------------------------------------------
INSERT INTO creneaux_horaires (jour_semaine, heure_debut, heure_fin) VALUES
    (1, '08:00', '10:00'),  -- Lundi    8h-10h
    (1, '10:00', '12:00'),  -- Lundi   10h-12h
    (1, '14:00', '16:00'),  -- Lundi   14h-16h
    (2, '08:00', '10:00'),  -- Mardi    8h-10h
    (2, '14:00', '16:00'),  -- Mardi   14h-16h
    (3, '10:00', '12:00'),  -- Mercredi 10h-12h
    (3, '16:00', '18:00'),  -- Mercredi 16h-18h
    (4, '08:00', '10:00'),  -- Jeudi    8h-10h
    (4, '14:00', '16:00'),  -- Jeudi   14h-16h
    (5, '10:00', '12:00'),  -- Vendredi 10h-12h
    (6, '09:00', '11:00'),  -- Samedi   9h-11h
    (6, '14:00', '16:00');  -- Samedi  14h-16h

-- -------------------------------------------------------------
-- 2. UTILISATEURS
-- Mots de passe tous "Azerty123!" hashés en bcrypt (simulé)
-- -------------------------------------------------------------
INSERT INTO utilisateurs (nom, prenom, email, telephone, mot_de_passe_hash, filiere_id, niveau, biographie, centres_interet) VALUES
    -- Mentor fort en Programmation et Maths (GL - L2)
    ('AGOSSA',    'Koffi',     'koffi.agossa@etud.ifri-uac.bj',     '+22961000001', '$2b$12$hashed_password_1', 3, 'Licence 2',
     'En L2 GL, je maîtrise la programmation et les maths de L1. Disponible pour aider les L1.',
     'Algorithmique, Développement logiciel, Open source'),

    -- Mentorée faible en Maths (IA - L1)
    ('DOSSOU',    'Aïcha',     'aicha.dossou@etud.ifri-uac.bj',     '+22961000002', '$2b$12$hashed_password_2', 1, 'Licence 1',
     'Étudiante en L1 IA. J''ai du mal avec les maths et la logique.',
     'Intelligence artificielle, Data Science'),

    -- Mentor fort en Maths et Réseaux (IM - L3)
    ('HOUNSOU',   'Romaric',   'romaric.hounsou@etud.ifri-uac.bj',  '+22961000003', '$2b$12$hashed_password_3', 2, 'Licence 3',
     'L3 IM. Je peux aider en mathématiques, probabilités et architecture réseaux.',
     'Mathématiques, Recherche opérationnelle'),

    -- Mentoré faible en Programmation (SI - L1)
    ('TOSSOU',    'Merveille', 'merveille.tossou@etud.ifri-uac.bj', '+22961000004', '$2b$12$hashed_password_4', 5, 'Licence 1',
     'L1 SI. Débutant en programmation, je cherche de l''aide en Langage C et Algorithmique.',
     'Systèmes d''information, Gestion'),

    -- Mentor fort en Systèmes (SE_IoT - L2)
    ('VODOUNOU',  'Brice',     'brice.vodounou@etud.ifri-uac.bj',   '+22961000005', '$2b$12$hashed_password_5', 4, 'Licence 2',
     'L2 SE&IoT. Je maîtrise les systèmes d''exploitation et les réseaux informatiques.',
     'IoT, Electronique, Systèmes embarqués'),

    -- Mentorée faible en Systèmes et Réseaux (GL - L1)
    ('AZONDEKON', 'Faridath',  'faridath.azondekon@etud.ifri-uac.bj','+22961000006', '$2b$12$hashed_password_6', 3, 'Licence 1',
     'L1 GL. J''ai des difficultés en architecture réseaux et systèmes d''exploitation.',
     'Génie logiciel, Conception');

-- -------------------------------------------------------------
-- 3. COMPÉTENCES — matières officielles du programme L1 S1 IFRI
-- -------------------------------------------------------------
INSERT INTO competences (intitule, categorie, cree_par) VALUES
    -- MTH1121
    ('Logique et arithmétique',             'Mathématiques',  1),
    -- MTH1122
    ('Mathématiques fondamentales',         'Mathématiques',  3),
    -- MTH1123
    ('Probabilité et statistique',          'Mathématiques',  3),
    -- INF1124
    ('Architecture et topologie des réseaux','Informatique',  5),
    -- INF1125 EC1 : Outils de base en informatique
    ('Outils de base en informatique',      'Informatique',   5),
    -- INF1125 EC2 : Systèmes d exploitation
    ('Systemes d exploitation',            'Informatique',   5),
    -- INF1126 EC1 : Algorithmique
    ('Algorithmique',                       'Programmation',  1),
    -- INF1126 EC2 : Langage C
    ('Langage C',                           'Programmation',  1),
    -- DRP1127
    ('Déontologie et droit liés aux TIC',   'Culture générale',4),
    -- TCC1128
    ('Techniques d''expression écrite et orale','Méthodologie',4);

-- -------------------------------------------------------------
-- 4. POINTS FORTS DES UTILISATEURS
-- -------------------------------------------------------------
INSERT INTO competences_utilisateur (utilisateur_id, competence_id) VALUES
    -- Koffi (L2 GL) : maîtrise tout le programme L1
    (1, 1), (1, 2), (1, 3), (1, 7), (1, 8),
    -- Romaric (L3 IM) : fort en Maths et Réseaux
    (3, 1), (3, 2), (3, 3), (3, 4),
    -- Brice (L2 SE_IoT) : fort en Systèmes et Réseaux
    (5, 4), (5, 5), (5, 6),
    -- Aïcha : forte en TCC uniquement pour l instant
    (2, 10),
    -- Faridath : forte en expression écrite
    (6, 10);

-- -------------------------------------------------------------
-- 5. LACUNES DES UTILISATEURS
-- -------------------------------------------------------------
INSERT INTO lacunes_utilisateur (utilisateur_id, competence_id) VALUES
    -- Aïcha : lacunes en Logique, Maths fondamentales, Proba
    (2, 1), (2, 2), (2, 3),
    -- Merveille : lacunes en Algorithmique, Langage C, Outils de base
    (4, 7), (4, 8), (4, 5),
    -- Faridath : lacunes en Réseaux, Systemes d exploitation
    (6, 4), (6, 6),
    -- Koffi : lacune en Déontologie TIC
    (1, 9),
    -- Brice : lacune en Probabilité et statistique
    (5, 3);

-- -------------------------------------------------------------
-- 6. DISPONIBILITÉS DES UTILISATEURS
-- -------------------------------------------------------------
INSERT INTO disponibilites_utilisateur (utilisateur_id, creneau_id) VALUES
    -- Koffi : Lundi 8h, Mercredi 10h, Vendredi 10h
    (1, 1), (1, 6), (1, 10),
    -- Aïcha : Lundi 8h, Lundi 14h, Mardi 14h
    (2, 1), (2, 3), (2, 5),
    -- Romaric : Mardi 8h, Jeudi 8h, Samedi 9h
    (3, 4), (3, 8), (3, 11),
    -- Merveille : Lundi 10h, Mercredi 16h
    (4, 2), (4, 7),
    -- Brice : Lundi 8h, Jeudi 14h, Samedi 14h
    (5, 1), (5, 9), (5, 12),
    -- Faridath : Lundi 8h, Mardi 14h
    (6, 1), (6, 5);

-- -------------------------------------------------------------
-- 7. OFFRES DE MENTORAT
-- -------------------------------------------------------------
INSERT INTO offres_mentorat (mentor_id, description, format, statut) VALUES
    -- Koffi propose Algorithmique + Langage C
    (1, 'Je propose des sessions d''Algorithmique et Langage C pour les L1. Exercices pratiques et corrections détaillées.', 'les deux', 'ouverte'),
    -- Romaric propose les Maths L1
    (3, 'Disponible pour réviser Logique, Maths fondamentales et Probabilités. Idéal avant les examens.', 'en ligne', 'ouverte'),
    -- Brice propose Systèmes et Réseaux
    (5, 'Je peux aider en Architecture réseaux et Systemes d exploitation. TP guidés sous Linux.', 'présentiel', 'ouverte');

-- Compétences liées aux offres
INSERT INTO competences_offre (offre_id, competence_id) VALUES
    (1, 7), (1, 8),         -- Offre Koffi   : Algorithmique + Langage C
    (2, 1), (2, 2), (2, 3), -- Offre Romaric : Logique + Maths + Proba
    (3, 4), (3, 6);         -- Offre Brice   : Réseaux + Systemes d exploitation

-- Créneaux liés aux offres
INSERT INTO creneaux_offre (offre_id, creneau_id) VALUES
    (1, 1), (1, 6),  -- Offre Koffi   : Lundi 8h + Mercredi 10h
    (2, 4), (2, 8),  -- Offre Romaric : Mardi 8h + Jeudi 8h
    (3, 1), (3, 9);  -- Offre Brice   : Lundi 8h + Jeudi 14h

-- -------------------------------------------------------------
-- 8. DEMANDES DE MENTORAT
-- -------------------------------------------------------------
INSERT INTO demandes_mentorat (mentore_id, description, format, statut) VALUES
    -- Aïcha cherche aide en Maths
    (2, 'J''ai du mal avec la logique et les probabilités. Mes examens approchent, besoin d''aide urgente.', 'en ligne', 'ouverte'),
    -- Merveille cherche aide en Programmation
    (4, 'Débutant complet en Langage C et Algorithmique. Cherche quelqu''un de patient.', 'les deux', 'ouverte'),
    -- Faridath cherche aide en Réseaux et Systèmes
    (6, 'J''ai du mal à comprendre les cours de réseaux et de systèmes d''exploitation. Besoin de TP pratiques.', 'présentiel', 'ouverte');

-- Compétences liées aux demandes
INSERT INTO competences_demande (demande_id, competence_id) VALUES
    (1, 1), (1, 3),  -- Demande Aïcha     : Logique + Proba
    (2, 7), (2, 8),  -- Demande Merveille : Algorithmique + Langage C
    (3, 4), (3, 6);  -- Demande Faridath  : Réseaux + Systèmes

-- Créneaux liés aux demandes
INSERT INTO creneaux_demande (demande_id, creneau_id) VALUES
    (1, 1), (1, 5),  -- Demande Aïcha     : Lundi 8h + Mardi 14h
    (2, 2), (2, 7),  -- Demande Merveille : Lundi 10h + Mercredi 16h
    (3, 1), (3, 5);  -- Demande Faridath  : Lundi 8h + Mardi 14h

-- -------------------------------------------------------------
-- 9. RÉPONSES AUX OFFRES / DEMANDES
-- -------------------------------------------------------------
INSERT INTO reponses_mentorat (repondant_id, offre_id, demande_id, message, acceptee) VALUES
    -- Aïcha répond à l offre de Romaric (Maths)
    (2, 2, NULL, 'Bonjour Romaric ! Ton offre correspond exactement à ce dont j''ai besoin avant les examens.', NULL),
    -- Merveille répond à l offre de Koffi (Algo + C)
    (4, 1, NULL, 'Bonjour Koffi, je suis intéressé par tes sessions Algorithmique et Langage C.', NULL),
    -- Koffi répond à la demande de Faridath (Réseaux)
    (1, NULL, 3, 'Je connais bien les bases des réseaux, je peux t''aider même si ce n''est pas ma spécialité principale.', FALSE),
    -- Brice répond à la demande de Faridath (Réseaux + Systèmes)
    (5, NULL, 3, 'C''est exactement ma spécialité ! Je peux t''aider avec des TP pratiques sous Linux.', TRUE),
    -- Romaric répond à la demande d Aïcha (Maths)
    (3, NULL, 1, 'Avec plaisir ! On peut commencer par la logique arithmétique dès cette semaine.', TRUE);

-- -------------------------------------------------------------
-- 10. RÉSULTATS DE CORRESPONDANCE
-- -------------------------------------------------------------
INSERT INTO resultats_correspondance (mentor_id, mentore_id, score_competences, score_disponibilites, score_filiere) VALUES
    -- Koffi → Merveille : Algo+C en commun, filières différentes, peu de créneaux communs
    (1, 4, 80.00, 40.00, 20.00),
    -- Romaric → Aïcha : Maths en commun, filières proches, créneau commun
    (3, 2, 90.00, 60.00, 60.00),
    -- Brice → Faridath : Réseaux+Systèmes en commun, même filière approximative, créneau commun
    (5, 6, 85.00, 70.00, 60.00),
    -- Koffi → Aïcha : Logique en commun, créneau Lundi 8h commun
    (1, 2, 65.00, 70.00, 40.00),
    -- Romaric → Merveille : peu de compétences communes
    (3, 4, 25.00, 30.00, 20.00);

-- -------------------------------------------------------------
-- 11. SESSIONS DE MENTORAT
-- -------------------------------------------------------------
INSERT INTO sessions_mentorat (mentor_id, mentore_id, correspondance_id, planifiee_le, duree_minutes, format, notes, est_terminee) VALUES
    -- Session Brice → Faridath (déjà terminée)
    (5, 6, 3, NOW() - INTERVAL '3 days', 90, 'présentiel',
     'Introduction aux réseaux : modèle OSI, adressage IP. Faridath a bien suivi.', TRUE),
    -- Session Romaric → Aïcha (planifiée demain)
    (3, 2, 2, NOW() + INTERVAL '1 day', 60, 'en ligne',
     'Révision Logique et arithmétique : tables de vérité, démonstrations.', FALSE),
    -- Session Koffi → Merveille (planifiée cette semaine)
    (1, 4, 1, NOW() + INTERVAL '2 days', 60, 'les deux',
     'Première session Langage C : variables, types, boucles for et while.', FALSE);

-- -------------------------------------------------------------
-- 12. CONVERSATIONS ET MESSAGES
-- -------------------------------------------------------------

-- Conversations (utilisateur1_id toujours < utilisateur2_id)
INSERT INTO conversations (utilisateur1_id, utilisateur2_id, statut) VALUES
    (1, 4, 'active'),  -- Koffi ↔ Merveille
    (2, 3, 'active'),  -- Aïcha ↔ Romaric
    (5, 6, 'active');  -- Brice ↔ Faridath

-- Messages
INSERT INTO messages (conversation_id, expediteur_id, contenu, est_lu, envoye_le) VALUES
    -- Conversation Koffi ↔ Merveille
    (1, 4, 'Bonjour Koffi ! Je bloque totalement sur les pointeurs en Langage C.',                     TRUE,  NOW() - INTERVAL '3 days'),
    (1, 1, 'C''est normal au début ! Les pointeurs c''est le concept le plus difficile du C.',         TRUE,  NOW() - INTERVAL '3 days'),
    (1, 4, 'Tu peux m''expliquer la différence entre * et & ?',                                        TRUE,  NOW() - INTERVAL '2 days'),
    (1, 1, '* déclare un pointeur ou déréférence, & donne l''adresse. On verra ça en session !',      TRUE,  NOW() - INTERVAL '2 days'),
    (1, 4, 'Super merci ! J''attends notre session avec impatience.',                                   FALSE, NOW() - INTERVAL '1 day'),

    -- Conversation Aïcha ↔ Romaric
    (2, 2, 'Bonjour Romaric, j''ai du mal avec les tables de vérité en Logique.',                     TRUE,  NOW() - INTERVAL '4 days'),
    (2, 3, 'Pas de souci ! C''est une question de méthode. Mardi à 14h on s''appelle sur Meet ?',     TRUE,  NOW() - INTERVAL '4 days'),
    (2, 2, 'Mardi c''est parfait ! Tu peux aussi m''aider pour les probabilités ?',                    TRUE,  NOW() - INTERVAL '3 days'),
    (2, 3, 'Oui bien sûr, on fera Logique + Proba en même session.',                                   FALSE, NOW() - INTERVAL '2 days'),

    -- Conversation Brice ↔ Faridath
    (3, 6, 'Bonjour Brice ! Je n''arrive pas à comprendre le modèle OSI.',                            TRUE,  NOW() - INTERVAL '5 days'),
    (3, 5, 'Le modèle OSI c''est 7 couches. Je t''explique chacune avec des exemples concrets.',      TRUE,  NOW() - INTERVAL '5 days'),
    (3, 6, 'La session était super ! J''ai enfin compris l''adressage IP.',                            TRUE,  NOW() - INTERVAL '2 days'),
    (3, 5, 'Super ! La prochaine fois on attaque les sous-réseaux et le masque CIDR.',                 FALSE, NOW() - INTERVAL '1 day');

-- =============================================================
-- FIN DU SCRIPT SEED
-- =============================================================
