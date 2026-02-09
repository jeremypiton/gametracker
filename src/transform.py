import pandas as pd

# ============== TRANSFORM ==============
def transform_players(df: pd.DataFrame) -> pd.DataFrame:
    """Transforme et nettoie les données des joueurs.

    Args:
        df: DataFrame brut des joueurs.

    Returns:
        DataFrame nettoyé.
    """
    df = df.copy()
    # 1. Supprimer les doublons sur player_id
    df = df.drop_duplicates(subset=['player_id'])
    # 2. Nettoyer les espaces des username (strip)
    df['username'] = df['username'].str.strip()
    # 3. Convertir les dates d’inscription (pd.to_datetime, errors=’coerce’)
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
    # Remplacer NaT par None pour MySQL
    df['registration_date'] = df['registration_date'].where(df['registration_date'].notna(), None)
    # 4. Remplacer les emails invalides (sans @) par None
    df['email'] = df['email'].where(df['email'].str.contains('@', na=False), None)
    print(f"Transformé {len(df)} joueurs")
    return df


def transform_scores(df: pd.DataFrame, valid_player_ids) -> pd.DataFrame:
    """Transforme et nettoie les données des scores.

    Args:
        df: DataFrame brut des scores.
        valid_player_ids: Liste des player_id valides.

    Returns:
        DataFrame nettoyé.
    """
    df = df.copy()
    # 1. Supprimer les doublons sur score_id
    df = df.drop_duplicates(subset=['score_id'])
    # 2. Convertir les dates et les scores en types numériques appropriés
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')
    # 3. Supprimer les lignes avec un score négatif ou nul
    df = df[df['score'] > 0]
    # 4. Supprimer les scores dont le player_id n’est pas dans valid_player_ids
    df = df[df['player_id'].isin(valid_player_ids)]
    print(f"Transformé {len(df)} scores")
    return df