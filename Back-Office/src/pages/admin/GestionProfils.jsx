import { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Tag } from 'primereact/tag';
import { Dialog } from 'primereact/dialog';
import CreateUserDialog from '../../components/CreateUserDialog';
import { 
  Search, Plus, Download, Shield, Users, UserCog, Lock, MoreVertical,
  Eye, History, FileText, Activity, UserCheck, Clock, Settings, Copy, Edit, Trash2
} from 'lucide-react';

function GestionProfils() {
  const [globalFilter, setGlobalFilter] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [selectedProfil, setSelectedProfil] = useState(null);
  const [showDialog, setShowDialog] = useState(false);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [openMenuId, setOpenMenuId] = useState(null);
  const [menuPosition, setMenuPosition] = useState({ top: 0, right: 20 });
  
  const menuRef = useRef(null);
  const buttonRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target) && 
          buttonRef.current && !buttonRef.current.contains(event.target)) {
        setOpenMenuId(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const profils = [
    { 
      id: 'PR001', 
      nom: 'Super Administrateur', 
      code: 'SUPER_ADMIN', 
      type: 'systeme',
      utilisateurs: 2, 
      permissions: ['all'],
      description: 'Accès complet au système',
      status: 'actif', 
      dateCreation: '2023-01-01',
      modifiable: false
    },
    { 
      id: 'PR002', 
      nom: 'Administrateur', 
      code: 'ADMIN', 
      type: 'systeme',
      utilisateurs: 5, 
      permissions: ['gestion_users', 'gestion_agents', 'reporting', 'transactions', 'parametres'],
      description: 'Gestion complète de la plateforme',
      status: 'actif', 
      dateCreation: '2023-01-01',
      modifiable: false
    },
    { 
      id: 'PR003', 
      nom: 'Agent Principal', 
      code: 'AGENT_PRINCIPAL', 
      type: 'operationnel',
      utilisateurs: 12, 
      permissions: ['transactions', 'float', 'commissions', 'rapports'],
      description: 'Agent avec accès complet aux opérations',
      status: 'actif', 
      dateCreation: '2023-02-15',
      modifiable: true
    },
    { 
      id: 'PR004', 
      nom: 'Agent Standard', 
      code: 'AGENT', 
      type: 'operationnel',
      utilisateurs: 45, 
      permissions: ['transactions', 'float', 'commissions'],
      description: 'Agent avec accès standard',
      status: 'actif', 
      dateCreation: '2023-02-15',
      modifiable: true
    },
    { 
      id: 'PR005', 
      nom: 'Client Premium', 
      code: 'CLIENT_PREMIUM', 
      type: 'client',
      utilisateurs: 234, 
      permissions: ['transactions', 'historique', 'profil'],
      description: 'Client avec plafonds élevés',
      status: 'actif', 
      dateCreation: '2023-03-01',
      modifiable: true
    },
    { 
      id: 'PR006', 
      nom: 'Client Standard', 
      code: 'CLIENT', 
      type: 'client',
      utilisateurs: 1567, 
      permissions: ['transactions', 'historique', 'profil'],
      description: 'Client avec plafonds standards',
      status: 'actif', 
      dateCreation: '2023-03-01',
      modifiable: true
    },
    { 
      id: 'PR007', 
      nom: 'Technicien', 
      code: 'TECH', 
      type: 'technique',
      utilisateurs: 3, 
      permissions: ['monitoring', 'logs', 'api', 'maintenance'],
      description: 'Support technique et maintenance',
      status: 'actif', 
      dateCreation: '2023-04-10',
      modifiable: true
    },
    { 
      id: 'PR008', 
      nom: 'Superviseur', 
      code: 'SUPERVISEUR', 
      type: 'operationnel',
      utilisateurs: 8, 
      permissions: ['gestion_agents', 'reporting', 'validation', 'fraude'],
      description: 'Supervision des agents et opérations',
      status: 'actif', 
      dateCreation: '2024-01-15',
      modifiable: true
    },
  ];

  const typeOptions = [
    { label: 'Tous', value: 'all' },
    { label: 'Système', value: 'systeme' },
    { label: 'Opérationnel', value: 'operationnel' },
    { label: 'Client', value: 'client' },
    { label: 'Technique', value: 'technique' }
  ];

  const filteredProfils = profils.filter(profil => {
    const matchesType = selectedType === 'all' || profil.type === selectedType;
    const matchesSearch = !globalFilter || 
      profil.nom.toLowerCase().includes(globalFilter.toLowerCase()) ||
      profil.code.toLowerCase().includes(globalFilter.toLowerCase()) ||
      profil.description.toLowerCase().includes(globalFilter.toLowerCase());
    return matchesType && matchesSearch;
  });

  const stats = {
    total: profils.length,
    systeme: profils.filter(p => p.type === 'systeme').length,
    operationnel: profils.filter(p => p.type === 'operationnel').length,
    totalUtilisateurs: profils.reduce((sum, p) => sum + p.utilisateurs, 0)
  };

  const codeBodyTemplate = (rowData) => {
    return <Tag value={rowData.code} severity="info" />;
  };

  const typeBodyTemplate = (rowData) => {
    const config = {
      systeme: { label: 'Système', severity: 'danger' },
      operationnel: { label: 'Opérationnel', severity: 'success' },
      client: { label: 'Client', severity: 'info' },
      technique: { label: 'Technique', severity: 'warning' }
    };
    const { label, severity } = config[rowData.type];
    return <Tag value={label} severity={severity} />;
  };

  const statusBodyTemplate = (rowData) => {
    return <Tag value={rowData.status} severity={rowData.status === 'actif' ? 'success' : 'danger'} />;
  };

  const permissionsBodyTemplate = (rowData) => {
    const count = rowData.permissions.length;
    return (
      <div className="flex gap-1 flex-wrap">
        {rowData.permissions[0] === 'all' ? (
          <Tag value="Toutes" severity="danger" />
        ) : (
          <Tag value={`${count} permissions`} severity="info" />
        )}
      </div>
    );
  };

  const utilisateursBodyTemplate = (rowData) => {
    return <Tag value={rowData.utilisateurs} severity="secondary" />;
  };

  const actionsBodyTemplate = (rowData) => {
    const isOpen = openMenuId === rowData.id;

    const handleMenuAction = (action) => {
      setOpenMenuId(null);
      action();
    };

    const calculateMenuPosition = (buttonElement) => {
      const buttonRect = buttonElement.getBoundingClientRect();
      const menuHeight = 500; // Hauteur approximative du menu
      const menuWidth = 280;
      const windowHeight = window.innerHeight;
      const windowWidth = window.innerWidth;

      let top = buttonRect.bottom + 5;
      let left = buttonRect.right - menuWidth;

      // Si le menu dépasse en bas, le positionner au-dessus du bouton
      if (top + menuHeight > windowHeight) {
        top = buttonRect.top - menuHeight - 5;
      }

      // Si le menu dépasse encore en haut, le positionner au milieu de l'écran
      if (top < 0) {
        top = Math.max(10, (windowHeight - menuHeight) / 2);
      }

      // Si le menu dépasse à gauche, l'aligner à gauche du bouton
      if (left < 10) {
        left = buttonRect.left;
      }

      // Si le menu dépasse à droite, l'aligner à droite de l'écran
      if (left + menuWidth > windowWidth - 10) {
        left = windowWidth - menuWidth - 10;
      }

      return { top, left };
    };

    const MenuContent = () => (
      <div 
        ref={menuRef}
        className="bg-card border border-darkGray rounded-xl shadow-2xl py-2 min-w-[280px] max-h-[500px] overflow-y-auto"
        style={{ 
          animation: 'fadeIn 0.15s ease-out',
          zIndex: 99999,
          position: 'fixed',
          top: `${menuPosition.top}px`,
          left: `${menuPosition.left}px`
        }}
      >
        <button
          onClick={() => handleMenuAction(() => {
            setSelectedProfil(rowData);
            setShowDialog(true);
          })}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Eye className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Consulter</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Historique', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <History className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Historique</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Logs', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <FileText className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Logs d'activité</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Activités', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Activity className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Activités en cours</span>
        </button>

        <div className="border-t border-darkGray my-2"></div>

        <button
          onClick={() => handleMenuAction(() => console.log('Utilisateurs', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <UserCheck className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Utilisateurs associés</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Sessions', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Clock className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Sessions actives</span>
        </button>

        <div className="border-t border-darkGray my-2"></div>
        <div className="px-3 py-2">
          <span className="text-xs font-semibold text-gray-500 uppercase">Contrôle Bancaire</span>
        </div>

        <button
          onClick={() => handleMenuAction(() => console.log('Vérifier identité', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Shield className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Vérifier l'identité</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Comptes bancaires', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Users className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Comptes bancaires</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Historique transactions', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Activity className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Historique des transactions</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Limites et plafonds', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Settings className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Limites et plafonds</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Documents KYC', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <FileText className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Documents KYC</span>
        </button>

        <button
          onClick={() => handleMenuAction(() => console.log('Alertes fraude', rowData.id))}
          className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
        >
          <Lock className="w-4 h-4 text-gray-400" />
          <span className="text-sm">Alertes de fraude</span>
        </button>

        {rowData.modifiable ? (
          <>
            <div className="border-t border-darkGray my-2"></div>

            <button
              onClick={() => handleMenuAction(() => console.log('Modifier droits', rowData.id))}
              className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
            >
              <Settings className="w-4 h-4 text-gray-400" />
              <span className="text-sm">Modifier les droits</span>
            </button>

            <button
              onClick={() => handleMenuAction(() => console.log('Dupliquer', rowData.id))}
              className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
            >
              <Copy className="w-4 h-4 text-gray-400" />
              <span className="text-sm">Dupliquer le profil</span>
            </button>

            <button
              onClick={() => handleMenuAction(() => console.log('Modifier', rowData.id))}
              className="w-full flex items-center gap-3 px-4 py-3 text-text hover:bg-darkGray transition-colors text-left"
            >
              <Edit className="w-4 h-4 text-gray-400" />
              <span className="text-sm">Modifier</span>
            </button>

            <div className="border-t border-darkGray my-2"></div>

            <button
              onClick={() => handleMenuAction(() => console.log('Bloquer le compte', rowData.id))}
              className="w-full flex items-center gap-3 px-4 py-3 text-danger hover:bg-danger/10 transition-colors text-left"
            >
              <Lock className="w-4 h-4" />
              <span className="text-sm">Bloquer le compte</span>
            </button>

            <button
              onClick={() => handleMenuAction(() => console.log('Supprimer', rowData.id))}
              className="w-full flex items-center gap-3 px-4 py-3 text-danger hover:bg-danger/10 transition-colors text-left"
            >
              <Trash2 className="w-4 h-4" />
              <span className="text-sm">Supprimer</span>
            </button>
          </>
        ) : (
          <>
            <div className="border-t border-darkGray my-2"></div>
            <div className="flex items-center gap-3 px-4 py-3 text-gray-500 opacity-50 cursor-not-allowed">
              <Lock className="w-4 h-4" />
              <span className="text-sm">Profil système</span>
            </div>
          </>
        )}
      </div>
    );

    return (
      <div className="flex justify-center">
        <button
          ref={buttonRef}
          onClick={(e) => {
            e.stopPropagation();
            if (!isOpen) {
              const position = calculateMenuPosition(e.currentTarget);
              setMenuPosition(position);
              setOpenMenuId(rowData.id);
            } else {
              setOpenMenuId(null);
            }
          }}
          className="p-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors"
          title="Actions"
        >
          <MoreVertical className="w-4 h-4" />
        </button>

        {isOpen && createPortal(<MenuContent />, document.body)}
      </div>
    );
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-anton uppercase text-text">Gestion des Profils</h1>
          <p className="text-sm text-gray-400 mt-1">Gérer les rôles et permissions du système</p>
        </div>
        <button 
          onClick={() => setShowCreateDialog(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-5 h-5" />
          <span>Nouveau Profil</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20 rounded-xl p-5 hover:shadow-lg transition-all">
          <div className="flex items-center justify-between mb-3">
            <div className="p-3 bg-primary/20 rounded-lg">
              <Shield className="w-6 h-6 text-primary" />
            </div>
            <span className="text-3xl font-bold text-primary">{stats.total}</span>
          </div>
          <p className="text-sm text-gray-400">Total Profils</p>
        </div>

        <div className="bg-gradient-to-br from-danger/10 to-danger/5 border border-danger/20 rounded-xl p-5 hover:shadow-lg transition-all">
          <div className="flex items-center justify-between mb-3">
            <div className="p-3 bg-danger/20 rounded-lg">
              <Lock className="w-6 h-6 text-danger" />
            </div>
            <span className="text-3xl font-bold text-danger">{stats.systeme}</span>
          </div>
          <p className="text-sm text-gray-400">Profils Système</p>
        </div>

        <div className="bg-gradient-to-br from-secondary/10 to-secondary/5 border border-secondary/20 rounded-xl p-5 hover:shadow-lg transition-all">
          <div className="flex items-center justify-between mb-3">
            <div className="p-3 bg-secondary/20 rounded-lg">
              <UserCog className="w-6 h-6 text-secondary" />
            </div>
            <span className="text-3xl font-bold text-secondary">{stats.operationnel}</span>
          </div>
          <p className="text-sm text-gray-400">Opérationnels</p>
        </div>

        <div className="bg-gradient-to-br from-primary/10 to-primary/5 border border-primary/20 rounded-xl p-5 hover:shadow-lg transition-all">
          <div className="flex items-center justify-between mb-3">
            <div className="p-3 bg-primary/20 rounded-lg">
              <Users className="w-6 h-6 text-primary" />
            </div>
            <span className="text-3xl font-bold text-primary">{stats.totalUtilisateurs}</span>
          </div>
          <p className="text-sm text-gray-400">Utilisateurs</p>
        </div>
      </div>

      <div className="bg-card border border-darkGray rounded-lg p-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <InputText
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              placeholder="Rechercher par nom, code, description..."
              className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text"
            />
          </div>
          
          <Dropdown
            value={selectedType}
            options={typeOptions}
            onChange={(e) => setSelectedType(e.value)}
            className="w-full md:w-48"
          />

          <button className="flex items-center gap-2 px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary/90 transition-colors">
            <Download className="w-5 h-5" />
            <span>Exporter</span>
          </button>
        </div>
      </div>

      <div className="bg-card border border-darkGray rounded-lg overflow-hidden">
        <DataTable
          value={filteredProfils}
          paginator
          rows={10}
          rowsPerPageOptions={[5, 10, 25, 50]}
          className="custom-datatable"
          emptyMessage="Aucun profil trouvé"
          scrollable
          scrollHeight="600px"
        >
          <Column 
            field="code" 
            header="Code" 
            body={codeBodyTemplate}
            sortable 
            frozen
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="nom" 
            header="Nom du Profil" 
            sortable 
            frozen
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="type" 
            header="Type" 
            body={typeBodyTemplate} 
            sortable 
            frozen
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="utilisateurs" 
            header="Utilisateurs" 
            body={utilisateursBodyTemplate}
            sortable 
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="permissions" 
            header="Permissions" 
            body={permissionsBodyTemplate} 
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="status" 
            header="Statut" 
            body={statusBodyTemplate} 
            sortable 
            frozen
            alignFrozen="right"
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            field="dateCreation" 
            header="Date Création" 
            sortable 
            frozen
            alignFrozen="right"
            style={{ whiteSpace: 'nowrap' }}
          />
          <Column 
            header="Actions" 
            body={actionsBodyTemplate} 
            frozen
            alignFrozen="right"
            style={{ whiteSpace: 'nowrap' }}
          />
        </DataTable>
      </div>

      <Dialog
        visible={showDialog}
        onHide={() => setShowDialog(false)}
        header="Détails du Profil"
        style={{ width: '700px' }}
        className="custom-dialog"
      >
        {selectedProfil && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-400">Code</p>
                <p className="font-semibold text-text">{selectedProfil.code}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Nom</p>
                <p className="font-semibold text-text">{selectedProfil.nom}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Type</p>
                {typeBodyTemplate(selectedProfil)}
              </div>
              <div>
                <p className="text-sm text-gray-400">Statut</p>
                {statusBodyTemplate(selectedProfil)}
              </div>
              <div>
                <p className="text-sm text-gray-400">Utilisateurs</p>
                <p className="font-semibold text-primary">{selectedProfil.utilisateurs}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Date création</p>
                <p className="font-semibold text-text">{selectedProfil.dateCreation}</p>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-gray-400">Description</p>
                <p className="font-semibold text-text">{selectedProfil.description}</p>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-gray-400 mb-2">Permissions</p>
                <div className="flex flex-wrap gap-2">
                  {selectedProfil.permissions[0] === 'all' ? (
                    <Tag value="Toutes les permissions" severity="danger" />
                  ) : (
                    selectedProfil.permissions.map((perm, index) => (
                      <Tag key={index} value={perm.replace(/_/g, ' ')} severity="info" />
                    ))
                  )}
                </div>
              </div>
              <div className="col-span-2">
                <p className="text-sm text-gray-400">Modifiable</p>
                <Tag 
                  value={selectedProfil.modifiable ? 'Oui' : 'Non (Profil système)'} 
                  severity={selectedProfil.modifiable ? 'success' : 'danger'} 
                />
              </div>
            </div>
          </div>
        )}
      </Dialog>

      {/* Dialog Création Utilisateur */}
      <CreateUserDialog
        visible={showCreateDialog}
        onHide={() => setShowCreateDialog(false)}
      />
    </div>
  );
}

export default GestionProfils;
