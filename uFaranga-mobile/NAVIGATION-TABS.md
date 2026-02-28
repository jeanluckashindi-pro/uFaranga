# 📱 Navigation - Bottom Tabs

Documentation de la barre de navigation inférieure de uFaranga.

## 🎯 Structure des Tabs

L'application dispose de 4 onglets principaux dans la barre de navigation:

### 1. 🏠 Accueil (`app/(tabs)/index.tsx`)
- **Icône**: Maison (house.fill)
- **Titre**: Accueil
- **Contenu**: Page d'accueil avec présentation de uFaranga
- **Description**: 
  - Titre de bienvenue
  - Présentation du système
  - Explication des fonctionnalités

### 2. 👤 Compte (`app/(tabs)/compte.tsx`)
- **Icône**: Personne (person.fill)
- **Titre**: Compte
- **Contenu**: Gestion du compte utilisateur
- **État**: En cours de développement

### 3. 💳 Carte Virtuelle (`app/(tabs)/carte.tsx`)
- **Icône**: Carte de crédit (creditcard.fill)
- **Titre**: Carte Virtuelle
- **Contenu**: Gestion de la carte virtuelle de transport
- **État**: En cours de développement

### 4. ⚙️ Plus (`app/(tabs)/plus.tsx`)
- **Icône**: Points de suspension (ellipsis.circle.fill)
- **Titre**: Plus
- **Contenu**: Paramètres et options supplémentaires
- **État**: En cours de développement

## 🎨 Style de la Barre de Navigation

### Couleurs
- **Active**: `Colors.primary` (#007BFF - Bleu)
- **Inactive**: `Colors.lightGray` (#F8F9FA)
- **Background**: `Colors.card` (#181F27)
- **Bordure**: `Colors.darkBlue` (#000C18)

### Dimensions
- **Hauteur**: 65px
- **Padding**: 8px (haut et bas)
- **Taille des icônes**: 26px
- **Taille du texte**: 12px

### Caractéristiques
- Retour haptique au toucher (HapticTab)
- Animations fluides
- Design cohérent avec le thème

## 📂 Structure des Fichiers

```
app/(tabs)/
├── _layout.tsx      # Configuration de la navigation
├── index.tsx        # Page Accueil
├── compte.tsx       # Page Compte
├── carte.tsx        # Page Carte Virtuelle
├── plus.tsx         # Page Plus
├── explore.tsx      # (Caché - ancienne page)
└── theme-demo.tsx   # (Caché - page de démo)
```

## 🔧 Configuration

### Layout (`app/(tabs)/_layout.tsx`)

```typescript
<Tabs
  screenOptions={{
    tabBarActiveTintColor: Colors.primary,
    tabBarInactiveTintColor: Colors.lightGray,
    headerShown: false,
    tabBarButton: HapticTab,
    tabBarStyle: {
      backgroundColor: Colors.card,
      borderTopColor: Colors.darkBlue,
      borderTopWidth: 1,
      paddingBottom: 8,
      paddingTop: 8,
      height: 65,
    },
  }}>
  {/* Tabs screens */}
</Tabs>
```

### Masquer des Tabs

Les anciennes pages (explore, theme-demo) sont masquées avec:
```typescript
<Tabs.Screen
  name="explore"
  options={{
    href: null, // Masque le tab
  }}
/>
```

## 🚀 Utilisation

### Navigation Programmatique

```typescript
import { useRouter } from 'expo-router';

const router = useRouter();

// Naviguer vers une page
router.push('/(tabs)/compte');
router.push('/(tabs)/carte');
router.push('/(tabs)/plus');
```

### Liens

```typescript
import { Link } from 'expo-router';

<Link href="/(tabs)/compte">Aller au compte</Link>
```

## 📝 Page d'Accueil

La page d'accueil (`index.tsx`) contient:

1. **Header**
   - Titre: "Bienvenue sur uFaranga"
   - Sous-titre: "Votre solution de transport sans contact"

2. **Contenu**
   - Présentation de uFaranga
   - Explication du système sans contact
   - Description de l'architecture sécurisée

3. **Style**
   - Texte justifié
   - Espacement cohérent
   - Lisibilité optimale

## 🎯 Prochaines Étapes

### Page Compte
- [ ] Profil utilisateur
- [ ] Informations personnelles
- [ ] Historique des transactions
- [ ] Paramètres du compte

### Page Carte Virtuelle
- [ ] Affichage de la carte
- [ ] QR Code pour validation
- [ ] Solde et recharge
- [ ] Historique d'utilisation

### Page Plus
- [ ] Paramètres de l'application
- [ ] Notifications
- [ ] Aide et support
- [ ] À propos
- [ ] Déconnexion

## 💡 Conseils

1. **Cohérence**: Toutes les pages utilisent le même style de header
2. **Simplicité**: Design épuré et professionnel
3. **Navigation**: Facile et intuitive
4. **Performance**: Chargement rapide des pages

## 🎨 Personnalisation

### Changer les Icônes

Dans `_layout.tsx`:
```typescript
<Tabs.Screen
  name="compte"
  options={{
    title: 'Compte',
    tabBarIcon: ({ color }) => (
      <IconSymbol size={26} name="person.fill" color={color} />
    ),
  }}
/>
```

### Modifier les Couleurs

Dans `_layout.tsx`:
```typescript
tabBarActiveTintColor: Colors.secondary, // Orange au lieu de bleu
```

### Ajuster la Hauteur

Dans `_layout.tsx`:
```typescript
tabBarStyle: {
  height: 70, // Au lieu de 65
}
```

## ✅ Résultat

Une barre de navigation professionnelle avec:
- 4 onglets clairs et distincts
- Design cohérent avec le thème uFaranga
- Navigation fluide et intuitive
- Prête pour le développement des fonctionnalités
