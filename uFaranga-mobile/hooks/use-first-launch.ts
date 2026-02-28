/**
 * Hook pour détecter le premier lancement de l'application
 * Utilise le localStorage pour le web et une variable en mémoire pour mobile
 */

import { useEffect, useState } from 'react';
import { Platform } from 'react-native';

const FIRST_LAUNCH_KEY = 'ufaranga_first_launch';

// Variable en mémoire pour mobile (simple pour la démo)
let hasLaunchedBefore = false;

export function useFirstLaunch() {
  const [isFirstLaunch, setIsFirstLaunch] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkFirstLaunch();
  }, []);

  const checkFirstLaunch = async () => {
    try {
      if (Platform.OS === 'web') {
        const hasLaunched = localStorage.getItem(FIRST_LAUNCH_KEY);
        setIsFirstLaunch(hasLaunched === null);
      } else {
        // Pour mobile, utiliser la variable en mémoire
        setIsFirstLaunch(!hasLaunchedBefore);
      }
    } catch (error) {
      console.error('Error checking first launch:', error);
      setIsFirstLaunch(true);
    } finally {
      setIsLoading(false);
    }
  };

  const markAsLaunched = async () => {
    try {
      if (Platform.OS === 'web') {
        localStorage.setItem(FIRST_LAUNCH_KEY, 'false');
      } else {
        hasLaunchedBefore = true;
      }
      setIsFirstLaunch(false);
    } catch (error) {
      console.error('Error marking as launched:', error);
    }
  };

  const resetFirstLaunch = async () => {
    try {
      if (Platform.OS === 'web') {
        localStorage.removeItem(FIRST_LAUNCH_KEY);
      } else {
        hasLaunchedBefore = false;
      }
      setIsFirstLaunch(true);
    } catch (error) {
      console.error('Error resetting first launch:', error);
    }
  };

  return {
    isFirstLaunch,
    isLoading,
    markAsLaunched,
    resetFirstLaunch,
  };
}
