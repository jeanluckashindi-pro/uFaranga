import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Input, Button, Alert } from '../../components/common';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [formData, setFormData] = useState({
    username: '' // Email ou téléphone
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Rediriger si déjà connecté
  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      navigate('/admin/dashboard', { replace: true });
    }
  }, [isAuthenticated, authLoading, navigate]);

  // Fonction de validation côté client
  const validateUsername = (username) => {
    if (!username.trim()) {
      return 'Saisissez votre adresse e-mail ou votre numéro de téléphone.';
    }

    // Vérification e-mail
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (emailRegex.test(username)) {
      return null; // E-mail valide
    }

    // Vérification téléphone (9 à 15 chiffres, + optionnel, espaces et tirets ignorés)
    const phoneRegex = /^\+?[\d\s-]{9,15}$/;
    const cleanPhone = username.replace(/[\s-]/g, '');
    const phoneDigitsOnly = cleanPhone.replace(/^\+/, '');
    
    if (phoneRegex.test(username) && phoneDigitsOnly.length >= 9 && phoneDigitsOnly.length <= 15) {
      return null; // Téléphone valide
    }

    return 'Saisissez une adresse e-mail valide ou un numéro de téléphone valide (9 à 15 chiffres).';
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Effacer les messages quand l'utilisateur tape
    if (error) setError('');
    if (success) setSuccess(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    // Validation côté client
    const usernameError = validateUsername(formData.username);
    if (usernameError) {
      setError(usernameError);
      setLoading(false);
      return;
    }

    try {
      // Appel à l'API de réinitialisation de mot de passe
      await apiService.forgotPassword(formData.username);
      
      setSuccess(true);
      
      // Rediriger vers la page de réinitialisation après 2 secondes
      setTimeout(() => {
        navigate('/reset-password');
      }, 2000);
    } catch (err) {
      console.error('Erreur:', err);
      setError(err.message || 'Une erreur est survenue. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  // Afficher un spinner pendant la vérification de la session
  if (authLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Logo et titre */}
        <div className="text-center">
          <div className="mb-6">
            <h1 className="text-4xl font-cookie text-secondary mb-2" style={{ fontFamily: 'Kaushan Script, cursive' }}>
              uFaranga
            </h1>
            <div className="flex items-center justify-center gap-2 font-allan">
              <span className="text-sm text-text">Simply</span> 
              <span className="text-sm text-primary">Money</span>
            </div>
          </div>
          
          <h2 className="text-2xl font-heading font-bold text-text mb-2">
            Mot de passe oublié ?
          </h2>
          <p className="text-sm text-gray-400">
            Entrez votre adresse e-mail ou numéro de téléphone pour réinitialiser votre mot de passe
          </p>
        </div>
        
        {/* Formulaire de réinitialisation */}
        <div className="bg-card border border-darkGray rounded-lg p-8 shadow-lg">
          {success ? (
            <div className="space-y-6">
              <Alert variant="success">
                Un code de vérification a été envoyé à votre adresse e-mail ou par SMS. Vous allez être redirigé...
              </Alert>
              
              <div className="text-center space-y-2">
                <Link 
                  to="/reset-password" 
                  className="block text-primary hover:text-secondary transition-colors font-medium"
                >
                  Entrer le code maintenant
                </Link>
                <Link 
                  to="/login" 
                  className="block text-sm text-gray-400 hover:text-primary transition-colors"
                >
                  Retour à la connexion
                </Link>
              </div>
            </div>
          ) : (
            <form className="space-y-6" onSubmit={handleSubmit}>
              {error && (
                <Alert variant="danger">
                  {error}
                </Alert>
              )}
              
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-text mb-2">
                  Adresse e-mail ou numéro de téléphone
                </label>
                <Input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="admin@ufaranga.bi ou +25779111111"
                  className="w-full !bg-transparent border-gray-400 text-text placeholder-gray-400 focus:border-primary focus:ring-primary"
                  size="large"
                  fullWidth
                />
              </div>

              <div>
                <Button
                  type="submit"
                  variant="primary"
                  size="large"
                  className="w-full bg-primary hover:bg-blue-700 text-white font-medium rounded-lg transition-all duration-200 focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-card disabled:opacity-50"
                  disabled={loading}
                  loading={loading}
                  fullWidth
                >
                  Réinitialiser le mot de passe
                </Button>
              </div>

              <div className="text-center">
                <Link 
                  to="/login" 
                  className="text-sm text-gray-400 hover:text-primary transition-colors"
                >
                  Retour à la connexion
                </Link>
              </div>
            </form>
          )}
        </div>
        
        {/* Footer */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            © 2024 uFaranga Platform. Tous droits réservés.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
