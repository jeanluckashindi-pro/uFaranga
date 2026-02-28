import { useFonts } from 'expo-font';

/**
 * Hook pour charger les polices Google Fonts du projet
 * Retourne un booléen indiquant si les polices sont chargées
 */
export function useProjectFonts() {
  const [fontsLoaded] = useFonts({
    // Polices principales
    'OpenSans-Regular': require('../assets/fonts/OpenSans-Regular.ttf'),
    'OpenSans-Bold': require('../assets/fonts/OpenSans-Bold.ttf'),
    'JosefinSans-Regular': require('../assets/fonts/JosefinSans-Regular.ttf'),
    'JosefinSans-Bold': require('../assets/fonts/JosefinSans-Bold.ttf'),
    
    // Polices supplémentaires
    'Anton-Regular': require('../assets/fonts/Anton-Regular.ttf'),
    'Antonio-Regular': require('../assets/fonts/Antonio-Regular.ttf'),
    'Bangers-Regular': require('../assets/fonts/Bangers-Regular.ttf'),
    'Cookie-Regular': require('../assets/fonts/Cookie-Regular.ttf'),
    'Allan-Regular': require('../assets/fonts/Allan-Regular.ttf'),
    'LuckiestGuy-Regular': require('../assets/fonts/LuckiestGuy-Regular.ttf'),
    'Ubuntu-Regular': require('../assets/fonts/Ubuntu-Regular.ttf'),
  });

  return fontsLoaded;
}
