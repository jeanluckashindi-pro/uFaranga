# Mock utilisateurs — identite.utilisateurs

Commande : **`python manage.py creer_mock_utilisateurs_identite`**

Mot de passe commun : **`DemoPass123!`**

---

## Utilisateurs créés (par profil)

| Profil        | Courriel               | Téléphone    | Prénom / Nom           | Statut / KYC      |
|---------------|------------------------|--------------|-------------------------|--------------------|
| **SUPER_ADMIN** | super.admin@ufaranga.bi | +25779000001 | Super Admin             | ACTIF, KYC 3       |
| **ADMIN**       | admin@ufaranga.bi       | +25779000002 | Jean Administrateur     | ACTIF, KYC 2       |
| **AGENT**       | agent1@ufaranga.bi      | +25779000003 | Marie Agent             | ACTIF, KYC 2       |
| **MARCHAND**    | marchand1@ufaranga.bi   | +25779000004 | Pierre Marchand         | ACTIF, KYC 2       |
| **CLIENT**      | client1@example.com     | +25779111111 | Alice Client            | ACTIF, KYC 1       |
| **CLIENT**      | client2@example.com     | +25779222222 | Bernard Client          | EN_VERIFICATION, KYC 0 |
| **SYSTEME**     | systeme@ufaranga.bi     | +25779000000 | Compte Système          | ACTIF, KYC 3       |

---

## Options

- `--password "MonMotDePasse"` : mot de passe pour tous les comptes.
- `--skip-existing` : ne pas recréer un utilisateur si le courriel existe déjà.

---

## Prérequis

Si les tables `identite.utilisateurs` et `identite.profils_utilisateurs` n’existent pas :

```bash
python manage.py makemigrations identite
python manage.py migrate
```

Puis :

```bash
python manage.py creer_mock_utilisateurs_identite
```
