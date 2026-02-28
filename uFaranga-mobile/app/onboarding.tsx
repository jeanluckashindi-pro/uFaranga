/**
 * Onboarding - Présentation de uFaranga
 * Écrans d'introduction pour comprendre l'application
 */

import { ThemedText, ThemedView } from '@/components/themed';
import { Colors } from '@/constants/theme';
import { useRouter } from 'expo-router';
import { useRef, useState } from 'react';
import {
    Animated,
    Dimensions,
    FlatList,
    StyleSheet,
    TouchableOpacity,
    View,
} from 'react-native';

const { width, height } = Dimensions.get('window');

interface OnboardingSlide {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
}

const slides: OnboardingSlide[] = [
  {
    id: '1',
    title: 'Transport Sans Contact',
    description:
      'Accédez aux services de transport urbain sans paiement physique. Une expérience moderne et fluide.',
    icon: '🚌',
    color: Colors.primary,
  },
  {
    id: '2',
    title: 'Sécurité Maximale',
    description:
      'Architecture strictement sécurisée avec chiffrement des données. Vos informations sont protégées à tout moment.',
    icon: '🔒',
    color: Colors.secondary,
  },
  {
    id: '3',
    title: 'Technologie Innovante',
    description:
      'Système robuste et performant, conçu pour fonctionner même en environnement à forte charge.',
    icon: '⚡',
    color: Colors.primary,
  },
  {
    id: '4',
    title: 'Validation Instantanée',
    description:
      'Validez votre passage en un instant grâce à des technologies numériques fiables et rapides.',
    icon: '✓',
    color: Colors.secondary,
  },
];

export default function OnboardingScreen() {
  const router = useRouter();
  const [currentIndex, setCurrentIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);
  const scrollX = useRef(new Animated.Value(0)).current;

  const handleNext = () => {
    if (currentIndex < slides.length - 1) {
      flatListRef.current?.scrollToIndex({
        index: currentIndex + 1,
        animated: true,
      });
    } else {
      router.replace('/(tabs)');
    }
  };

  const handleSkip = () => {
    router.replace('/(tabs)');
  };

  const onViewableItemsChanged = useRef(({ viewableItems }: any) => {
    if (viewableItems.length > 0) {
      setCurrentIndex(viewableItems[0].index || 0);
    }
  }).current;

  const viewabilityConfig = useRef({
    itemVisiblePercentThreshold: 50,
  }).current;

  const renderSlide = ({ item, index }: { item: OnboardingSlide; index: number }) => {
    return (
      <View style={styles.slide}>
        {/* Cercle décoratif */}
        <View style={[styles.decorativeCircle, { backgroundColor: item.color }]} />

        {/* Icône */}
        <View style={[styles.iconContainer, { backgroundColor: item.color }]}>
          <ThemedText style={styles.icon}>{item.icon}</ThemedText>
        </View>

        {/* Contenu */}
        <View style={styles.textContainer}>
          <ThemedText style={styles.title}>{item.title}</ThemedText>
          <ThemedText style={styles.description}>{item.description}</ThemedText>
        </View>
      </View>
    );
  };

  return (
    <ThemedView bg="background" style={styles.container}>
      {/* Header avec bouton Skip */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleSkip} style={styles.skipButton}>
          <ThemedText style={styles.skipText}>Passer</ThemedText>
        </TouchableOpacity>
      </View>

      {/* Slides */}
      <FlatList
        ref={flatListRef}
        data={slides}
        renderItem={renderSlide}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        keyExtractor={(item) => item.id}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { x: scrollX } } }],
          { useNativeDriver: false }
        )}
        onViewableItemsChanged={onViewableItemsChanged}
        viewabilityConfig={viewabilityConfig}
      />

      {/* Footer avec indicateurs et bouton */}
      <View style={styles.footer}>
        {/* Indicateurs de pagination */}
        <View style={styles.pagination}>
          {slides.map((_, index) => {
            const inputRange = [
              (index - 1) * width,
              index * width,
              (index + 1) * width,
            ];

            const dotWidth = scrollX.interpolate({
              inputRange,
              outputRange: [8, 24, 8],
              extrapolate: 'clamp',
            });

            const opacity = scrollX.interpolate({
              inputRange,
              outputRange: [0.3, 1, 0.3],
              extrapolate: 'clamp',
            });

            return (
              <Animated.View
                key={index}
                style={[
                  styles.dot,
                  {
                    width: dotWidth,
                    opacity,
                    backgroundColor:
                      currentIndex === index ? Colors.primary : Colors.lightGray,
                  },
                ]}
              />
            );
          })}
        </View>

        {/* Bouton Suivant/Commencer */}
        <TouchableOpacity
          onPress={handleNext}
          style={[
            styles.nextButton,
            {
              backgroundColor:
                currentIndex === slides.length - 1
                  ? Colors.secondary
                  : Colors.primary,
            },
          ]}
        >
          <ThemedText style={styles.nextButtonText}>
            {currentIndex === slides.length - 1 ? 'Commencer' : 'Suivant'}
          </ThemedText>
        </TouchableOpacity>
      </View>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    paddingTop: 50,
    paddingHorizontal: 20,
    alignItems: 'flex-end',
  },
  skipButton: {
    padding: 10,
  },
  skipText: {
    fontSize: 16,
    color: Colors.secondary,
  },
  slide: {
    width,
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  decorativeCircle: {
    position: 'absolute',
    width: width * 1.5,
    height: width * 1.5,
    borderRadius: width * 0.75,
    top: -width * 0.5,
    opacity: 0.1,
  },
  iconContainer: {
    width: 140,
    height: 140,
    borderRadius: 70,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 40,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  icon: {
    fontSize: 70,
  },
  textContainer: {
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: Colors.text,
    textAlign: 'center',
    marginBottom: 20,
  },
  description: {
    fontSize: 16,
    color: Colors.text,
    textAlign: 'center',
    lineHeight: 24,
    opacity: 0.8,
  },
  footer: {
    paddingBottom: 50,
    paddingHorizontal: 40,
  },
  pagination: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  dot: {
    height: 8,
    borderRadius: 4,
    marginHorizontal: 4,
  },
  nextButton: {
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  nextButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.text,
    letterSpacing: 1,
  },
});
