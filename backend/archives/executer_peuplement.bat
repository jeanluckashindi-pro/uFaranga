@echo off
REM ============================================================================
REM Script pour peupler la base de données uFaranga avec les données de localisation
REM ============================================================================

echo ============================================================================
echo PEUPLEMENT DE LA BASE DE DONNEES UFARANGA
echo ============================================================================
echo.

REM Configuration
set PGUSER=ufaranga
set PGPASSWORD=12345
set PGDATABASE=ufaranga
set PGHOST=localhost
set PGPORT=5432

echo Configuration:
echo   Utilisateur: %PGUSER%
echo   Base: %PGDATABASE%
echo   Host: %PGHOST%:%PGPORT%
echo.

REM Vérifier que psql est disponible
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: psql n'est pas trouve dans le PATH
    echo Veuillez installer PostgreSQL ou ajouter psql au PATH
    pause
    exit /b 1
)

echo ============================================================================
echo ETAPE 1: Peupler les pays africains
echo ============================================================================
echo.

psql -U %PGUSER% -d %PGDATABASE% -f peupler_localisation_sql.sql

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERREUR lors du peuplement des pays
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo ETAPE 2: Peupler les provinces
echo ============================================================================
echo.

psql -U %PGUSER% -d %PGDATABASE% -f peupler_provinces_sql.sql

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERREUR lors du peuplement des provinces
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo VERIFICATION
echo ============================================================================
echo.

psql -U %PGUSER% -d %PGDATABASE% -c "SELECT continent, sous_region, COUNT(*) as nb_pays FROM localisation.pays WHERE continent = 'Afrique' GROUP BY continent, sous_region ORDER BY sous_region;"

echo.
echo ============================================================================
echo PEUPLEMENT TERMINE AVEC SUCCES!
echo ============================================================================
echo.
echo Resultats:
echo   - 19 pays africains ajoutes
echo   - 68+ provinces creees
echo   - Colonnes continent et sous_region ajoutees
echo.
echo Prochaines etapes:
echo   1. Verifier l'API: http://127.0.0.1:8000/api/v1/localisation/pays/
echo   2. Ajouter des districts: python ajouter_districts_quartiers.py
echo   3. Generer un rapport: python generer_rapport_geo.py
echo.

pause
