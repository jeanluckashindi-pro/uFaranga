/**
 * Composants thématisés pour uFaranga
 * Utilisation simplifiée des couleurs et polices du projet
 */

import { Colors, Fonts, FontSizes } from '@/constants/theme';
import type { ColorName, FontName, FontSize } from '@/constants/theme.types';
import { Text as RNText, View as RNView, StyleSheet, TextProps, ViewProps } from 'react-native';

// Props étendues pour Text
interface ThemedTextProps extends TextProps {
  color?: ColorName | string;
  font?: FontName;
  size?: FontSize | number;
  bold?: boolean;
}

// Props étendues pour View
interface ThemedViewProps extends ViewProps {
  bg?: ColorName | string;
  card?: boolean;
}

/**
 * Composant Text thématisé
 * Usage: <ThemedText color="primary" font="heading" size="xl">Mon texte</ThemedText>
 */
export function ThemedText({ 
  color = 'text', 
  font = 'body', 
  size = 'base',
  bold = false,
  style, 
  ...props 
}: ThemedTextProps) {
  const textColor = color in Colors ? Colors[color as ColorName] : color;
  const fontSize = typeof size === 'number' ? size : FontSizes[size];
  const fontFamily = Fonts[font];

  return (
    <RNText
      style={[
        {
          color: textColor,
          fontSize,
          fontFamily,
          fontWeight: bold ? '700' : '400',
        },
        style,
      ]}
      {...props}
    />
  );
}

/**
 * Composant View thématisé
 * Usage: <ThemedView bg="background" card>Contenu</ThemedView>
 */
export function ThemedView({ 
  bg = 'background', 
  card = false,
  style, 
  ...props 
}: ThemedViewProps) {
  const backgroundColor = bg in Colors ? Colors[bg as ColorName] : bg;

  return (
    <RNView
      style={[
        { backgroundColor },
        card && styles.card,
        style,
      ]}
      {...props}
    />
  );
}

/**
 * Composant Heading (titre) thématisé
 * Usage: <Heading level={1}>Mon titre</Heading>
 */
interface HeadingProps extends ThemedTextProps {
  level?: 1 | 2 | 3 | 4 | 5 | 6;
}

export function Heading({ level = 1, size, ...props }: HeadingProps) {
  const headingSizes: Record<number, FontSize> = {
    1: '4xl',
    2: '3xl',
    3: '2xl',
    4: 'xl',
    5: 'lg',
    6: 'base',
  };

  return (
    <ThemedText
      font="heading"
      size={size || headingSizes[level]}
      bold
      {...props}
    />
  );
}

/**
 * Composant Card thématisé
 * Usage: <Card>Contenu de la carte</Card>
 */
interface CardProps extends ThemedViewProps {
  borderColor?: ColorName | string;
}

export function Card({ borderColor, style, ...props }: CardProps) {
  const borderLeftColor = borderColor 
    ? (borderColor in Colors ? Colors[borderColor as ColorName] : borderColor)
    : Colors.primary;

  return (
    <ThemedView
      bg="card"
      style={[
        styles.card,
        { borderLeftColor },
        style,
      ]}
      {...props}
    />
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    borderRadius: 8,
    borderLeftWidth: 4,
    marginBottom: 16,
  },
});
