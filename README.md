# GameTracker - Pipeline ETL

## Description du projet

GameTracker est un système de pipeline ETL (Extract, Transform, Load) conçu pour traiter et analyser les données de jeux vidéo. Le projet extrait les données des joueurs et de leurs scores depuis des fichiers CSV, les nettoie et les valide, puis les charge dans une base de données MySQL. Enfin, il génère un rapport de synthèse avec des statistiques détaillées.

## Prérequis techniques

- **Docker** et **Docker Compose** (pour la conteneurisation)
- **Python 3.11** (dans le conteneur)
- **MySQL 8.0** (dans le conteneur)
- **Git** (pour le versionnement)

### Dépendances Python
- pandas==2.1.0
- mysql-connector-python==8.2.0

## Instructions de lancement

1. **Cloner le projet et accéder au répertoire :**
   ```bash
   cd gametracker
   ```

2. **Démarrer les services Docker :**
   ```bash
   docker compose up -d
   ```

3. **Exécuter le pipeline complet :**
   ```bash
   docker compose exec app bash scripts/run_pipeline.sh
   ```

   Ce script effectue automatiquement :
   - Attente de la disponibilité de la base de données
   - Initialisation des tables SQL
   - Exécution du pipeline ETL (extraction, transformation, chargement)
   - Génération du rapport de synthèse

4. **Consulter le rapport généré :**
   Le rapport est disponible dans `data/output/rapport.txt`

## Structure du projet

```
gametracker/
├── data/
│   ├── raw/           # Données sources (Players.csv, Scores.csv)
│   └── output/        # Rapport généré (rapport.txt)
├── scripts/
│   ├── init-db.sql    # Script de création des tables
│   ├── run_pipeline.sh # Script d'automatisation complet
│   └── wait-for-db.sh  # Script d'attente de la DB
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuration de la base de données
│   ├── database.py    # Gestion des connexions DB
│   ├── extract.py     # Extraction des données CSV
│   ├── transform.py   # Transformation et nettoyage des données
│   ├── load.py        # Chargement des données en base
│   ├── report.py      # Génération du rapport de synthèse
│   └── main.py        # Orchestration du pipeline ETL
├── Dockerfile         # Configuration du conteneur application
├── docker-compose.yml # Configuration des services Docker
├── requirements.txt   # Dépendances Python
└── README.md          # Ce fichier
```

## Description des problèmes de qualité traités

### Extraction (Extract)
- **Validation des fichiers** : Vérification de l'existence des fichiers CSV avant extraction
- **Gestion des erreurs** : Gestion des erreurs de lecture de fichiers

### Transformation (Transform) - 7 problèmes de qualité traités
- **Données des joueurs :**
  - 1. Suppression des doublons sur `player_id`
  - 2. Nettoyage des espaces dans les noms d'utilisateur
  - 3. Conversion et validation des dates d'inscription
  - 4. Validation des adresses email (présence de '@')
  - Gestion des valeurs nulles

- **Données des scores :**
  - 5. Suppression des doublons sur `score_id`
  - 6. Conversion des types de données (dates, numériques)
  - 7. Filtrage des scores négatifs ou nuls
  - Validation des `player_id` par rapport aux joueurs existants (intégrité référentielle)
  - Gestion des valeurs manquantes

### Chargement (Load)
- **Contraintes d'intégrité** : Respect de la clé étrangère entre SCORES et PLAYERS
- **Insertion sécurisée** : Utilisation de requêtes préparées pour éviter les injections SQL
- **Gestion des conflits** : Utilisation de `ON DUPLICATE KEY UPDATE` pour gérer les doublons
- **Transactions** : Utilisation de context managers pour garantir l'intégrité des données

### Pipeline global
- **Ordonnancement** : Chargement des joueurs avant les scores (contrainte FK)
- **Gestion d'erreurs** : Arrêt automatique à la première erreur
- **Connexion robuste** : Tentatives multiples de connexion à la base de données
- **Logging** : Messages de progression détaillés à chaque étape

### Rapport de synthèse
- **Statistiques générales** : Nombre de joueurs, scores, jeux distincts
- **Top scores** : Classement des 5 meilleurs scores avec noms de joueurs
- **Moyennes par jeu** : Score moyen pour chaque jeu
- **Répartition géographique** : Nombre de joueurs par pays
- **Analyse par plateforme** : Répartition des sessions de jeu par plateforme