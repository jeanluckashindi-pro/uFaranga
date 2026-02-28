# 🐛 Correction - Erreur Fonts

## Problème Identifié
```
ERROR [TypeError: Cannot convert undefined value to object]
```

L'erreur venait de `Fonts.default` qui était `undefined` car `Platform.select()` ne retourne pas un objet avec une propriété `default`, mais directement l'objet correspondant à la plateforme.

## Solution Appliquée

### Avant (❌ Incorrect)
```typescript
export const Fonts = Platform.select({
  web: { body: "'Open Sans', sans-serif", ... },
  default: { body: 'OpenSans-Regular', ... },
});

// Usage
const fontFamily = Fonts.default.heading; // ❌ Fonts.default est undefined!
```

### Après (✅ Correct)
```typescript
const fontConfig = {
  web: { body: "'Open Sans', sans-serif", ... },
  native: { body: 'System', ... },
};

export const Fonts = Platform.OS === 'web' ? fontConfig.web : fontConfig.native;

// Usage
const fontFamily = Fonts.heading; // ✅ Fonctionne correctement!
```

## Fichiers Modifiés

1. ✅ `constants/theme.ts` - Structure de Fonts corrigée
2. ✅ `components/themed.tsx` - Accès à Fonts corrigé
3. ✅ `constants/theme-usage-example.tsx` - Exemples mis à jour

## Utilisation Correcte

### Dans les composants
```typescript
import { Fonts } from '@/constants/theme';

// ✅ Correct
<Text style={{ fontFamily: Fonts.body }}>Texte</Text>
<Text style={{ fontFamily: Fonts.heading }}>Titre</Text>

// ❌ Incorrect (ne plus utiliser)
<Text style={{ fontFamily: Fonts.default.body }}>Texte</Text>
```

### Avec ThemedText
```typescript
// Pas besoin de s'inquiéter, c'est géré automatiquement
<ThemedText font="body">Mon texte</ThemedText>
<ThemedText font="heading">Mon titre</ThemedText>
```

## Test

Relancez l'application:
```bash
npm start
```

L'erreur devrait être résolue et l'application devrait démarrer correctement! 🎉
