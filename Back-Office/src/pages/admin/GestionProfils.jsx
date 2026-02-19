import { useState } from 'react';
import {
  Users, Plus, Edit2, Trash2, Search, Filter, Eye, EyeOff,
  Lock, Unlock, Shield, Clock, Key, CheckCircle, XCircle,
  MoreVertical, Calendar, Activity, AlertTriangle
} from 'lucide-react';
import { Card } from '../../components/common';

const GestionProfils = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  // État pour les profils utilisateurs
  const [profiles, setProfiles] = useState([
    {
      id: 1,
      username: 'admin.system',
      email: 'admin@ufaranga.com',
      fullName: 'Administrateur Système',
      role: 'super_admin',
      status: 'active',
      lastLogin: '2024-02-19 10:30',
      createdAt: '2024-01-01',
      permissions: ['all'],
      twoFactorEnabled: true,
    },
    {
      id: 2,
      username: 'tech.admin',
      email: 'tech@ufaranga.com',
      fullName: 'Admin Technique',
      role: 'admin_tech',
      status: 'active',
      lastLogin: '2024-02-19 09:15',
      createdAt: '2024-01-15',
      permissions: ['monitoring', 'api', 'logs'],
      twoFactorEnabled: false,
    },
    {
      id: 3,
      username: 'agent.001',
      email: 'agent001@ufaranga.com',
      fullName: 'Agent Commercial',
      role: 'agent',
      status: 'inactive',
      lastLogin: '2024-02-10 14:20',
      createdAt: '2024-02-01',
      permissions: ['transactions', 'clients'],
      twoFactorEnabled: false,
    },
  ]);

  const roles = [
    { value: 'super_admin', label: 'Super Administrateur', color: 'red' },
    { value: 'admin_system', label: 'Admin Système', color: 'orange' },
    { value: 'admin_tech', label: 'Admin Technique', color: 'blue' },
    { value: 'agent', label: 'Agent', color: 'green' },
    { value: 'client', label: 'Client', color: 'gray' },
  ];

  const permissions = [
    { id: 'all', label: 'Tous les droits', category: 'system' },
    { id: 'users', label: 'Gestion utilisateurs', category: 'admin' },
    { id: 'transactions', label: 'Transactions', category: 'operations' },
    { id: 'float', label: 'Gestion Float', category: 'operations' },
    { id: 'commissions', label: 'Commissions', category: 'finance' },
    { id: 'reporting', label: 'Rapports', category: 'analytics' },
    { id: 'monitoring', label: 'Monitoring', category: 'tech' },
    { id: 'api', label: 'API Management', category: 'tech' },
    { id: 'logs', label: 'Logs système', category: 'tech' },
  ];

  const filteredProfiles = profiles.filter(profile => {
    const matchSearch = profile.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                       profile.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                       profile.fullName.toLowerCase().includes(searchTerm.toLowerCase());
    const matchRole = filterRole === 'all' || profile.role === filterRole;
    const matchStatus = filterStatus === 'all' || profile.status === filterStatus;
    return matchSearch && matchRole && matchStatus;
  });

  const getRoleColor = (role) => {
    const roleObj = roles.find(r => r.value === role);
    return roleObj?.color || 'gray';
  };

  const toggleStatus = (profileId) => {
    setProfiles(profiles.map(p =>
      p.id === profileId ? { ...p, status: p.status === 'active' ? 'inactive' : 'active' } : p
    ));
  };

  return (
    <div className="space-y-6">
      <Card className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-heading font-bold text-text mb-1">Gestion des Profils</h2>
            <p className="text-sm text-gray-400 font-sans">
              Gérez les utilisateurs, rôles, permissions et sécurité
            </p>
          </div>
          <button
            onClick={() => {
              setSelectedProfile(null);
              setShowModal(true);
            }}
            className="px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 font-sans"
          >
            <Plus className="w-4 h-4" />
            Nouveau Profil
          </button>
        </div>

        {/* Filtres et recherche */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Rechercher par nom, email, username..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
              />
            </div>
          </div>
          <select
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
            className="px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
          >
            <option value="all">Tous les rôles</option>
            {roles.map(role => (
              <option key={role.value} value={role.value}>{role.label}</option>
            ))}
          </select>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
          >
            <option value="all">Tous les statuts</option>
            <option value="active">Actifs</option>
            <option value="inactive">Inactifs</option>
          </select>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="p-4 bg-background rounded-lg border border-darkGray">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-sans">Total Profils</p>
                <p className="text-2xl font-bold text-text font-heading">{profiles.length}</p>
              </div>
              <Users className="w-8 h-8 text-primary" />
            </div>
          </div>
          <div className="p-4 bg-background rounded-lg border border-darkGray">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-sans">Actifs</p>
                <p className="text-2xl font-bold text-green-400 font-heading">
                  {profiles.filter(p => p.status === 'active').length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-400" />
            </div>
          </div>
          <div className="p-4 bg-background rounded-lg border border-darkGray">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-sans">Inactifs</p>
                <p className="text-2xl font-bold text-red-400 font-heading">
                  {profiles.filter(p => p.status === 'inactive').length}
                </p>
              </div>
              <XCircle className="w-8 h-8 text-red-400" />
            </div>
          </div>
          <div className="p-4 bg-background rounded-lg border border-darkGray">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-sans">2FA Activé</p>
                <p className="text-2xl font-bold text-blue-400 font-heading">
                  {profiles.filter(p => p.twoFactorEnabled).length}
                </p>
              </div>
              <Shield className="w-8 h-8 text-blue-400" />
            </div>
          </div>
        </div>

        {/* Table des profils */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-darkGray">
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400 font-sans">Utilisateur</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400 font-sans">Rôle</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400 font-sans">Statut</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400 font-sans">Dernière connexion</th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400 font-sans">Sécurité</th>
                <th className="text-right py-3 px-4 text-sm font-medium text-gray-400 font-sans">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredProfiles.map((profile) => (
                <tr key={profile.id} className="border-b border-darkGray hover:bg-background transition-colors">
                  <td className="py-4 px-4">
                    <div>
                      <p className="text-sm font-medium text-text font-sans">{profile.fullName}</p>
                      <p className="text-xs text-gray-400 font-mono">{profile.username}</p>
                      <p className="text-xs text-gray-500">{profile.email}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium font-sans bg-${getRoleColor(profile.role)}-400/20 text-${getRoleColor(profile.role)}-400`}>
                      {roles.find(r => r.value === profile.role)?.label}
                    </span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      {profile.status === 'active' ? (
                        <CheckCircle className="w-4 h-4 text-green-400" />
                      ) : (
                        <XCircle className="w-4 h-4 text-red-400" />
                      )}
                      <span className={`text-sm font-sans ${profile.status === 'active' ? 'text-green-400' : 'text-red-400'}`}>
                        {profile.status === 'active' ? 'Actif' : 'Inactif'}
                      </span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2 text-sm text-gray-400 font-mono">
                      <Clock className="w-4 h-4" />
                      {profile.lastLogin}
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      {profile.twoFactorEnabled ? (
                        <Shield className="w-4 h-4 text-green-400" title="2FA activé" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-orange-400" title="2FA désactivé" />
                      )}
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => {
                          setSelectedProfile(profile);
                          setShowHistoryModal(true);
                        }}
                        className="p-2 hover:bg-darkGray rounded transition-colors"
                        title="Historique"
                      >
                        <Activity className="w-4 h-4 text-gray-400" />
                      </button>
                      <button
                        onClick={() => {
                          setSelectedProfile(profile);
                          setShowPasswordModal(true);
                        }}
                        className="p-2 hover:bg-darkGray rounded transition-colors"
                        title="Réinitialiser mot de passe"
                      >
                        <Key className="w-4 h-4 text-gray-400" />
                      </button>
                      <button
                        onClick={() => toggleStatus(profile.id)}
                        className="p-2 hover:bg-darkGray rounded transition-colors"
                        title={profile.status === 'active' ? 'Désactiver' : 'Activer'}
                      >
                        {profile.status === 'active' ? (
                          <Lock className="w-4 h-4 text-orange-400" />
                        ) : (
                          <Unlock className="w-4 h-4 text-green-400" />
                        )}
                      </button>
                      <button
                        onClick={() => {
                          setSelectedProfile(profile);
                          setShowModal(true);
                        }}
                        className="p-2 hover:bg-darkGray rounded transition-colors"
                        title="Modifier"
                      >
                        <Edit2 className="w-4 h-4 text-blue-400" />
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Supprimer le profil "${profile.fullName}" ?`)) {
                            setProfiles(profiles.filter(p => p.id !== profile.id));
                          }
                        }}
                        className="p-2 hover:bg-darkGray rounded transition-colors"
                        title="Supprimer"
                      >
                        <Trash2 className="w-4 h-4 text-red-400" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Modal Créer/Modifier Profil */}
      {showModal && (
        <ProfileModal
          profile={selectedProfile}
          roles={roles}
          permissions={permissions}
          onClose={() => setShowModal(false)}
          onSave={(profile) => {
            if (selectedProfile) {
              setProfiles(profiles.map(p => p.id === profile.id ? profile : p));
            } else {
              setProfiles([...profiles, { ...profile, id: Date.now() }]);
            }
            setShowModal(false);
          }}
        />
      )}

      {/* Modal Historique */}
      {showHistoryModal && selectedProfile && (
        <HistoryModal
          profile={selectedProfile}
          onClose={() => setShowHistoryModal(false)}
        />
      )}

      {/* Modal Réinitialiser Mot de Passe */}
      {showPasswordModal && selectedProfile && (
        <PasswordModal
          profile={selectedProfile}
          onClose={() => setShowPasswordModal(false)}
          onReset={() => {
            alert(`Mot de passe réinitialisé pour ${selectedProfile.username}`);
            setShowPasswordModal(false);
          }}
        />
      )}
    </div>
  );
};

export default GestionProfils;

// Modal pour créer/modifier un profil
const ProfileModal = ({ profile, roles, permissions, onClose, onSave }) => {
  const [formData, setFormData] = useState(profile || {
    username: '',
    email: '',
    fullName: '',
    role: 'agent',
    status: 'active',
    permissions: [],
    twoFactorEnabled: false,
  });

  const [selectedPermissions, setSelectedPermissions] = useState(
    profile?.permissions || []
  );

  const togglePermission = (permId) => {
    if (selectedPermissions.includes(permId)) {
      setSelectedPermissions(selectedPermissions.filter(p => p !== permId));
    } else {
      setSelectedPermissions([...selectedPermissions, permId]);
    }
  };

  const handleSubmit = () => {
    onSave({
      ...formData,
      permissions: selectedPermissions,
      createdAt: profile?.createdAt || new Date().toISOString().split('T')[0],
      lastLogin: profile?.lastLogin || '-',
    });
  };

  const permissionsByCategory = permissions.reduce((acc, perm) => {
    if (!acc[perm.category]) acc[perm.category] = [];
    acc[perm.category].push(perm);
    return acc;
  }, {});

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-darkGray rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-card border-b border-darkGray p-6 flex items-center justify-between">
          <h3 className="text-xl font-heading font-bold text-text">
            {profile ? 'Modifier le Profil' : 'Nouveau Profil'}
          </h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-darkGray rounded-lg transition-colors"
          >
            <XCircle className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Informations de base */}
          <div>
            <h4 className="text-lg font-bold text-text mb-4 font-heading">Informations de base</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">
                  Nom complet
                </label>
                <input
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
                  placeholder="Ex: Jean Dupont"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">
                  Nom d'utilisateur
                </label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-mono"
                  placeholder="Ex: jean.dupont"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
                  placeholder="jean.dupont@ufaranga.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">
                  Rôle
                </label>
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
                >
                  {roles.map(role => (
                    <option key={role.value} value={role.value}>{role.label}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Permissions */}
          <div>
            <h4 className="text-lg font-bold text-text mb-4 font-heading">Permissions</h4>
            <div className="space-y-4">
              {Object.entries(permissionsByCategory).map(([category, perms]) => (
                <div key={category} className="p-4 bg-background rounded-lg border border-darkGray">
                  <h5 className="text-sm font-bold text-text mb-3 uppercase font-sans">{category}</h5>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {perms.map(perm => (
                      <label
                        key={perm.id}
                        className="flex items-center gap-2 p-2 hover:bg-card rounded cursor-pointer transition-colors"
                      >
                        <input
                          type="checkbox"
                          checked={selectedPermissions.includes(perm.id)}
                          onChange={() => togglePermission(perm.id)}
                          className="w-4 h-4 rounded border-darkGray text-primary focus:ring-primary"
                        />
                        <span className="text-sm text-gray-300 font-sans">{perm.label}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Sécurité */}
          <div>
            <h4 className="text-lg font-bold text-text mb-4 font-heading">Sécurité</h4>
            <div className="space-y-3">
              <label className="flex items-center justify-between p-4 bg-background rounded-lg border border-darkGray cursor-pointer hover:border-primary transition-colors">
                <div className="flex items-center gap-3">
                  <Shield className="w-5 h-5 text-primary" />
                  <div>
                    <p className="text-sm font-medium text-text font-sans">Authentification à deux facteurs (2FA)</p>
                    <p className="text-xs text-gray-400 font-sans">Sécurité renforcée pour ce compte</p>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={formData.twoFactorEnabled}
                  onChange={(e) => setFormData({ ...formData, twoFactorEnabled: e.target.checked })}
                  className="w-5 h-5 rounded border-darkGray text-primary focus:ring-primary"
                />
              </label>

              <label className="flex items-center justify-between p-4 bg-background rounded-lg border border-darkGray cursor-pointer hover:border-primary transition-colors">
                <div className="flex items-center gap-3">
                  {formData.status === 'active' ? (
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-400" />
                  )}
                  <div>
                    <p className="text-sm font-medium text-text font-sans">Compte actif</p>
                    <p className="text-xs text-gray-400 font-sans">Autoriser l'accès à ce compte</p>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={formData.status === 'active'}
                  onChange={(e) => setFormData({ ...formData, status: e.target.checked ? 'active' : 'inactive' })}
                  className="w-5 h-5 rounded border-darkGray text-primary focus:ring-primary"
                />
              </label>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3 pt-4 border-t border-darkGray">
            <button
              onClick={handleSubmit}
              className="flex-1 px-4 py-3 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors font-sans font-medium"
            >
              {profile ? 'Enregistrer les modifications' : 'Créer le profil'}
            </button>
            <button
              onClick={onClose}
              className="flex-1 px-4 py-3 bg-darkGray hover:bg-gray-700 text-text rounded-lg transition-colors font-sans font-medium"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Modal Historique
const HistoryModal = ({ profile, onClose }) => {
  const historyData = [
    { id: 1, action: 'Connexion réussie', date: '2024-02-19 10:30', ip: '192.168.1.100', type: 'login' },
    { id: 2, action: 'Modification du profil', date: '2024-02-18 15:20', ip: '192.168.1.100', type: 'update' },
    { id: 3, action: 'Changement de mot de passe', date: '2024-02-15 09:10', ip: '192.168.1.100', type: 'security' },
    { id: 4, action: 'Connexion réussie', date: '2024-02-14 14:45', ip: '192.168.1.101', type: 'login' },
    { id: 5, action: 'Échec de connexion', date: '2024-02-14 14:40', ip: '192.168.1.101', type: 'failed_login' },
  ];

  const getActionIcon = (type) => {
    switch (type) {
      case 'login': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'failed_login': return <XCircle className="w-4 h-4 text-red-400" />;
      case 'update': return <Edit2 className="w-4 h-4 text-blue-400" />;
      case 'security': return <Shield className="w-4 h-4 text-orange-400" />;
      default: return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-darkGray rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-card border-b border-darkGray p-6 flex items-center justify-between">
          <div>
            <h3 className="text-xl font-heading font-bold text-text">Historique d'activité</h3>
            <p className="text-sm text-gray-400 font-sans mt-1">{profile.fullName} ({profile.username})</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-darkGray rounded-lg transition-colors"
          >
            <XCircle className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        <div className="p-6">
          <div className="space-y-3">
            {historyData.map((item) => (
              <div
                key={item.id}
                className="flex items-start gap-4 p-4 bg-background rounded-lg border border-darkGray hover:border-primary transition-colors"
              >
                <div className="mt-1">{getActionIcon(item.type)}</div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-text font-sans">{item.action}</p>
                  <div className="flex items-center gap-4 mt-1">
                    <span className="text-xs text-gray-400 font-mono flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {item.date}
                    </span>
                    <span className="text-xs text-gray-400 font-mono">IP: {item.ip}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Modal Réinitialiser Mot de Passe
const PasswordModal = ({ profile, onClose, onReset }) => {
  const [sendEmail, setSendEmail] = useState(true);
  const [generatePassword, setGeneratePassword] = useState(true);
  const [newPassword, setNewPassword] = useState('');

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-darkGray rounded-lg max-w-md w-full">
        <div className="bg-card border-b border-darkGray p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Key className="w-6 h-6 text-primary" />
            <h3 className="text-xl font-heading font-bold text-text">Réinitialiser le mot de passe</h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-darkGray rounded-lg transition-colors"
          >
            <XCircle className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          <div className="p-4 bg-orange-400/10 border border-orange-400/30 rounded-lg">
            <p className="text-sm text-orange-400 font-sans">
              Vous êtes sur le point de réinitialiser le mot de passe de <strong>{profile.fullName}</strong>
            </p>
          </div>

          <label className="flex items-center justify-between p-4 bg-background rounded-lg border border-darkGray cursor-pointer">
            <span className="text-sm text-text font-sans">Générer un mot de passe automatiquement</span>
            <input
              type="checkbox"
              checked={generatePassword}
              onChange={(e) => setGeneratePassword(e.target.checked)}
              className="w-4 h-4 rounded border-darkGray text-primary focus:ring-primary"
            />
          </label>

          {!generatePassword && (
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">
                Nouveau mot de passe
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-mono"
                placeholder="Entrez le nouveau mot de passe"
              />
            </div>
          )}

          <label className="flex items-center justify-between p-4 bg-background rounded-lg border border-darkGray cursor-pointer">
            <span className="text-sm text-text font-sans">Envoyer par email à l'utilisateur</span>
            <input
              type="checkbox"
              checked={sendEmail}
              onChange={(e) => setSendEmail(e.target.checked)}
              className="w-4 h-4 rounded border-darkGray text-primary focus:ring-primary"
            />
          </label>

          <div className="flex items-center gap-3 pt-4">
            <button
              onClick={onReset}
              className="flex-1 px-4 py-3 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors font-sans font-medium"
            >
              Réinitialiser
            </button>
            <button
              onClick={onClose}
              className="flex-1 px-4 py-3 bg-darkGray hover:bg-gray-700 text-text rounded-lg transition-colors font-sans font-medium"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
