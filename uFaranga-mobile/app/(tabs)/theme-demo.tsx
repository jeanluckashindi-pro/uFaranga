/**
 * Page de démonstration du thème uFaranga
 * Vous pouvez utiliser cette page pour tester le thème
 */

import { Card, Heading, ThemedText, ThemedView } from '@/components/themed';
import { Colors } from '@/constants/theme';
import { ScrollView, StyleSheet } from 'react-native';

export default function ThemeDemoScreen() {
  return (
    <ScrollView style={styles.container}>
      <ThemedView bg="background" style={styles.content}>
        
        {/* En-tête */}
        <ThemedView style={styles.header}>
          <Heading level={1} color="primary">
            uFaranga
          </Heading>
          <ThemedText size="lg" color="secondary">
            Démonstration du Thème
          </ThemedText>
        </ThemedView>

        {/* Section Couleurs Principales */}
        <Heading level={2} style={styles.sectionTitle}>
          Couleurs Principales
        </Heading>

        <Card borderColor="primary">
          <Heading level={3} color="primary">
            Couleur Primaire
          </Heading>
          <ThemedText>
            Utilisée pour les éléments principaux et les actions importantes.
          </ThemedText>
          <ThemedText size="sm" style={styles.colorCode}>
            {Colors.primary}
          </ThemedText>
        </Card>

        <Card borderColor="secondary">
          <Heading level={3} color="secondary">
            Couleur Secondaire
          </Heading>
          <ThemedText>
            Utilisée pour les accents et les éléments secondaires.
          </ThemedText>
          <ThemedText size="sm" style={styles.colorCode}>
            {Colors.secondary}
          </ThemedText>
        </Card>

        <Card borderColor="danger">
          <Heading level={3} color="danger">
            Couleur Danger
          </Heading>
          <ThemedText>
            Utilisée pour les alertes et les messages d'erreur.
          </ThemedText>
          <ThemedText size="sm" style={styles.colorCode}>
            {Colors.danger}
          </ThemedText>
        </Card>

        {/* Section Typographie */}
        <Heading level={2} style={styles.sectionTitle}>
          Typographie
        </Heading>

        <Card>
          <Heading level={1}>Heading 1</Heading>
          <Heading level={2}>Heading 2</Heading>
          <Heading level={3}>Heading 3</Heading>
          <Heading level={4}>Heading 4</Heading>
          
          <ThemedText size="xl" style={styles.textSample}>
            Texte XL - Open Sans
          </ThemedText>
          <ThemedText size="lg" style={styles.textSample}>
            Texte Large - Open Sans
          </ThemedText>
          <ThemedText size="base" style={styles.textSample}>
            Texte Base - Open Sans
          </ThemedText>
          <ThemedText size="sm" style={styles.textSample}>
            Texte Small - Open Sans
          </ThemedText>
        </Card>

        {/* Section Polices Décoratives */}
        <Heading level={2} style={styles.sectionTitle}>
          Polices Décoratives
        </Heading>

        <Card>
          <ThemedText font="anton" size="2xl" color="primary" style={styles.decorativeFont}>
            Anton Font
          </ThemedText>
          <ThemedText font="bangers" size="2xl" color="secondary" style={styles.decorativeFont}>
            Bangers Font
          </ThemedText>
          <ThemedText font="cookie" size="2xl" color="primary" style={styles.decorativeFont}>
            Cookie Font
          </ThemedText>
          <ThemedText font="luckiestGuy" size="2xl" color="secondary" style={styles.decorativeFont}>
            Luckiest Guy
          </ThemedText>
        </Card>

        {/* Section Exemples d'Usage */}
        <Heading level={2} style={styles.sectionTitle}>
          Exemples d'Usage
        </Heading>

        <Card borderColor="primary">
          <Heading level={3} color="primary">
            Carte d'Information
          </Heading>
          <ThemedText style={styles.paragraph}>
            Cette carte utilise la couleur primaire pour la bordure et le titre.
            Le texte utilise la police Open Sans par défaut.
          </ThemedText>
          <ThemedText bold color="primary">
            Texte en gras avec couleur primaire
          </ThemedText>
        </Card>

        <Card borderColor="secondary">
          <Heading level={3} color="secondary">
            Carte d'Action
          </Heading>
          <ThemedText style={styles.paragraph}>
            Cette carte utilise la couleur secondaire pour attirer l'attention
            sur une action ou un élément important.
          </ThemedText>
          <ThemedText bold color="secondary">
            Appel à l'action
          </ThemedText>
        </Card>

        {/* Footer */}
        <ThemedView style={styles.footer}>
          <ThemedText size="sm" style={styles.footerText}>
            Thème uFaranga - Tous les composants sont personnalisables
          </ThemedText>
        </ThemedView>

      </ThemedView>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    padding: 16,
  },
  header: {
    marginBottom: 24,
    paddingVertical: 16,
  },
  sectionTitle: {
    marginTop: 24,
    marginBottom: 16,
  },
  colorCode: {
    marginTop: 8,
    fontFamily: 'monospace',
    opacity: 0.7,
  },
  textSample: {
    marginVertical: 4,
  },
  decorativeFont: {
    marginVertical: 8,
    textAlign: 'center',
  },
  paragraph: {
    marginBottom: 12,
    lineHeight: 22,
  },
  footer: {
    marginTop: 32,
    marginBottom: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: Colors.card,
    alignItems: 'center',
  },
  footerText: {
    opacity: 0.6,
  },
});
