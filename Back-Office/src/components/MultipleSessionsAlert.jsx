import { useState } from 'react';
import { AlertTriangle, Shield, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';

const MultipleSessionsAlert = () => {
  const { activeSessions } = useAuth();
  const [dismissed, setDismissed] = useState(false);
  const [loading, setLoading] = useState(false);

  // Ne rien afficher si pas de sessions multiples ou si l'alerte a été fermée
  if (!activeSessions || 
      !activeSessions.connexion_multiple || 
      activeSessions.nombre_sessions_actives <= 1 ||
      dismissed) {
    return null;
  }

  const handleLogoutOtherSessions = async () => {
    setLoading(true);
    try {
      // Appeler l'endpoint pour déconnecter les autres sessions (pas toutes)
      await apiService.logoutOtherSessions();
      
      setDismissed(true);
    } catch (error) {
      console.error('Erreur lors de la déconnexion des autres sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed top-20 right-6 z-50 max-w-md animate-slide-in">
      <div className="bg-card border border-yellow-500/30 rounded-lg shadow-2xl overflow-hidden">
        {/* Header avec gradient */}
        <div className="bg-gradient-to-r from-yellow-500/20 to-red-500/20 px-4 py-3 border-b border-yellow-500/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center">
                <AlertTriangle className="w-4 h-4 text-yellow-500" />
              </div>
              <h3 className="text-sm font-bold text-yellow-500">
                Alerte de sécurité
              </h3>
            </div>
            <button
              onClick={() => setDismissed(true)}
              className="text-gray-400 hover:text-text transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Contenu */}
        <div className="p-4">
          <div className="flex items-start gap-3 mb-4">
            <Shield className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-text font-medium mb-1">
                Connexions multiples détectées
              </p>
              <p className="text-xs text-gray-400">
                Votre compte est actuellement utilisé sur <span className="text-yellow-500 font-bold">{activeSessions.nombre_sessions_actives} appareils</span> différents.
              </p>
            </div>
          </div>

          {/* Statistiques */}
          <div className="bg-background border border-darkGray rounded-lg p-3 mb-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-400">Sessions actives</span>
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  {Array.from({ length: Math.min(activeSessions.nombre_sessions_actives, 5) }).map((_, i) => (
                    <div key={i} className="w-2 h-2 rounded-full bg-yellow-500"></div>
                  ))}
                </div>
                <span className="text-lg font-bold text-yellow-500">
                  {activeSessions.nombre_sessions_actives}
                </span>
              </div>
            </div>
          </div>

          {/* Message d'avertissement */}
          <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 mb-4">
            <p className="text-xs text-gray-300">
              Si vous ne reconnaissez pas ces connexions, déconnectez immédiatement les autres sessions pour sécuriser votre compte.
            </p>
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <button
              onClick={handleLogoutOtherSessions}
              disabled={loading}
              className="flex-1 px-4 py-2.5 bg-yellow-500 hover:bg-yellow-600 text-background font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-background"></div>
                  Déconnexion...
                </>
              ) : (
                <>
                  <Shield className="w-4 h-4" />
                  Déconnecter les autres
                </>
              )}
            </button>
            <button
              onClick={() => setDismissed(true)}
              className="px-4 py-2.5 text-gray-400 hover:text-text transition-colors text-sm font-medium"
            >
              Plus tard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MultipleSessionsAlert;
