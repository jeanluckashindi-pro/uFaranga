import React, { useState } from 'react';
import { 
  Spinner, 
  DotSpinner, 
  BarSpinner,
  Button, 
  ButtonGroup, 
  IconButton,
  Card, 
  StatsCard
} from './index';

// Exemples d'utilisation des composants communs
const ComponentExamples = () => {
  const [loading, setLoading] = useState(false);

  const handleLoadingDemo = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Composants Communs - Front Office</h1>

      {/* Spinners */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Spinners</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card title="Spinner Standard">
            <div className="flex justify-center space-x-4">
              <Spinner size="small" />
              <Spinner size="medium" />
              <Spinner size="large" />
            </div>
          </Card>
          
          <Card title="Dot Spinner">
            <div className="flex justify-center space-x-4">
              <DotSpinner color="primary" />
              <DotSpinner color="success" />
              <DotSpinner color="danger" />
            </div>
          </Card>
          
          <Card title="Bar Spinner">
            <div className="flex justify-center space-x-4">
              <BarSpinner color="primary" />
              <BarSpinner color="warning" />
              <BarSpinner color="success" />
            </div>
          </Card>
        </div>
      </section>

      {/* Buttons */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Boutons</h2>
        <div className="space-y-4">
          <Card title="Variantes de boutons">
            <div className="flex flex-wrap gap-3">
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="success">Success</Button>
              <Button variant="warning">Warning</Button>
              <Button variant="danger">Danger</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="link">Link</Button>
            </div>
          </Card>

          <Card title="Tailles et états">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Button size="small">Small</Button>
                <Button size="medium">Medium</Button>
                <Button size="large">Large</Button>
                <Button size="xlarge">XLarge</Button>
              </div>
              <div className="flex items-center gap-3">
                <Button loading={loading} onClick={handleLoadingDemo}>
                  {loading ? 'Chargement...' : 'Test Loading'}
                </Button>
                <Button disabled>Disabled</Button>
              </div>
            </div>
          </Card>

          <Card title="Groupe de boutons">
            <ButtonGroup>
              <Button variant="outline">Gauche</Button>
              <Button variant="outline">Centre</Button>
              <Button variant="outline">Droite</Button>
            </ButtonGroup>
          </Card>
        </div>
      </section>

      {/* Cards */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Cartes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card 
            title="Transactions" 
            subtitle="Aperçu des transactions récentes"
            footer={<Button size="small">Voir tout</Button>}
          >
            <p className="text-gray-600">Vous avez effectué 12 transactions ce mois-ci.</p>
          </Card>

          <StatsCard
            title="Solde Total"
            value="2,450 €"
            change="+5.2% ce mois"
            changeType="positive"
            icon={
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
              </svg>
            }
          />

          <Card variant="success" hover>
            <h3 className="font-semibold mb-2">Compte Vérifié</h3>
            <p className="text-sm text-gray-600">Votre compte est entièrement vérifié et actif.</p>
          </Card>
        </div>
      </section>

      {/* Interactive Demo */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Démonstration Interactive</h2>
        <Card>
          <div className="text-center space-y-4">
            <h3 className="text-lg font-semibold">Test des Composants</h3>
            <p className="text-gray-600">Cliquez sur les boutons pour tester les différents états</p>
            
            <div className="flex justify-center space-x-4">
              <Button 
                variant="primary" 
                loading={loading}
                onClick={handleLoadingDemo}
              >
                {loading ? 'Chargement...' : 'Démarrer Test'}
              </Button>
              
              <IconButton
                icon={
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                }
                variant="danger"
              />
            </div>
            
            {loading && (
              <div className="mt-4">
                <Spinner text="Traitement en cours..." />
              </div>
            )}
          </div>
        </Card>
      </section>
    </div>
  );
};

export default ComponentExamples;