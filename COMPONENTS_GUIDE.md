# Guide des Composants Communs uFaranga

Ce guide présente les composants UI réutilisables créés pour les applications Back-Office et Front-Office de uFaranga.

## 📁 Structure

```
Back-Office/src/components/common/
├── Spinner.jsx & Spinner.css    # Animations de chargement
├── Button.jsx                   # Boutons avec variantes
├── Card.jsx                     # Cartes et conteneurs
├── Modal.jsx                    # Modales et confirmations
├── Input.jsx                    # Champs de saisie
├── Alert.jsx                    # Messages d'alerte
├── index.js                     # Export centralisé
└── ComponentExamples.jsx        # Exemples d'utilisation

Front-Office/src/components/common/
├── Spinner.jsx & Spinner.css    # Animations de chargement
├── Button.jsx                   # Boutons avec variantes
├── Card.jsx                     # Cartes et conteneurs
├── index.js                     # Export centralisé
└── ComponentExamples.jsx        # Exemples d'utilisation
```

## 🎨 Composants Disponibles

### 1. Spinner - Animations de Chargement

**Variantes disponibles :**
- `Spinner` - Spinner rotatif standard
- `DotSpinner` - Animation avec points
- `BarSpinner` - Animation avec barres

**Props :**
- `size`: 'small' | 'medium' | 'large' | 'xlarge'
- `color`: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'white'
- `text`: Texte à afficher sous le spinner
- `overlay`: Affichage en overlay plein écran

**Utilisation :**
```jsx
import { Spinner, DotSpinner, BarSpinner } from './components/common';

<Spinner size="medium" color="primary" text="Chargement..." />
<DotSpinner color="success" />
<BarSpinner color="warning" />
```

### 2. Button - Boutons Interactifs

**Variantes disponibles :**
- `Button` - Bouton principal
- `ButtonGroup` - Groupe de boutons
- `IconButton` - Bouton avec icône uniquement

**Props :**
- `variant`: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline' | 'ghost' | 'link'
- `size`: 'small' | 'medium' | 'large' | 'xlarge'
- `loading`: État de chargement
- `disabled`: État désactivé
- `fullWidth`: Largeur complète
- `icon`: Icône à afficher
- `iconPosition`: 'left' | 'right'

**Utilisation :**
```jsx
import { Button, ButtonGroup, IconButton } from './components/common';

<Button variant="primary" size="medium" loading={isLoading}>
  Enregistrer
</Button>

<ButtonGroup>
  <Button variant="outline">Gauche</Button>
  <Button variant="outline">Droite</Button>
</ButtonGroup>

<IconButton icon={<HeartIcon />} variant="danger" />
```

### 3. Card - Conteneurs et Cartes

**Variantes disponibles :**
- `Card` - Carte standard
- `CardHeader`, `CardBody`, `CardFooter` - Sections de carte
- `StatsCard` - Carte pour statistiques

**Props :**
- `variant`: 'default' | 'primary' | 'success' | 'warning' | 'danger'
- `padding`: 'none' | 'small' | 'medium' | 'large' | 'xlarge'
- `shadow`: 'none' | 'small' | 'medium' | 'large' | 'xlarge'
- `hover`: Effet hover
- `title`: Titre de la carte
- `subtitle`: Sous-titre
- `footer`: Contenu du pied de page

**Utilisation :**
```jsx
import { Card, StatsCard } from './components/common';

<Card 
  title="Titre" 
  subtitle="Description"
  variant="primary"
  hover
  footer={<Button>Action</Button>}
>
  Contenu de la carte
</Card>

<StatsCard
  title="Utilisateurs"
  value="1,234"
  change="+12%"
  changeType="positive"
  icon={<UserIcon />}
/>
```

### 4. Modal - Modales et Confirmations (Back-Office uniquement)

**Variantes disponibles :**
- `Modal` - Modale standard
- `ConfirmModal` - Modale de confirmation

**Props :**
- `isOpen`: État d'ouverture
- `onClose`: Fonction de fermeture
- `title`: Titre de la modale
- `size`: 'small' | 'medium' | 'large' | 'xlarge' | 'full'
- `closeOnOverlay`: Fermeture sur clic overlay
- `closeOnEscape`: Fermeture sur Échap
- `footer`: Contenu du pied de page

**Utilisation :**
```jsx
import { Modal, ConfirmModal } from './components/common';

<Modal
  isOpen={showModal}
  onClose={() => setShowModal(false)}
  title="Titre de la modale"
  footer={<Button>Confirmer</Button>}
>
  Contenu de la modale
</Modal>

<ConfirmModal
  isOpen={showConfirm}
  onClose={() => setShowConfirm(false)}
  onConfirm={handleConfirm}
  title="Confirmation"
  message="Êtes-vous sûr ?"
/>
```

### 5. Input - Champs de Saisie (Back-Office uniquement)

**Props :**
- `type`: Type d'input HTML
- `label`: Libellé du champ
- `placeholder`: Texte d'aide
- `error`: Message d'erreur
- `disabled`: État désactivé
- `required`: Champ obligatoire
- `size`: 'small' | 'medium' | 'large'
- `fullWidth`: Largeur complète

**Utilisation :**
```jsx
import { Input } from './components/common';

<Input
  label="Nom d'utilisateur"
  placeholder="Entrez votre nom"
  value={value}
  onChange={handleChange}
  required
  error={errorMessage}
/>
```

### 6. Alert - Messages d'Alerte (Back-Office uniquement)

**Props :**
- `variant`: 'success' | 'warning' | 'danger' | 'info'
- `size`: 'small' | 'medium' | 'large'
- `dismissible`: Possibilité de fermer
- `onDismiss`: Fonction de fermeture
- `icon`: Affichage de l'icône

**Utilisation :**
```jsx
import { Alert } from './components/common';

<Alert 
  variant="success" 
  dismissible 
  onDismiss={handleDismiss}
>
  <strong>Succès!</strong> Action effectuée avec succès.
</Alert>
```

## 🎯 Import Centralisé

Tous les composants peuvent être importés depuis l'index :

```jsx
// Back-Office
import { 
  Spinner, 
  Button, 
  Card, 
  Modal, 
  Input, 
  Alert 
} from './components/common';

// Front-Office
import { 
  Spinner, 
  Button, 
  Card 
} from './components/common';
```

## 🎨 Personnalisation

Les composants utilisent Tailwind CSS pour le styling. Vous pouvez :

1. **Ajouter des classes personnalisées** via la prop `className`
2. **Modifier les variantes** en éditant les objets de classes dans chaque composant
3. **Étendre les composants** en créant des wrappers personnalisés

## 📱 Responsive Design

Tous les composants sont conçus pour être responsive et s'adaptent automatiquement aux différentes tailles d'écran grâce aux classes Tailwind CSS.

## 🔧 Développement

Pour ajouter de nouveaux composants :

1. Créer le fichier dans `src/components/common/`
2. Suivre la structure et les conventions existantes
3. Ajouter l'export dans `index.js`
4. Créer des exemples dans `ComponentExamples.jsx`
5. Documenter dans ce guide

## 🚀 Utilisation dans les Projets

### Back-Office (React + Vite)
```jsx
// Dans vos composants
import { Button, Card, Spinner } from '../components/common';

function Dashboard() {
  return (
    <Card title="Dashboard">
      <Button variant="primary">Action</Button>
      <Spinner size="medium" />
    </Card>
  );
}
```

### Front-Office (React + Vite)
```jsx
// Dans vos composants
import { Button, Card, Spinner } from '../components/common';

function UserProfile() {
  return (
    <Card title="Profil Utilisateur">
      <Button variant="success">Modifier</Button>
    </Card>
  );
}
```

## 📋 Exemples Complets

Consultez les fichiers `ComponentExamples.jsx` dans chaque projet pour voir des exemples complets d'utilisation de tous les composants.

---

**Note :** Les composants Modal, Input et Alert sont actuellement disponibles uniquement dans le Back-Office. Ils peuvent être adaptés pour le Front-Office selon les besoins.