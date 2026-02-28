/**
 * Badge de Sécurité
 * Affiche les caractéristiques de sécurité de uFaranga
 */

import { Colors } from '@/constants/theme';
import { StyleSheet, View } from 'react-native';
import { ThemedText } from './themed';

interface SecurityBadgeProps {
  icon: string;
  label: string;
  color?: string;
}

export function SecurityBadge({ icon, label, color = Colors.primary }: SecurityBadgeProps) {
  return (
    <View style={styles.container}>
      <View style={[styles.iconContainer, { backgroundColor: color }]}>
        <ThemedText style={styles.icon}>{icon}</ThemedText>
      </View>
      <ThemedText style={styles.label}>{label}</ThemedText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginHorizontal: 12,
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  icon: {
    fontSize: 28,
  },
  label: {
    fontSize: 12,
    color: Colors.text,
    textAlign: 'center',
    opacity: 0.8,
  },
});
