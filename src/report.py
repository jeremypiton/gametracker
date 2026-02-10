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

        cursor.execute("SELECT MIN(score), MAX(score), AVG(score) FROM SCORES")
        score_min, score_max, score_avg = cursor.fetchone()

        cursor.execute("SELECT SUM(duration_minutes) FROM SCORES")
        total_minutes = cursor.fetchone()[0] or 0

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
            SELECT game, AVG(score), COUNT(*)
            FROM SCORES
            GROUP BY game
            ORDER BY AVG(score) DESC
        """)
        stats_par_jeu = cursor.fetchall()

        # Répartition des joueurs par pays
        cursor.execute("""
            SELECT country, COUNT(*)
            FROM PLAYERS
            WHERE country IS NOT NULL
            GROUP BY country
            ORDER BY COUNT(*) DESC
        """)
        players_by_country = cursor.fetchall()

        # Répartition des sessions par plateforme
        cursor.execute("""
            SELECT platform, COUNT(*), AVG(score)
            FROM SCORES
            GROUP BY platform
            ORDER BY COUNT(*) DESC
        """)
        sessions_by_platform = cursor.fetchall()

    # Construction du rapport
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sep = "=" * 50

    r = ""
    r += sep + "\n"
    r += "  GAMETRACKER - Rapport de synthese\n"
    r += f"  Genere le : {now}\n"
    r += sep + "\n\n"

    # Statistiques générales
    r += "-- Statistiques generales --\n\n"
    r += f"  Joueurs inscrits     : {nb_joueurs}\n"
    r += f"  Scores enregistres   : {nb_scores}\n"
    r += f"  Jeux distincts       : {nb_jeux}\n"
    r += f"  Temps de jeu total   : {total_minutes} min ({total_minutes / 60:.1f}h)\n"
    r += f"  Score minimum        : {score_min}\n"
    r += f"  Score maximum        : {score_max}\n"
    r += f"  Score moyen          : {score_avg:.1f}\n\n"

    # Top 5
    r += "-- Top 5 des meilleurs scores --\n\n"
    for i, (username, game, score) in enumerate(top_scores, 1):
        r += f"  {i}. {username:<16} {game:<18} {score:>6}\n"
    r += "\n"

    # Stats par jeu
    r += "-- Score moyen par jeu --\n\n"
    for game, avg, count in stats_par_jeu:
        r += f"  {game:<18} moyenne: {avg:>8.1f}   ({count} parties)\n"
    r += "\n"

    # Joueurs par pays
    r += "-- Joueurs par pays --\n\n"
    for country, count in players_by_country:
        pct = count / nb_joueurs * 100
        r += f"  {country or 'N/A':<14} {count:>3} joueur(s)   ({pct:.0f}%)\n"
    r += "\n"

    # Sessions par plateforme
    r += "-- Sessions par plateforme --\n\n"
    for platform, count, avg_s in sessions_by_platform:
        pct = count / nb_scores * 100
        r += f"  {platform:<12} {count:>3} sessions   ({pct:.0f}%)   score moyen: {avg_s:.1f}\n"
    r += "\n"

    r += sep + "\n"
    r += "  Rapport genere automatiquement par GameTracker\n"
    r += sep + "\n"

    # Écrire dans le fichier
    with open("output/rapport.txt", "w", encoding="utf-8") as f:
        f.write(r)

    print("Rapport généré dans output/rapport.txt")