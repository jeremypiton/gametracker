#!/bin/bash
# Script d'automatisation du pipeline complet
set -e

echo "=== Démarrage du pipeline ==="

echo "1. Attente de la base de données..."
./scripts/wait-for-db.sh

echo "2. Initialisation des tables..."
mysql --skip-ssl -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < scripts/init-db.sql
echo "Tables initialisées avec succès."

echo "3. Exécution du pipeline ETL..."
python -c "
import sys
sys.path.insert(0, 'src')
from extract import extract
from transform import transform_players, transform_scores
from load import load_players, load_scores
from database import database_connection
from pathlib import Path

# Extraction
players_df = extract('data/raw/Players.csv')
scores_df = extract('data/raw/Scores.csv')

# Transformation
players_transformed = transform_players(players_df)
valid_player_ids = set(players_transformed['player_id'])
scores_transformed = transform_scores(scores_df, valid_player_ids)

# Chargement
with database_connection() as conn:
    load_players(players_transformed, conn)
    load_scores(scores_transformed, conn)

print('Pipeline ETL terminé avec succès')
"

echo "4. Génération du rapport..."
python -c "
import sys
sys.path.insert(0, 'src')
from report import generate_report
generate_report()
"

echo "=== Pipeline terminé avec succès ==="