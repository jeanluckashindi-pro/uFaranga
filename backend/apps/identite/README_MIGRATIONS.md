# Erreur : permission denied for schema identite

L’utilisateur PostgreSQL utilisé par Django (`DB_USER`, par défaut `ufaranga`) n’a pas le droit de créer des tables dans le schéma **identite** (tables **identite.utilisateurs**, **identite.profils_utilisateurs**).

## Solution 1 : Accorder les droits (recommandé si vous avez un accès admin à la base)

1. Connectez-vous à PostgreSQL avec un compte **superutilisateur** (ou propriétaire du schéma) :
   ```bash
   psql -U postgres -d ufaranga
   ```
   Ou via pgAdmin / DBeaver avec un compte admin.

2. Exécutez le script :
   ```bash
   psql -U postgres -d ufaranga -f apps/identite/grant_schema_identite.sql
   ```
   Ou copiez-collez le contenu de `apps/identite/grant_schema_identite.sql` dans une fenêtre SQL.

3. Si votre utilisateur Django n’est pas `ufaranga`, modifiez la ligne `TO ufaranga` dans le script avec le bon nom d’utilisateur.

4. Relancez les migrations :
   ```bash
   python manage.py migrate
   ```

## Solution 2 : Utiliser le schéma `public`

Si vous ne pouvez pas modifier les droits sur le schéma `identite`, on peut faire créer les tables dans le schéma `public` (ex. `identite_utilisateurs` au lieu de `identite.utilisateurs`). Dans ce cas il faut adapter les `db_table` des modèles. À faire seulement si la solution 1 n’est pas possible.

---

## Table existante : colonnes Django manquantes

Si la table **identite.utilisateurs** a été créée à la main (sans la migration Django), il peut manquer les colonnes **password** / **last_login** / **is_superuser** / **is_staff**.

- Le modèle a été aligné sur la base : **password** → `hash_mot_de_passe`, **last_login** → `derniere_connexion`.
- Pour **is_superuser** et **is_staff**, exécuter en tant que **propriétaire de la table** (ou postgres) :

```bash
psql -U postgres -d ufaranga -f apps/identite/alter_utilisateurs_django_columns.sql
```

Puis relancer : `python manage.py creer_mock_utilisateurs_identite`
