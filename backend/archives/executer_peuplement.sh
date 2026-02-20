#!/bin/bash
# ============================================================================
# Script pour peupler la base de données uFaranga avec les données de localisation
# ============================================================================

echo "============================================================================"
echo "PEUPLEMENT DE LA BASE DE DONNEES UFARANGA"
echo "============================================================================"
echo ""

# Configuration
export PGUSER=ufaranga
export PGPASSWORD=12345
export PGDATABASE=ufaranga
export PGHOST=localhost
export PGPORT=5432

echo "Configuration:"
echo "  Utilisateur: $PGUSER"
echo "  Base: $PGDATABASE"
echo "  Host: $PGHOST:$PGPORT"
echo ""

# Vérifier que psql est disponible
if ! command -v psql &> /dev/null; then
    echo "ERREUR: psql n'est pas trouvé dans le PATH"
    echo "Veuillez installer PostgreSQL"
    exit 1
fi

echo "============================================================================"
echo "ETAPE 1: Peupler les pays africains"
echo "============================================================================"
echo ""

psql -U $PGUSER -d $PGDATABASE -f peupler_localisation_sql.sql

if [ $? -ne 0 ]; then
    echo ""
    echo "ERREUR lors du peuplement des pays"
    exit 1
fi

echo ""
echo "============================================================================"
echo "ETAPE 2: Peupler les provinces"
echo "============================================================================"
echo ""

psql -U $PGUSER -d $PGDATABASE -f peupler_provinces_sql.sql

if [ $? -ne 0 ]; then
    echo ""
    echo "ERREUR lors du peuplement des provinces"
    exit 1
fi

echo ""
echo "============================================================================"
echo "VERIFICATION"
echo "============================================================================"
echo ""

psql -U $PGUSER -d $PGDATABASE -c "SELECT continent, sous_region, COUNT(*) as nb_pays FROM localisation.pays WHERE continent = 'Afrique' GROUP BY continent, sous_region ORDER BY sous_region;"

echo ""
echo "============================================================================"
echo "PEUPLEMENT TERMINE AVEC SUCCES!"
echo "============================================================================"
echo ""
echo "Resultats:"
echo "  - 19 pays africains ajoutes"
echo "  - 68+ provinces creees"
echo "  - Colonnes continent et sous_region ajoutees"
echo ""
echo "Prochaines etapes:"
echo "  1. Verifier l'API: http://127.0.0.1:8000/api/v1/localisation/pays/"
echo "  2. Ajouter des districts: python ajouter_districts_quartiers.py"
echo "  3. Generer un rapport: python generer_rapport_geo.py"
echo ""
