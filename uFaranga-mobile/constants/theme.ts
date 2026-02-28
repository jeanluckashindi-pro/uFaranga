/**
 * Thème uFaranga - Couleurs et polices du projet
 */

import { Platform } from 'react-native';

// 🎨 Palette de Couleurs
export const Colors = {
  // Couleurs principales
  primary: '#007BFF',
  secondary: '#F58424',
  text: '#F9F9F9',
  background: '#00070F',
  
  // Couleurs secondaires
  card: '#181F27',
  darkBlue: '#000C18',
  darkGray: '#343A40',
  lightGray: '#F8F9FA',
  danger: '#8B1538',
  
  // Modes clair/sombre (pour compatibilité)
  light: {
    text: '#343A40',
    background: '#F8F9FA',
    tint: '#007BFF',
    icon: '#343A40',
    tabIconDefault: '#343A40',
    tabIconSelected: '#007BFF',
    card: '#FFFFFF',
  },
  dark: {
    text: '#F9F9F9',
    background: '#00070F',
    tint: '#007BFF',
    icon: '#F9F9F9',
    tabIconDefault: '#F9F9F9',
    tabIconSelected: '#F58424',
    card: '#181F27',
  },
};

// 🔤 Polices (Font Family)
const fontConfig = {
  web: {
    // Polices principales
    body: "'Open Sans', sans-serif",
    heading: "'Josefin Sans', sans-serif",
    
    // Polices supplémentaires
    anton: "'Anton', sans-serif",
    antonio: "'Antonio', sans-serif",
    bangers: "'Bangers', cursive",
    cookie: "'Cookie', cursive",
    allan: "'Allan', cursive",
    luckiestGuy: "'Luckiest Guy', cursive",
    ubuntu: "'Ubuntu', sans-serif",
  },
  native: {
    // Pour iOS/Android, utiliser les polices système par défaut
    // Les polices Google seront chargées via expo-font
    body: 'System',
    heading: 'System',
    anton: 'System',
    antonio: 'System',
    bangers: 'System',
    cookie: 'System',
    allan: 'System',
    luckiestGuy: 'System',
    ubuntu: 'System',
  },
};

export const Fonts = Platform.OS === 'web' ? fontConfig.web : fontConfig.native;

// Poids des polices
export const FontWeights = {
  regular: '400' as const,
  medium: '500' as const,
  semibold: '600' as const,
  bold: '700' as const,
};

// Tailles de police
export const FontSizes = {
  xs: 12,
  sm: 14,
  base: 16,
  lg: 18,
  xl: 20,
  '2xl': 24,
  '3xl': 30,
  '4xl': 36,
};
