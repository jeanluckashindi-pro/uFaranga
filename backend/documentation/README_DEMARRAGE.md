# 🚀 Démarrage - Système de Localisation

## ⚡ Méthode Rapide (5 secondes)

### Windows
```cmd
executer_peuplement.bat
```

### Linux/Mac
```bash
./executer_peuplement.sh
```

**C'est tout!** Le script va:
- Ajouter les colonnes continent/sous_region
- Insérer 19 pays africains
- Créer 68+ provinces
- Créer les index

---

## 🐍 Méthode Python (30 secondes)

```bash
# 1. Migrations Django
python manage.py migrate localisation

# 2. Peupler les données
python analyser_et_completer_localisation.py
# Répondre "o" aux 2 questions

# 3. Ajouter districts/quartiers (optionnel)
python ajouter_districts_quartiers.py
```

---

## ✅ Vérifier

```bash
# Tester l'API
curl http://127.0.0.1:8000/api/v1/localisation/pays/?continent=Afrique
```

Vous devriez voir 19 pays africains avec leurs informations.

---

## 📚 Documentation

**Pour aller plus loin:**
- **INDEX_FINAL_LOCALISATION.md** - Index complet de tout
- **EXECUTER_SQL.md** - Guide SQL
- **LANCER_TOUT.md** - Guide Python
- **RESUME_COMPLET_LOCALISATION.md** - Résumé complet

---

## 🎯 Résultat

Après exécution:
- ✅ 19 pays africains (5 sous-régions)
- ✅ 68+ provinces
- ✅ API publique fonctionnelle
- ✅ Filtres par continent/sous-région

---

**Choisissez votre méthode et lancez!** 🎉
