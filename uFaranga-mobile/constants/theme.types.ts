/**
 * Types TypeScript pour le thème uFaranga
 */

export type ColorName = 
  | 'primary'
  | 'secondary'
  | 'text'
  | 'background'
  | 'card'
  | 'darkBlue'
  | 'darkGray'
  | 'lightGray'
  | 'danger';

export type FontName = 
  | 'body'
  | 'heading'
  | 'anton'
  | 'antonio'
  | 'bangers'
  | 'cookie'
  | 'allan'
  | 'luckiestGuy'
  | 'ubuntu';

export type FontSize = 
  | 'xs'
  | 'sm'
  | 'base'
  | 'lg'
  | 'xl'
  | '2xl'
  | '3xl'
  | '4xl';

export type FontWeight = 
  | 'regular'
  | 'medium'
  | 'semibold'
  | 'bold';

export interface ThemeColors {
  primary: string;
  secondary: string;
  text: string;
  background: string;
  card: string;
  darkBlue: string;
  darkGray: string;
  lightGray: string;
  danger: string;
}

export interface ThemeFonts {
  body: string;
  heading: string;
  anton: string;
  antonio: string;
  bangers: string;
  cookie: string;
  allan: string;
  luckiestGuy: string;
  ubuntu: string;
}
