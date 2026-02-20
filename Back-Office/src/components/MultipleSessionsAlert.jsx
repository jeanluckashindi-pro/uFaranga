import { useState } from 'react';
import { AlertTriangle, X } from 'lucide-react';
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
      await apiService.logoutOtherSessions();
      setDismissed(true);
    } catch (error) {
      console.error('Erreur lors de la déconnexion des autres sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed top-20 right-6 z-50 max-w-sm animate-slide-in">
      <div className="bg-card border border-yellow-500/20 rounded-xl shadow-2xl overflow-hidden backdrop-blur-sm">
        <div className="p-5">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-yellow-500/10 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-yellow-500" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-text">Connexions multiples</h3>
                <p className="text-xs text-gray-400 mt-0.5">
                  {activeSessions.nombre_sessions_actives} sessions actives
                </p>
              </div>
            </div>
            <button
              onClick={() => setDismissed(true)}
              className="text-gray-400 hover:text-text transition-colors p-1"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Message */}
          <p className="text-sm text-gray-300 mb-5 leading-relaxed">
            Votre compte est utilisé sur plusieurs appareils. Déconnectez les sessions non reconnues.
          </p>

          {/* Actions */}
          <div className="flex gap-2">
            <button
              onClick={handleLogoutOtherSessions}
              disabled={loading}
              className="flex-1 px-4 py-2.5 bg-yellow-500 hover:bg-yellow-600 text-background font-medium rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            >
              {loading ? 'Déconnexion...' : 'Sécuriser'}
            </button>
            <button
              onClick={() => setDismissed(true)}
              className="px-4 py-2.5 text-gray-400 hover:text-text hover:bg-background/50 rounded-lg transition-all text-sm font-medium"
            >
              Ignorer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MultipleSessionsAlert;
