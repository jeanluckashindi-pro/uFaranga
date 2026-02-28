import { Heading, ThemedText, ThemedView } from '@/components/themed';
import { Colors } from '@/constants/theme';
import { ScrollView, StyleSheet, View } from 'react-native';

export default function AccueilScreen() {
  return (
    <ThemedView bg="background" style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* Header */}
        <View style={styles.header}>
          <Heading level={1} color="primary">
            Bienvenue sur uFaranga
          </Heading>
          <ThemedText style={styles.subtitle}>
            Votre solution de transport sans contact
          </ThemedText>
        </View>

        {/* Contenu principal */}
        <View style={styles.content}>
          <ThemedText style={styles.paragraph}>
            uFaranga est une solution innovante et strictement sécurisée, 
            conçue pour moderniser le transport urbain sans contact.
          </ThemedText>

          <ThemedText style={styles.paragraph}>
            Elle permet aux usagers d'accéder aux services de transport et 
            de valider leur passage sans paiement physique, grâce à des 
            technologies numériques fiables et performantes.
          </ThemedText>

          <ThemedText style={styles.paragraph}>
            L'application repose sur une architecture logicielle robuste et 
            bien structurée, développée selon des principes d'ingénierie 
            rigoureux afin de garantir la sécurité des données, la stabilité 
            du système et une excellente performance, même en environnement 
            à forte charge.
          </ThemedText>
        </View>

      </ScrollView>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    marginTop: 40,
    marginBottom: 30,
  },
  subtitle: {
    fontSize: 16,
    color: Colors.secondary,
    marginTop: 8,
    opacity: 0.9,
  },
  content: {
    gap: 20,
  },
  paragraph: {
    fontSize: 16,
    lineHeight: 26,
    color: Colors.text,
    opacity: 0.85,
    textAlign: 'justify',
  },
});
