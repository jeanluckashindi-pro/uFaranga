import React, { useState } from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import { Button, FacebookButton } from './components/common';
import ThemeToggle from './components/common/ThemeToggle';

function AppContent() {
  const [loadingStates, setLoadingStates] = useState({
    standard: false,
    facebook: false,
    variant: false
  });

  const handleTestSpinner = (type) => {
    setLoadingStates(prev => ({ ...prev, [type]: true }));
    
    // Arrêter le spinner après 3 secondes
    setTimeout(() => {
      setLoadingStates(prev => ({ ...prev, [type]: false }));
    }, 3000);
  };

  return (
    <div className="min-h-screen transition-colors duration-300">
      <div className="p-8">
        {/* Header avec toggle de thème */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-blue-600 font-roboto">uFaranga - Front Office</h1>
          <ThemeToggle />
        </div>
        
        <div className="mt-4 p-4 bg-card border border-default rounded mb-8">
          <p className="text-muted">Interface avec thème dark/light. Cliquez sur l'icône pour basculer !</p>
        </div>

        {/* Test des Boutons avec Spinners */}
        <div className="bg-card border border-default p-6 rounded-lg shadow-md mb-8">
          <h2 className="text-xl font-semibold mb-4">Test des Boutons avec Spinners</h2>
          
          <div className="flex flex-wrap gap-4 mb-6">
            <Button 
              variant="primary"
              loading={loadingStates.standard}
              onClick={() => handleTestSpinner('standard')}
              disabled={loadingStates.standard}
            >
              {loadingStates.standard ? 'Chargement...' : 'Test Spinner Standard'}
            </Button>
            
            <Button 
              variant="facebook"
              loading={loadingStates.variant}
              onClick={() => handleTestSpinner('variant')}
              disabled={loadingStates.variant}
            >
              {loadingStates.variant ? 'Chargement...' : 'Bouton Facebook Variant'}
            </Button>
          </div>
        </div>

        {/* Test du Bouton Facebook */}
        <div className="bg-card border border-default p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Bouton Facebook Style Exact</h2>
          
          <div className="flex flex-wrap gap-4 mb-6">
            <FacebookButton 
              size="small"
              loading={loadingStates.facebook}
              onClick={() => handleTestSpinner('facebook')}
              disabled={loadingStates.facebook}
            >
              {loadingStates.facebook ? 'Connexion...' : 'Se connecter avec Facebook'}
            </FacebookButton>
            
            <FacebookButton 
              size="medium"
              fullWidth={false}
            >
              Continuer avec Facebook
            </FacebookButton>
            
            <FacebookButton 
              size="large"
              fullWidth={false}
            >
              Créer un compte Facebook
            </FacebookButton>
          </div>

          <div className="text-sm text-muted">
            <p>• Thème dark par défaut (bg: noir, text: blanc)</p>
            <p>• Basculement vers thème light disponible</p>
            <p>• Couleurs Facebook : #1877f2</p>
            <p>• Spinner radial amélioré</p>
            <p>• Police par défaut : Roboto</p>
          </div>
        </div>

        {/* Démonstration des Polices */}
        <div className="bg-card border border-default p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4 font-roboto">Polices Disponibles</h2>
          
          <div className="space-y-4">
            <div className="p-4 border border-default rounded">
              <h3 className="text-lg font-roboto font-medium mb-2">Roboto (Par défaut)</h3>
              <p className="font-roboto text-base">Cette police moderne et lisible est utilisée par défaut dans toute l'application.</p>
              <p className="font-roboto font-bold text-sm mt-1">Classes : font-roboto, font-sans</p>
            </div>
            
            <div className="p-4 border border-default rounded">
              <h3 className="text-2xl font-anton mb-2">ANTON</h3>
              <p className="font-roboto text-sm text-muted">Police condensée et impactante, parfaite pour les titres.</p>
              <p className="font-roboto font-bold text-sm mt-1">Classe : font-anton</p>
            </div>
            
            <div className="p-4 border border-default rounded">
              <h3 className="text-2xl font-bangers mb-2">BANGERS</h3>
              <p className="font-roboto text-sm text-muted">Police de style comic/cartoon, idéale pour les éléments ludiques.</p>
              <p className="font-roboto font-bold text-sm mt-1">Classe : font-bangers</p>
            </div>
            
            <div className="p-4 border border-default rounded">
              <h3 className="text-2xl font-cookie mb-2">Cookie</h3>
              <p className="font-roboto text-sm text-muted">Police script élégante, parfaite pour les signatures ou éléments décoratifs.</p>
              <p className="font-roboto font-bold text-sm mt-1">Classe : font-cookie</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
