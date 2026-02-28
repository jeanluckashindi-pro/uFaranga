/**
 * Logo Animé uFaranga
 * Composant réutilisable avec animations
 */

import { Colors } from '@/constants/theme';
import { useEffect, useRef } from 'react';
import { Animated, StyleSheet, View } from 'react-native';
import { ThemedText } from './themed';

interface AnimatedLogoProps {
  size?: number;
  showText?: boolean;
}

export function AnimatedLogo({ size = 120, showText = true }: AnimatedLogoProps) {
  const rotateAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    // Animation de rotation continue
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 3000,
        useNativeDriver: true,
      })
    ).start();

    // Animation de pulsation
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <View style={styles.container}>
      {/* Cercle extérieur animé */}
      <Animated.View
        style={[
          styles.outerCircle,
          {
            width: size * 1.3,
            height: size * 1.3,
            borderRadius: size * 0.65,
            transform: [{ rotate }],
          },
        ]}
      />

      {/* Logo principal */}
      <Animated.View
        style={[
          styles.logoCircle,
          {
            width: size,
            height: size,
            borderRadius: size / 2,
            transform: [{ scale: pulseAnim }],
          },
        ]}
      >
        <ThemedText style={[styles.logoText, { fontSize: size * 0.53 }]}>
          u
        </ThemedText>
      </Animated.View>

      {/* Texte optionnel */}
      {showText && (
        <View style={styles.textContainer}>
          <ThemedText style={styles.appName}>Faranga</ThemedText>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  outerCircle: {
    position: 'absolute',
    borderWidth: 2,
    borderColor: Colors.primary,
    borderStyle: 'dashed',
    opacity: 0.3,
  },
  logoCircle: {
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 10,
  },
  logoText: {
    fontWeight: 'bold',
    color: Colors.text,
  },
  textContainer: {
    marginTop: 20,
  },
  appName: {
    fontSize: 32,
    fontWeight: 'bold',
    color: Colors.text,
    letterSpacing: 2,
  },
});
