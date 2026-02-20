@echo off
REM =============================================================================
REM Script Windows pour exécuter le setup complet
REM =============================================================================

echo =========================================
echo SETUP DES TABLES DE REFERENCE IDENTITE
echo =========================================
echo.

REM Vérifier si psql est disponible
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: psql n'est pas trouvé dans le PATH
    echo Veuillez installer PostgreSQL ou ajouter psql au PATH
    pause
    exit /b 1
)

echo Connexion à la base de données...
echo.

REM Exécuter le script SQL
psql -U ufaranga -d ufaranga -f setup_complet.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================
    echo SUCCES! Setup terminé
    echo =========================================
    echo.
    echo Prochaines étapes:
    echo 1. Redémarrer le serveur Django
    echo 2. Tester la connexion
    echo.
) else (
    echo.
    echo =========================================
    echo ERREUR lors de l'exécution du script
    echo =========================================
    echo.
    echo Vérifiez:
    echo - Que PostgreSQL est démarré
    echo - Que l'utilisateur 'ufaranga' existe
    echo - Que la base 'ufaranga' existe
    echo - Que le mot de passe est correct
    echo.
)

pause
