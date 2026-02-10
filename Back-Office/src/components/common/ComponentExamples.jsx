import React, { useState } from 'react';
import { 
  Spinner, 
  DotSpinner, 
  BarSpinner,
  Button, 
  ButtonGroup, 
  IconButton,
  Card, 
  StatsCard,
  Modal,
  ConfirmModal,
  Input,
  Alert
} from './index';

// Exemples d'utilisation des composants communs
const ComponentExamples = () => {
  const [showModal, setShowModal] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [showAlert, setShowAlert] = useState(true);

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Composants Communs - Exemples</h1>

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
                <Button loading>Loading</Button>
                <Button disabled>Disabled</Button>
                <Button fullWidth>Full Width</Button>
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
            title="Carte Simple" 
            subtitle="Description de la carte"
            footer={<Button size="small">Action</Button>}
          >
            <p>Contenu de la carte avec du texte d'exemple.</p>
          </Card>

          <StatsCard
            title="Utilisateurs Actifs"
            value="1,234"
            change="+12% ce mois"
            changeType="positive"
            icon={
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
            }
          />

          <Card variant="primary" hover>
            <h3 className="font-semibold mb-2">Carte Interactive</h3>
            <p>Cette carte a un effet hover et une variante colorée.</p>
          </Card>
        </div>
      </section>

      {/* Inputs */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Champs de saisie</h2>
        <Card>
          <div className="space-y-4">
            <Input
              label="Nom d'utilisateur"
              placeholder="Entrez votre nom"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              required
            />
            
            <Input
              label="Email"
              type="email"
              placeholder="exemple@email.com"
              error="Format d'email invalide"
            />
            
            <Input
              label="Mot de passe"
              type="password"
              disabled
              placeholder="Champ désactivé"
            />
          </div>
        </Card>
      </section>

      {/* Alerts */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Alertes</h2>
        <div className="space-y-4">
          {showAlert && (
            <Alert 
              variant="success" 
              dismissible 
              onDismiss={() => setShowAlert(false)}
            >
              <strong>Succès!</strong> Votre action a été effectuée avec succès.
            </Alert>
          )}
          
          <Alert variant="warning">
            <strong>Attention!</strong> Cette action nécessite une confirmation.
          </Alert>
          
          <Alert variant="danger">
            <strong>Erreur!</strong> Une erreur s'est produite lors du traitement.
          </Alert>
          
          <Alert variant="info" icon={false}>
            Information sans icône pour un style plus minimaliste.
          </Alert>
        </div>
      </section>

      {/* Modals */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Modales</h2>
        <div className="space-x-4">
          <Button onClick={() => setShowModal(true)}>
            Ouvrir Modal
          </Button>
          <Button 
            variant="danger" 
            onClick={() => setShowConfirm(true)}
          >
            Confirmation
          </Button>
        </div>

        <Modal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          title="Exemple de Modal"
          footer={
            <div className="flex justify-end space-x-3">
              <Button variant="outline" onClick={() => setShowModal(false)}>
                Annuler
              </Button>
              <Button onClick={() => setShowModal(false)}>
                Confirmer
              </Button>
            </div>
          }
        >
          <p>Ceci est le contenu de la modal. Vous pouvez y placer n'importe quel contenu.</p>
        </Modal>

        <ConfirmModal
          isOpen={showConfirm}
          onClose={() => setShowConfirm(false)}
          onConfirm={() => {
            alert('Action confirmée!');
            setShowConfirm(false);
          }}
          title="Confirmer l'action"
          message="Êtes-vous sûr de vouloir effectuer cette action ? Cette opération ne peut pas être annulée."
          confirmText="Oui, continuer"
          cancelText="Annuler"
        />
      </section>
    </div>
  );
};

export default ComponentExamples;