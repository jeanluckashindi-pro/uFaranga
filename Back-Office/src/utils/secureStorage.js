/**
 * Gestionnaire de stockage sécurisé pour les données sensibles
 * Utilise sessionStorage pour la persistance pendant la session
 * et localStorage uniquement pour rememberMe
 */

class SecureStorage {
  constructor() {
    // Stockage en mémoire pour accès rapide
    this.memoryStorage = {
      accessToken: null,
      refreshToken: null,
      user: null,
      sessionId: null,
      rememberMe: false,
    };

    // Générer un ID de session unique
    this.sessionId = this.generateSessionId();
    
    // Charger rememberMe depuis localStorage si existe
    const savedRememberMe = localStorage.getItem('rememberMe');
    if (savedRememberMe === 'true') {
      this.memoryStorage.rememberMe = true;
    }

    // Charger les données depuis sessionStorage au démarrage
    this.loadFromSessionStorage();
  }

  /**
   * Charger les données depuis sessionStorage
   */
  loadFromSessionStorage() {
    try {
      const accessToken = sessionStorage.getItem('accessToken');
      const refreshToken = sessionStorage.getItem('refreshToken');
      const userData = sessionStorage.getItem('userData');

      if (accessToken) this.memoryStorage.accessToken = accessToken;
      if (refreshToken) this.memoryStorage.refreshToken = refreshToken;
      if (userData) this.memoryStorage.user = JSON.parse(userData);
    } catch (e) {
      console.error('Erreur lors du chargement depuis sessionStorage:', e);
    }
  }

  /**
   * Générer un ID de session unique
   */
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Stocker le token d'accès
   */
  setAccessToken(token) {
    this.memoryStorage.accessToken = token;
    if (token) {
      sessionStorage.setItem('accessToken', token);
    } else {
      sessionStorage.removeItem('accessToken');
    }
  }

  /**
   * Récupérer le token d'accès
   */
  getAccessToken() {
    return this.memoryStorage.accessToken || sessionStorage.getItem('accessToken');
  }

  /**
   * Stocker le refresh token
   */
  setRefreshToken(token) {
    this.memoryStorage.refreshToken = token;
    if (token) {
      sessionStorage.setItem('refreshToken', token);
    } else {
      sessionStorage.removeItem('refreshToken');
    }
  }

  /**
   * Récupérer le refresh token
   */
  getRefreshToken() {
    return this.memoryStorage.refreshToken || sessionStorage.getItem('refreshToken');
  }

  /**
   * Stocker les données utilisateur
   */
  setUser(user) {
    this.memoryStorage.user = user;
    if (user) {
      sessionStorage.setItem('userData', JSON.stringify(user));
    } else {
      sessionStorage.removeItem('userData');
    }
  }

  /**
   * Récupérer les données utilisateur
   */
  getUser() {
    if (this.memoryStorage.user) {
      return this.memoryStorage.user;
    }
    
    try {
      const userData = sessionStorage.getItem('userData');
      if (userData) {
        this.memoryStorage.user = JSON.parse(userData);
        return this.memoryStorage.user;
      }
    } catch (e) {
      console.error('Erreur lors de la lecture des données utilisateur:', e);
    }
    
    return null;
  }

  /**
   * Vérifier si une session est active
   */
  hasActiveSession() {
    return this.getAccessToken() !== null;
  }

  /**
   * Nettoyer toutes les données de session
   */
  clearSession() {
    const rememberMe = this.memoryStorage.rememberMe;
    
    // Nettoyer la mémoire
    this.memoryStorage = {
      accessToken: null,
      refreshToken: null,
      user: null,
      sessionId: null,
      rememberMe: false,
    };
    
    // Nettoyer sessionStorage
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
    sessionStorage.removeItem('userData');
    
    // Nettoyer localStorage (anciennes sessions)
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userData');
    
    // Ne pas supprimer rememberMe si c'était activé
    if (!rememberMe) {
      localStorage.removeItem('rememberMe');
    }
    
    // Nettoyer les cookies si nécessaire
    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
  }

  /**
   * Obtenir l'ID de session
   */
  getSessionId() {
    return this.sessionId;
  }

  /**
   * Définir le mode "Se souvenir de moi"
   */
  setRememberMe(remember) {
    this.memoryStorage.rememberMe = remember;
    if (remember) {
      localStorage.setItem('rememberMe', 'true');
    } else {
      localStorage.removeItem('rememberMe');
    }
  }

  /**
   * Vérifier si "Se souvenir de moi" est activé
   */
  getRememberMe() {
    return this.memoryStorage.rememberMe || localStorage.getItem('rememberMe') === 'true';
  }

  /**
   * Vérifier si le token est expiré
   */
  isTokenExpired(token) {
    if (!token) return true;
    
    try {
      // Décoder le JWT (partie payload)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp * 1000; // Convertir en millisecondes
      return Date.now() >= exp;
    } catch (e) {
      return true;
    }
  }

  /**
   * Obtenir le temps restant avant expiration (en secondes)
   */
  getTokenTimeRemaining(token) {
    if (!token) return 0;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp * 1000;
      const remaining = Math.max(0, exp - Date.now());
      return Math.floor(remaining / 1000);
    } catch (e) {
      return 0;
    }
  }
}

// Instance singleton
const secureStorage = new SecureStorage();

// Nettoyer la session quand l'onglet/fenêtre est fermé
window.addEventListener('beforeunload', () => {
  // Note: Les données en mémoire seront automatiquement perdues
  // On peut logger la déconnexion si nécessaire
  console.log('Session terminée');
});

// Nettoyer la session en cas d'inactivité prolongée
let inactivityTimer;

const resetInactivityTimer = () => {
  // Ne pas déconnecter si "Se souvenir de moi" est activé
  if (secureStorage.getRememberMe()) {
    return;
  }
  
  const INACTIVITY_TIMEOUT = 30 * 60 * 1000; // 30 minutes
  
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(() => {
    console.warn('Session expirée par inactivité');
    secureStorage.clearSession();
    window.location.href = '/login';
  }, INACTIVITY_TIMEOUT);
};

// Écouter les événements d'activité
['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event => {
  document.addEventListener(event, resetInactivityTimer, true);
});

// Démarrer le timer
resetInactivityTimer();

export default secureStorage;
