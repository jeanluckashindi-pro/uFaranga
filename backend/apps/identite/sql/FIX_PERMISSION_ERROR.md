# Fix: Permission Denied for Relation niveaux_kyc

## Problème
Erreur lors de la connexion: `permission denied for relation niveaux_kyc`

Cette erreur se produit car l'utilisateur PostgreSQL utilisé par Django n'a pas les permissions nécessaires pour lire les tables de référence dans le schéma `identite`.

## Solution Rapide

### Option 1: Utiliser psql (Recommandé)

1. Ouvrez une invite de commande et connectez-vous à PostgreSQL:
```cmd
psql -U postgres -d nom_de_votre_base
```

2. Trouvez votre utilisateur actuel:
```sql
SELECT current_user;
```

3. Exécutez le script de permissions:
```sql
\i apps/identite/sql/grant_permissions.sql
```

### Option 2: Accorder les permissions manuellement

Connectez-vous à PostgreSQL et exécutez:

```sql
-- Remplacez 'votre_utilisateur' par votre utilisateur DB
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.types_utilisateurs TO votre_utilisateur;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.niveaux_kyc TO votre_utilisateur;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.statuts_utilisateurs TO votre_utilisateur;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.utilisateurs TO votre_utilisateur;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE identite.profils_utilisateurs TO votre_utilisateur;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA identite TO votre_utilisateur;
```

### Option 3: Accorder à tous les utilisateurs (Développement uniquement)

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA identite TO PUBLIC;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA identite TO PUBLIC;
```

⚠️ **Attention**: N'utilisez pas `TO PUBLIC` en production!

## Vérification

Après avoir accordé les permissions, vérifiez qu'elles sont bien appliquées:

```sql
SELECT 
    grantee,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'identite'
  AND table_name = 'niveaux_kyc';
```

Vous devriez voir des lignes avec `SELECT`, `INSERT`, `UPDATE`, `DELETE` pour votre utilisateur.

## Tester la connexion

Redémarrez votre serveur Django et essayez de vous connecter à nouveau:

```cmd
python manage.py runserver
```

Puis testez l'endpoint de connexion:
```
POST http://127.0.0.1:8000/api/v1/authentification/connexion/
```

## Pourquoi cette erreur se produit?

Lors de la connexion, le serializer `CustomTokenObtainPairSerializer` accède à:
1. `identite.utilisateurs` pour vérifier les identifiants
2. `identite.niveaux_kyc` pour récupérer le niveau KYC (via la relation ForeignKey)
3. `identite.types_utilisateurs` et `identite.statuts_utilisateurs` pour les informations du compte

Si l'utilisateur DB n'a pas les permissions SELECT sur ces tables, Django ne peut pas exécuter les requêtes et retourne l'erreur "permission denied".

## Prévention future

Pour éviter ce problème à l'avenir:

1. **Lors de la création de nouvelles tables**, accordez immédiatement les permissions:
```sql
GRANT ALL PRIVILEGES ON TABLE schema.nouvelle_table TO votre_utilisateur;
```

2. **Utilisez un script de migration** qui accorde automatiquement les permissions après la création des tables.

3. **Documentez les permissions requises** dans votre README ou documentation de déploiement.
