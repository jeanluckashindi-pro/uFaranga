/**
 * 📚 Exemples d'utilisation du thème uFaranga
 * 
 * Ce fichier montre comment utiliser les couleurs et polices du projet.
 * Vous pouvez supprimer ce fichier une fois que vous êtes familiarisé avec le thème.
 */

import { StyleSheet, Text, View } from 'react-native';
import { Colors, Fonts, FontSizes, FontWeights } from './theme';

export function ThemeExamples() {
  return (
    <View style={styles.container}>
      {/* Exemple avec couleur primaire */}
      <View style={styles.primaryCard}>
        <Text style={styles.heading}>Titre Principal</Text>
        <Text style={styles.body}>Texte du corps avec Open Sans</Text>
      </View>

      {/* Exemple avec couleur secondaire */}
      <View style={styles.secondaryCard}>
        <Text style={styles.headingSecondary}>Titre Secondaire</Text>
        <Text style={styles.body}>Texte avec couleur secondaire</Text>
      </View>

      {/* Exemples de polices */}
      <View style={styles.card}>
        <Text style={styles.fontAnton}>Police Anton</Text>
        <Text style={styles.fontBangers}>Police Bangers</Text>
        <Text style={styles.fontCookie}>Police Cookie</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    padding: 16,
  },
  primaryCard: {
    backgroundColor: Colors.card,
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: Colors.primary,
    marginBottom: 16,
  },
  secondaryCard: {
    backgroundColor: Colors.card,
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: Colors.secondary,
    marginBottom: 16,
  },
  card: {
    backgroundColor: Colors.card,
    padding: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  heading: {
    fontFamily: Fonts.heading,
    fontSize: FontSizes['2xl'],
    fontWeight: FontWeights.bold,
    color: Colors.primary,
    marginBottom: 8,
  },
  headingSecondary: {
    fontFamily: Fonts.heading,
    fontSize: FontSizes.xl,
    fontWeight: FontWeights.bold,
    color: Colors.secondary,
    marginBottom: 8,
  },
  body: {
    fontFamily: Fonts.body,
    fontSize: FontSizes.base,
    color: Colors.text,
    lineHeight: 24,
  },
  fontAnton: {
    fontFamily: Fonts.anton,
    fontSize: FontSizes.xl,
    color: Colors.text,
    marginBottom: 8,
  },
  fontBangers: {
    fontFamily: Fonts.bangers,
    fontSize: FontSizes.xl,
    color: Colors.secondary,
    marginBottom: 8,
  },
  fontCookie: {
    fontFamily: Fonts.cookie,
    fontSize: FontSizes.xl,
    color: Colors.primary,
  },
});
