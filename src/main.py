#!/usr/bin/env python3
"""Script principal pour orchestrer le pipeline ETL complet."""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from extract import extract
from transform import transform_players, transform_scores
from load import load_players, load_scores
from database import database_connection

def main():
    """Orchestre le pipeline ETL complet."""
    print("=== Démarrage du pipeline ETL ===")

    # Chemins des fichiers de données
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    players_file = data_dir / "Players.csv"
    scores_file = data_dir / "Scores.csv"

    try:
        # 1. Extraction des données
        print("1. Extraction des données...")
        players_df = extract(str(players_file))
        scores_df = extract(str(scores_file))

        # 2. Transformation des données
        print("2. Transformation des données...")

        # Transformer les joueurs en premier
        players_transformed = transform_players(players_df)

        # Extraire les player_id valides du DataFrame nettoyé
        valid_player_ids = set(players_transformed['player_id'])

        # Transformer les scores avec les player_id valides
        scores_transformed = transform_scores(scores_df, valid_player_ids)

        # 3. Chargement des données
        print("3. Chargement des données...")
        with database_connection() as conn:
            # Charger les joueurs en premier (contrainte de clé étrangère)
            load_players(players_transformed, conn)

            # Charger les scores ensuite
            load_scores(scores_transformed, conn)

        print("=== Pipeline ETL terminé avec succès ===")

    except Exception as e:
        print(f"Erreur lors de l'exécution du pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()