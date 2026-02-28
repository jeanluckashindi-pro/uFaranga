import { AnimatedLogo } from '@/components/animated-logo';
import { SecurityBadge } from '@/components/security-badge';
import { ThemedText } from '@/components/themed';
import { Colors } from '@/constants/theme';
import { useRouter } from 'expo-router';
import { useEffect, useRef } from 'react';
import { Animated, Dimensions, StyleSheet, View } from 'react-native';

const { width, height } = Dimensions.get('window');

export default function SplashScreen() {
  const router = useRouter();
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideUpAnim = useRef(new Animated.Value(30)).current;
  const badgesFadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.sequence([
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(slideUpAnim, {
          toValue: 0,
          duration: 800,
          useNativeDriver: true,
        }),
      ]),
      Animated.timing(badgesFadeAnim, {
        toValue: 1,
        duration: 600,
        delay: 200,
        useNativeDriver: true,
      }),
    ]).start();

    const timer = setTimeout(() => {
      router.replace('/onboarding');
    }, 3500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <View style={[styles.circle, styles.circle1]} />
      <View style={[styles.circle, styles.circle2]} />
      <View style={[styles.circle, styles.circle3]} />

      <Animated.View
        style={[
          styles.logoSection,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideUpAnim }],
          },
        ]}
      >
        <AnimatedLogo size={140} showText={false} />
        
        <View style={styles.titleContainer}>
          <ThemedText style={styles.appName}>uFaranga</ThemedText>
          <ThemedText style={styles.tagline}>
            Transport Sans Contact
          </ThemedText>
        </View>
      </Animated.View>

      <Animated.View
        style={[
          styles.badgesContainer,
          { opacity: badgesFadeAnim },
        ]}
      >
        <SecurityBadge icon="🔒" label="Sécurisé" color={Colors.primary} />
        <SecurityBadge icon="⚡" label="Innovant" color={Colors.secondary} />
        <SecurityBadge icon="✓" label="Fiable" color={Colors.primary} />
      </Animated.View>

      <Animated.View style={[styles.footer, { opacity: fadeAnim }]}>
        <ThemedText style={styles.footerText}>
          Architecture Robuste • Performance Optimale
        </ThemedText>
        <ThemedText style={[styles.footerText, styles.version]}>
          Version 1.0.0
        </ThemedText>
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  circle: {
    position: 'absolute',
    borderRadius: 1000,
    opacity: 0.08,
  },
  circle1: {
    width: width * 1.5,
    height: width * 1.5,
    backgroundColor: Colors.primary,
    top: -width * 0.5,
    right: -width * 0.3,
  },
  circle2: {
    width: width * 1.2,
    height: width * 1.2,
    backgroundColor: Colors.secondary,
    bottom: -width * 0.4,
    left: -width * 0.4,
  },
  circle3: {
    width: width * 0.8,
    height: width * 0.8,
    backgroundColor: Colors.primary,
    top: height * 0.3,
    left: -width * 0.2,
  },
  logoSection: {
    alignItems: 'center',
    marginBottom: 60,
  },
  titleContainer: {
    marginTop: 30,
    alignItems: 'center',
  },
  appName: {
    fontSize: 48,
    fontWeight: 'bold',
    color: Colors.text,
    letterSpacing: 3,
    textAlign: 'center',
  },
  tagline: {
    fontSize: 16,
    color: Colors.secondary,
    marginTop: 8,
    textAlign: 'center',
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
  badgesContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 40,
  },
  footer: {
    position: 'absolute',
    bottom: 40,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 11,
    color: Colors.text,
    opacity: 0.5,
    letterSpacing: 1,
    textAlign: 'center',
  },
  version: {
    marginTop: 4,
    fontSize: 10,
  },
});
