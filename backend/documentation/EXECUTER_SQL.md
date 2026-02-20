# ⚡ Exécution SQL Ultra-Rapide

## 🚀 Une Seule Commande

### Windows
```cmd
executer_peuplement.bat
```

### Linux/Mac
```bash
chmod +x executer_peuplement.sh
./executer_peuplement.sh
```

## ✅ Résultat

Après exécution:
- ✅ Colonnes `continent` et `sous_region` ajoutées
- ✅ 19 pays africains insérés
- ✅ 68+ provinces créées
- ✅ Index créés
- ✅ Métadonnées peuplées

## 🔍 Vérifier

```bash
# Tester l'API
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique
```

## 📚 Documentation

- **GUIDE_PEUPLEMENT_SQL.md** - Guide complet
- **peupler_localisation_sql.sql** - Script pays
- **peupler_provinces_sql.sql** - Script provinces

---

**C'est tout! Une commande et c'est fait.** 🎉
