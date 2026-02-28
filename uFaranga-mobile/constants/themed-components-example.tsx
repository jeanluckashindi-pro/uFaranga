/**
 * 📚 Exemples d'utilisation des composants thématisés
 * 
 * Ce fichier montre comment utiliser les composants ThemedText, ThemedView, Heading et Card.
 * Vous pouvez supprimer ce fichier une fois familiarisé avec les composants.
 */

import { Card, Heading, ThemedText, ThemedView } from '@/components/themed';
import { ScrollView, StyleSheet } from 'react-native';

export function ThemedComponentsExample() {
  return (
    <ScrollView style={styles.container}>
      <ThemedView bg="background" style={styles.section}>
        
        {/* Exemples de Headings */}
        <Heading level={1} color="primary">Titre H1</Heading>
        <Heading level={2} color="secondary">Titre H2</Heading>
        <Heading level={3}>Titre H3</Heading>
        
        {/* Exemples de Text */}
        <ThemedText size="lg">
          Texte normal avec la police Open Sans
        </ThemedText>
        
        <ThemedText color="secondary" bold>
          Texte en gras avec couleur secondaire
        </ThemedText>
        
        <ThemedText font="bangers" size="xl" color="primary">
          Texte avec police Bangers
        </ThemedText>
        
        {/* Exemples de Cards */}
        <Card borderColor="primary">
          <Heading level={4} color="primary">Carte avec bordure bleue</Heading>
          <ThemedText>
            Contenu de la carte avec style par défaut
          </ThemedText>
        </Card>
        
        <Card borderColor="secondary">
          <Heading level={4} color="secondary">Carte avec bordure orange</Heading>
          <ThemedText>
            Une autre carte avec une couleur différente
          </ThemedText>
        </Card>
        
        <Card borderColor="danger">
          <Heading level={4} color="danger">Alerte importante</Heading>
          <ThemedText>
            Carte avec bordure rouge pour les messages d'erreur
          </ThemedText>
        </Card>
        
        {/* Exemple avec polices décoratives */}
        <ThemedView bg="card" style={styles.fontsDemo}>
          <ThemedText font="anton" size="2xl" color="primary">
            Police Anton
          </ThemedText>
          <ThemedText font="cookie" size="2xl" color="secondary">
            Police Cookie
          </ThemedText>
          <ThemedText font="luckiestGuy" size="2xl" color="primary">
            Luckiest Guy
          </ThemedText>
        </ThemedView>
        
      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  section: {
    padding: 16,
  },
  fontsDemo: {
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
    alignItems: 'center',
  },
});
