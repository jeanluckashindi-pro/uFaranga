# 🚀 Instructions d'Exécution - Scripts de Localisation

## ⚡ Démarrage Rapide

### 1. Exécuter le Script Principal

```bash
python analyser_et_completer_localisation.py
```

**Le script va:**
1. Analyser la couverture actuelle
2. Proposer d'ajouter les colonnes `continent` et `sous_region`
3. Proposer de peupler les pays africains
4. Afficher les statistiques finales

### 2. Générer un Rapport

```bash
python generer_rapport_geo.py
```

**Output:** Fichier `RAPPORT_GEO_YYYYMMDD_HHMMSS.md`

---

## 📋 Étapes Détaillées

### Étape 1: Lancer le Script

```bash
cd D:\Projets\Decima Techno\uFaranga\backend
python analyser_et_completer_localisation.py
```

### Étape 2: Suivre les Instructions

Le script est interactif et vous guide:

```
================================================================================
SCRIPT D'ANALYSE ET COMPLÉTION DE LA LOCALISATION
================================================================================

Ce script va:
1. Analyser la couverture géographique actuelle
2. Vérifier/Ajouter les colonnes continent et sous_region
3. Peupler les pays africains avec leurs divisions
4. Afficher les statistiques finales

Appuyez sur Entrée pour continuer...
```

### Étape 3: Répondre aux Questions

**Question 1: Ajouter les colonnes?**
```
Voulez-vous ajouter les colonnes manquantes? (o/n): o
```
→ Tapez `o` puis Entrée

**Question 2: Peupler les pays?**
```
Voulez-vous peupler les pays africains? (o/n): o
```
→ Tapez `o` puis Entrée

### Étape 4: Vérifier les Résultats

Le script affiche:
- ✅ Nombre de pays créés/mis à jour
- ✅ Nombre de provinces créées
- ✅ Statistiques par continent
- ✅ Statistiques par sous-région

---

## 📊 Output Attendu

### Analyse Initiale
```
================================================================================
ANALYSE DE LA COUVERTURE GÉOGRAPHIQUE
================================================================================

Total pays dans la base: 3

Pays                           Code       Provinces    Districts    Quartiers   
--------------------------------------------------------------------------------
✅ Burundi                      BI         17           0            0           
❌ Rwanda                       RW         0            0            0           
❌ Kenya                        KE         0            0            0           

================================================================================
RÉSUMÉ: 2 pays sans divisions administratives
================================================================================
```

### Ajout des Colonnes
```
================================================================================
AJOUT DES COLONNES GÉOGRAPHIQUES
================================================================================

1. Ajout de la colonne 'continent'...
   ✅ Colonne 'continent' ajoutée

2. Ajout de la colonne 'sous_region'...
   ✅ Colonne 'sous_region' ajoutée

3. Création des index...
   ✅ Index créés

✅ Colonnes géographiques ajoutées avec succès!
```

### Peuplement des Pays
```
================================================================================
PEUPLEMENT DES PAYS AFRICAINS
================================================================================

📍 Traitement: Burundi (BI)
   ✅ Pays mis à jour
   📂 Création de 17 provinces...
      ✅ Bubanza
      ✅ Bujumbura Mairie
      ✅ Bujumbura Rural
      ...

📍 Traitement: Rwanda (RW)
   ✅ Pays créé
   📂 Création de 5 provinces...
      ✅ Kigali
      ✅ Est
      ...

================================================================================
RÉSUMÉ DU PEUPLEMENT
================================================================================
Pays créés: 15
Pays mis à jour: 4
Provinces créées: 68
Erreurs: 0
```

### Statistiques Finales
```
================================================================================
STATISTIQUES FINALES
================================================================================

Par continent:
Continent                      Nb Pays         Avec Provinces      
----------------------------------------------------------------------
Afrique                        19              19                  

Par sous-région (Afrique):
Sous-région                    Nb Pays         Avec Provinces      
----------------------------------------------------------------------
Afrique de l'Est               5               5                   
Afrique Centrale               5               5                   
Afrique de l'Ouest             4               4                   
Afrique du Nord                4               4                   
Afrique Australe               1               1                   

Total général:
  Pays: 19
  Provinces: 68
  Districts: 0
  Quartiers: 0
```

---

## ✅ Vérification

### 1. Vérifier les Colonnes

```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'localisation' 
AND table_name = 'pays'
AND column_name IN ('continent', 'sous_region');
```

**Résultat Attendu:**
```
column_name  | data_type
-------------+-----------
continent    | character varying
sous_region  | character varying
```

### 2. Vérifier les Données

```sql
SELECT code_iso_2, nom, continent, sous_region
FROM localisation.pays
WHERE continent = 'Afrique'
ORDER BY sous_region, nom;
```

**Résultat Attendu:**
```
code_iso_2 | nom                  | continent | sous_region
-----------+----------------------+-----------+------------------
BI         | Burundi              | Afrique   | Afrique de l'Est
KE         | Kenya                | Afrique   | Afrique de l'Est
RW         | Rwanda               | Afrique   | Afrique de l'Est
...
```

### 3. Vérifier les Provinces

```sql
SELECT p.nom as pays, COUNT(pr.id) as nb_provinces
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
WHERE p.continent = 'Afrique'
GROUP BY p.nom
ORDER BY nb_provinces DESC;
```

**Résultat Attendu:**
```
pays                  | nb_provinces
----------------------+-------------
Burundi               | 17
RD Congo              | 8
Rwanda                | 5
...
```

### 4. Tester l'API

```bash
curl http://127.0.0.1:8000/api/v1/localisation/pays/
```

**Vérifier que la réponse contient:**
```json
{
  "id": "...",
  "code_iso_2": "BI",
  "nom": "Burundi",
  "metadonnees": {
    "continent": "Afrique",
    "sous_region": "Afrique de l'Est",
    ...
  }
}
```

---

## 🐛 Dépannage

### Erreur: Module Django Not Found

**Problème:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
# Activer l'environnement virtuel
.\venv\Scripts\activate

# Ou installer Django
pip install django
```

### Erreur: Permission Denied (PostgreSQL)

**Problème:**
```
permission denied for schema localisation
```

**Solution:**
```sql
-- Se connecter en tant que postgres
psql -U postgres -d ufaranga

-- Donner les droits
GRANT ALL PRIVILEGES ON SCHEMA localisation TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA localisation TO ufaranga;
```

### Erreur: Column Already Exists

**Problème:**
```
column "continent" of relation "pays" already exists
```

**Solution:** Pas de problème! Le script utilise `IF NOT EXISTS`. Continuez.

### Erreur: Pays Déjà Existe

**Problème:**
```
duplicate key value violates unique constraint "pays_code_iso_2_key"
```

**Solution:** Pas de problème! Le script utilise `update_or_create()` qui met à jour au lieu de créer.

---

## 📝 Notes Importantes

1. **Backup:** Le script ne supprime aucune donnée, il ajoute/met à jour uniquement
2. **Idempotent:** Vous pouvez exécuter le script plusieurs fois sans problème
3. **Sécurisé:** Utilise des transactions PostgreSQL
4. **Rapide:** Prend environ 10-30 secondes selon la base

---

## 🎯 Après l'Exécution

### 1. Vérifier les Endpoints

```bash
# Pays africains
curl http://127.0.0.1:8000/api/v1/localisation/pays/

# Provinces du Burundi
curl http://127.0.0.1:8000/api/v1/localisation/provinces/?pays_id=<uuid_burundi>
```

### 2. Tester dans le Frontend

```javascript
// Charger les pays africains
const pays = await fetch('http://127.0.0.1:8000/api/v1/localisation/pays/')
  .then(r => r.json());

console.log('Pays africains:', pays.length);
console.log('Premier pays:', pays[0]);
```

### 3. Générer un Rapport

```bash
python generer_rapport_geo.py
```

---

## ✅ Checklist Finale

- [ ] Script exécuté sans erreur
- [ ] Colonnes `continent` et `sous_region` ajoutées
- [ ] 19+ pays africains dans la base
- [ ] 68+ provinces créées
- [ ] Métadonnées peuplées (continent, sous_region, capitale)
- [ ] Endpoints API fonctionnels
- [ ] Rapport généré
- [ ] Frontend peut charger les données

---

**🎉 Félicitations! Le système de localisation est maintenant complet!** 🚀

Pour toute question, consultez:
- **GUIDE_SCRIPTS_LOCALISATION.md** - Guide détaillé
- **README_LOCALISATION_COMPLETE.md** - Vue d'ensemble
