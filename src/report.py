"""Module pour générer le rapport de synthèse."""
import datetime
from database import database_connection


def generate_report():
    """Génère un rapport de synthèse dans output/rapport.txt."""
    with database_connection() as conn:
        cursor = conn.cursor()

        # Statistiques générales
        cursor.execute("SELECT COUNT(*) FROM PLAYERS")
        nb_joueurs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM SCORES")
        nb_scores = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT game) FROM SCORES")
        nb_jeux = cursor.fetchone()[0]

        # Top 5 des meilleurs scores
        cursor.execute("""
            SELECT p.username, s.game, s.score
            FROM SCORES s
            JOIN PLAYERS p ON s.player_id = p.player_id
            ORDER BY s.score DESC
            LIMIT 5
        """)
        top_scores = cursor.fetchall()

        # Score moyen par jeu
        cursor.execute("""
            SELECT game, AVG(score)
            FROM SCORES
            GROUP BY game
        """)
        avg_scores = cursor.fetchall()

        # Répartition des joueurs par pays
        cursor.execute("""
            SELECT country, COUNT(*)
            FROM PLAYERS
            GROUP BY country
        """)
        players_by_country = cursor.fetchall()

        # Répartition des sessions par plateforme
        cursor.execute("""
            SELECT platform, COUNT(*)
            FROM SCORES
            GROUP BY platform
        """)
        sessions_by_platform = cursor.fetchall()

    # Générer le rapport
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"""====================================================
GAMETRACKER - Rapport de synthese
Genere le : {now}
====================================================
--- Statistiques generales ---
Nombre de joueurs : {nb_joueurs}
Nombre de scores : {nb_scores}
Nombre de jeux : {nb_jeux}
--- Top 5 des meilleurs scores ---
"""
    for i, (username, game, score) in enumerate(top_scores, 1):
        report += f"{i}. {username} | {game} | {score}\n"

    report += "--- Score moyen par jeu ---\n"
    for game, avg_score in avg_scores:
        report += f"{game} : {avg_score:.1f}\n"

    report += "--- Joueurs par pays ---\n"
    for country, count in players_by_country:
        report += f"{country} : {count}\n"

    report += "--- Sessions par plateforme ---\n"
    for platform, count in sessions_by_platform:
        report += f"{platform} : {count}\n"

    report += "====================================================\n"

    # Écrire dans le fichier
    with open("output/rapport.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("Rapport généré dans output/rapport.txt")