import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  static const Color primary = Color(0xFF007BFF);
  static const Color secondary = Color(0xFFF58424);
  static const Color text = Color(0xFFF9F9F9);
  static const Color lightGray = Color(0xFFF8F9FA);
  static const Color background = Color(0xFF00070F);
  static const Color card = Color(0xFF181F27);
  static const Color darkBlue = Color(0xFF000C18);
  static const Color darkGray = Color(0xFF343A40);
  static const Color danger = Color(0xFF8B1538);
}

class ThemeManager {
  // Lazily create TextTheme for the requested font to avoid accessing
  // AssetManifest.json at import time (which causes errors on startup).
  static TextTheme _textThemeFor(String fontKey) {
    switch (fontKey) {
      case 'luckiestGuy':
        return GoogleFonts.luckiestGuyTextTheme();
      case 'ubuntu':
        return GoogleFonts.ubuntuTextTheme();
      case 'anton':
        return GoogleFonts.antonTextTheme();
      case 'allan':
        return GoogleFonts.allanTextTheme();
      case 'bangers':
        return GoogleFonts.bangersTextTheme();
      case 'cookie':
        return GoogleFonts.cookieTextTheme();
      case 'josefinSans':
        return GoogleFonts.josefinSansTextTheme();
      case 'openSans':
      default:
        return GoogleFonts.openSansTextTheme();
    }
  }

  static ThemeData themeForFont(String fontKey, Brightness brightness) {
    final baseTextTheme = _textThemeFor(fontKey);
    // Ensure body text uses Open Sans by default while allowing the selected
    // font to style headings/titles.
    final openSans = GoogleFonts.openSansTextTheme();
    final mergedTextTheme = baseTextTheme.copyWith(
      bodyLarge: openSans.bodyLarge,
      bodyMedium: openSans.bodyMedium,
      bodySmall: openSans.bodySmall,
      labelLarge: openSans.labelLarge,
      labelMedium: openSans.labelMedium,
      labelSmall: openSans.labelSmall,
    );

    final isDark = brightness == Brightness.dark;

    final colorScheme = isDark
        ? ColorScheme.dark(
            primary: AppColors.primary,
            secondary: AppColors.secondary,
            background: AppColors.background,
            surface: AppColors.card,
            error: AppColors.danger,
            onBackground: AppColors.text,
            onSurface: AppColors.text,
            onPrimary: AppColors.text,
            onSecondary: AppColors.text,
          )
        : ColorScheme.light(
            primary: AppColors.primary,
            secondary: AppColors.secondary,
            background: AppColors.lightGray,
            surface: AppColors.card,
            error: AppColors.danger,
            onBackground: AppColors.background,
            onSurface: AppColors.text,
            onPrimary: AppColors.text,
            onSecondary: AppColors.text,
          );

    return ThemeData(
      brightness: brightness,
      colorScheme: colorScheme,
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: colorScheme.background,
      cardColor: AppColors.card,
      appBarTheme: AppBarTheme(
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
      ),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: AppColors.secondary,
        foregroundColor: colorScheme.onSecondary,
      ),
      textTheme: mergedTextTheme.apply(
        bodyColor: AppColors.text,
        displayColor: AppColors.text,
      ),
      useMaterial3: true,
    );
  }
}
