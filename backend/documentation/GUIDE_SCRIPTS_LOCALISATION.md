# 📚 Guide d'Utilisation des Scripts de Localisation

## 🎯 Objectif

Ces scripts permettent de:
1. Analyser la couverture géographique actuelle
2. Ajouter les colonnes `continent` et `sous_region` à la table pays
3. Peupler automatiquement les pays africains avec leurs divisions administratives
4. Générer des rapports détaillés

## 📁 Scripts Disponibles

### 1. `analyser_et_completer_localisation.py`

**Script principal** pour analyser et compléter les données de localisation.

**Fonctionnalités:**
- ✅ Analyse la couverture actuelle (pays avec/sans provinces/districts/quartiers)
- ✅ Vérifie l'existence des colonnes `continent` et `sous_region`
- ✅ Ajoute les colonnes manquantes si nécessaire
- ✅ Peuple automatiquement 20+ pays africains avec leurs provinces
- ✅ Affiche des statistiques détaillées

**Utilisation:**
```bash
python analyser_et_completer_localisation.py
```

**Pays Africains Inclus:**

**Afrique de l'Est:**
- Burundi (17 provinces)
- Rwanda (5 provinces)
- Kenya (4 provinces)
- Tanzanie (4 provinces)
- Ouganda (4 provinces)

**Afrique Centrale:**
- RD Congo (8 provinces)
- République du Congo (2 provinces)
- Cameroun (2 provinces)
- Gabon (1 province)
- République Centrafricaine (1 province)

**Afrique de l'Ouest:**
- Sénégal (3 provinces)
- Côte d'Ivoire (2 provinces)
- Ghana (2 provinces)
- Nigeria (3 provinces)

**Afrique du Nord:**
- Maroc (3 provinces)
- Algérie (2 provinces)
- Tunisie (1 province)
- Égypte (2 provinces)

**Afrique Australe:**
- Afrique du Sud (3 provinces)

---

### 2. `generer_rapport_geo.py`

**Script de génération de rapports** en format Markdown.

**Fonctionnalités:**
- 📊 Statistiques globales
- 📍 Détail par pays
- 📈 Répartition par continent
- 📈 Répartition par sous-région
- ⚠️ Liste des pays incomplets
- 🏆 Top 10 des pays les plus complets
- 💡 Recommandations

**Utilisation:**
```bash
python generer_rapport_geo.py
```

**Output:**
- Fichier: `RAPPORT_GEO_YYYYMMDD_HHMMSS.md`
- Affichage console

---

## 🚀 Procédure Complète

### Étape 1: Analyser la Situation Actuelle

```bash
python analyser_et_completer_localisation.py
```

Le script va:
1. Lister tous les pays dans la base
2. Afficher combien ont des provinces/districts/quartiers
3. Identifier les pays incomplets

**Output Exemple:**
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

### Étape 2: Ajouter les Colonnes Géographiques

Le script détecte automatiquement si les colonnes existent et propose de les ajouter:

```
Voulez-vous ajouter les colonnes manquantes? (o/n): o
```

**Colonnes Ajoutées:**
- `continent` (VARCHAR 50) - Ex: "Afrique", "Europe", "Asie"
- `sous_region` (VARCHAR 100) - Ex: "Afrique de l'Est", "Afrique Centrale"

### Étape 3: Peupler les Pays Africains

```
Voulez-vous peupler les pays africains? (o/n): o
```

Le script va:
1. Créer ou mettre à jour chaque pays africain
2. Ajouter les métadonnées (continent, sous_region, capitale, téléphonie, devise)
3. Créer les provinces pour chaque pays
4. Afficher un résumé

**Output Exemple:**
```
📍 Traitement: Burundi (BI)
   ✅ Pays mis à jour
   📂 Création de 17 provinces...
      ✅ Bubanza
      ✅ Bujumbura Mairie
      ✅ Bujumbura Rural
      ...

================================================================================
RÉSUMÉ DU PEUPLEMENT
================================================================================
Pays créés: 15
Pays mis à jour: 5
Provinces créées: 68
Erreurs: 0
```

### Étape 4: Générer un Rapport

```bash
python generer_rapport_geo.py
```

**Output:**
- Fichier Markdown avec toutes les statistiques
- Tableaux détaillés
- Recommandations

---

## 📊 Structure des Données

### Table: `localisation.pays`

**Colonnes Ajoutées:**
```sql
continent VARCHAR(50)      -- Ex: "Afrique"
sous_region VARCHAR(100)   -- Ex: "Afrique de l'Est"
```

**Métadonnées JSON:**
```json
{
  "continent": "Afrique",
  "sous_region": "Afrique de l'Est",
  "capitale": "Gitega",
  "telephonie": {
    "code_telephonique": "+257"
  },
  "devise": {
    "code": "BIF"
  }
}
```

### Hiérarchie Géographique

```
Pays (continent, sous_region)
  └── Province/Région
       └── District/Ville
            └── Quartier/Zone
                 └── Point de Service
```

---

## 🌍 Groupements Géographiques

### Continents
- Afrique
- Europe
- Asie
- Amérique du Nord
- Amérique du Sud
- Océanie
- Antarctique

### Sous-Régions Africaines
- **Afrique de l'Est:** Burundi, Rwanda, Kenya, Tanzanie, Ouganda, Éthiopie, Somalie
- **Afrique Centrale:** RD Congo, Congo, Cameroun, Gabon, RCA, Tchad
- **Afrique de l'Ouest:** Sénégal, Côte d'Ivoire, Ghana, Nigeria, Mali, Burkina Faso
- **Afrique du Nord:** Maroc, Algérie, Tunisie, Égypte, Libye
- **Afrique Australe:** Afrique du Sud, Zimbabwe, Mozambique, Botswana, Namibie

---

## 🔍 Requêtes SQL Utiles

### Pays par Continent
```sql
SELECT continent, COUNT(*) as nb_pays
FROM localisation.pays
GROUP BY continent
ORDER BY nb_pays DESC;
```

### Pays par Sous-Région (Afrique)
```sql
SELECT sous_region, COUNT(*) as nb_pays
FROM localisation.pays
WHERE continent = 'Afrique'
GROUP BY sous_region
ORDER BY nb_pays DESC;
```

### Pays Sans Provinces
```sql
SELECT p.nom, p.code_iso_2, p.continent, p.sous_region
FROM localisation.pays p
WHERE NOT EXISTS (
    SELECT 1 FROM localisation.provinces pr WHERE pr.pays_id = p.id
)
ORDER BY p.nom;
```

### Statistiques Complètes
```sql
SELECT 
    p.nom,
    p.code_iso_2,
    p.continent,
    p.sous_region,
    COUNT(DISTINCT pr.id) as nb_provinces,
    COUNT(DISTINCT d.id) as nb_districts,
    COUNT(DISTINCT q.id) as nb_quartiers
FROM localisation.pays p
LEFT JOIN localisation.provinces pr ON pr.pays_id = p.id
LEFT JOIN localisation.districts d ON d.province_id = pr.id
LEFT JOIN localisation.quartiers q ON q.district_id = d.id
GROUP BY p.id, p.nom, p.code_iso_2, p.continent, p.sous_region
ORDER BY p.nom;
```

---

## ✅ Checklist de Validation

Après exécution des scripts:

- [ ] Les colonnes `continent` et `sous_region` existent dans `localisation.pays`
- [ ] Les pays africains ont leur continent = "Afrique"
- [ ] Les pays africains ont leur sous_region définie
- [ ] Les provinces sont créées pour les pays africains
- [ ] Les métadonnées contiennent les informations de téléphonie et devise
- [ ] Le rapport est généré sans erreur
- [ ] Les endpoints API retournent les nouvelles données

---

## 🔧 Dépannage

### Erreur: Permission Denied

**Problème:** L'utilisateur PostgreSQL n'a pas les droits pour ALTER TABLE

**Solution:**
```sql
-- Se connecter en tant que postgres
GRANT ALL PRIVILEGES ON SCHEMA localisation TO ufaranga;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA localisation TO ufaranga;
```

### Erreur: Column Already Exists

**Problème:** Les colonnes existent déjà

**Solution:** Le script utilise `ADD COLUMN IF NOT EXISTS`, donc pas de problème. Si l'erreur persiste, vérifier manuellement:
```sql
SELECT column_name 
FROM information_schema.columns 
WHERE table_schema = 'localisation' 
AND table_name = 'pays';
```

### Erreur: Pays Déjà Existe

**Problème:** Le pays existe déjà dans la base

**Solution:** Le script utilise `update_or_create()`, donc il met à jour au lieu de créer. Pas de problème.

---

## 📈 Prochaines Étapes

1. **Compléter les Districts et Quartiers**
   - Ajouter les districts pour les provinces créées
   - Ajouter les quartiers pour les grandes villes

2. **Ajouter d'Autres Continents**
   - Europe (si nécessaire)
   - Asie (si nécessaire)

3. **Enrichir les Métadonnées**
   - Ajouter les fuseaux horaires
   - Ajouter les langues officielles
   - Ajouter les populations

4. **Créer des Endpoints Filtrés**
   - `/api/v1/localisation/pays/?continent=Afrique`
   - `/api/v1/localisation/pays/?sous_region=Afrique de l'Est`

---

## 📞 Support

Si vous rencontrez des problèmes:
1. Vérifier les logs du script
2. Vérifier les permissions PostgreSQL
3. Vérifier que Django est bien configuré
4. Consulter la documentation des modèles

---

**✅ Scripts prêts à l'emploi!** 🚀
