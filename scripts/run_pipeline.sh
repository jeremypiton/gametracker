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
python src/main.py

echo "4. Génération du rapport..."
python -c "
import sys
sys.path.insert(0, 'src')
from report import generate_report
generate_report()
"

echo "=== Pipeline terminé avec succès ==="