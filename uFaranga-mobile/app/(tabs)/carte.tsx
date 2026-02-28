import { Heading, ThemedText, ThemedView } from '@/components/themed';
import { Colors } from '@/constants/theme';
import { ScrollView, StyleSheet, View } from 'react-native';

export default function CarteScreen() {
  return (
    <ThemedView bg="background" style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        <View style={styles.header}>
          <Heading level={1} color="primary">
            Carte Virtuelle
          </Heading>
        </View>

        <View style={styles.content}>
          <ThemedText style={styles.text}>
            Page Carte Virtuelle - En cours de développement
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
  content: {
    gap: 20,
  },
  text: {
    fontSize: 16,
    lineHeight: 26,
    color: Colors.text,
    opacity: 0.85,
  },
});
