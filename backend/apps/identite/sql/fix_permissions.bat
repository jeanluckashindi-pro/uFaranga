@echo off
REM =============================================================================
REM Script Windows pour corriger les permissions PostgreSQL
REM =============================================================================

echo.
echo ========================================
echo Fix: Permission Denied - niveaux_kyc
echo ========================================
echo.

REM Demander les informations de connexion
set /p DB_NAME="Nom de la base de donnees: "
set /p DB_USER="Utilisateur PostgreSQL (defaut: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

echo.
echo Connexion a PostgreSQL...
echo.

REM Exécuter le script SQL
psql -U %DB_USER% -d %DB_NAME% -f grant_permissions.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Succes! Permissions accordees.
    echo ========================================
    echo.
    echo Vous pouvez maintenant redemarrer votre serveur Django:
    echo   python manage.py runserver
    echo.
) else (
    echo.
    echo ========================================
    echo Erreur lors de l'execution du script
    echo ========================================
    echo.
    echo Verifiez que:
    echo   1. PostgreSQL est installe et accessible
    echo   2. Le nom de la base de donnees est correct
    echo   3. L'utilisateur a les droits necessaires
    echo.
)

pause
