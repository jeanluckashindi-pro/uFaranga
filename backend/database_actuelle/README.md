# Base de Données Localisation uFaranga

## 📦 Contenu

Ce dossier contient l'export complet du schéma `localisation` de la base de données uFaranga.

**Fichier**: `ufaranga_localisation_complete.sql` (~90 MB)

## 📊 Données incluses

- **232,370 entités géographiques** sur 9 niveaux
- 54 Pays africains
- 1,095 Provinces
- 3,374 Districts
- 20,715 Communes
- 114,370 Secteurs
- 16,542 Quartiers
- 60,164 Zones
- 16,056 Collines

## 🚀 Installation

### Restaurer la base de données complète:

```bash
psql -U ufaranga -d ufaranga -f ufaranga_localisation_complete.sql
```

**Durée**: ~5-10 minutes

## ✅ Après installation

La base contiendra:
- Toutes les tables du schéma `localisation`
- Toutes les données géographiques
- Tous les index optimisés
- Toutes les fonctions SQL
- Toutes les vues matérialisées

## 📝 Notes

- PostgreSQL 10+ requis
- Espace disque: ~500 MB
- Le fichier contient STRUCTURE + DONNÉES
- Aucun script Python nécessaire

## 🎯 Utilisation

### Exemples de requêtes:

```sql
-- Compter les entités
SELECT 
    'Pays' as niveau, COUNT(*) FROM localisation.pays
UNION ALL
SELECT 'Provinces', COUNT(*) FROM localisation.provinces
UNION ALL
SELECT 'Districts', COUNT(*) FROM localisation.districts;

-- Rechercher par GPS
SELECT * FROM localisation.trouver_pays_par_gps(-3.3731, 29.9189);

-- Statistiques complètes
SELECT * FROM localisation.stats_hierarchie_complete();
```

---

**Version**: 1.0  
**Date**: Mars 2026  
**Taille**: 90 MB  
**Statut**: ✅ Production Ready
