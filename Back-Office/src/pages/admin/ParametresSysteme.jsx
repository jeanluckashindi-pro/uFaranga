import { useState } from 'react';
import {
  Settings, Palette, Layout, Menu, Plus, Edit2, Trash2, Save,
  X, ChevronDown, ChevronRight, Eye, EyeOff, Globe, Shield
} from 'lucide-react';
import { Card } from '../../components/common';

const ParametresSysteme = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [showModuleModal, setShowModuleModal] = useState(false);
  const [showMenuModal, setShowMenuModal] = useState(false);
  const [editingModule, setEditingModule] = useState(null);
  const [editingMenu, setEditingMenu] = useState(null);

  // État pour la configuration générale
  const [config, setConfig] = useState({
    platformName: 'uFaranga',
    platformSlogan: 'Simply Money',
    primaryColor: '#007BFF',
    secondaryColor: '#F58424',
    backgroundColor: '#00070F',
    cardBackground: '#181F27',
    textColor: '#F9F9F9',
  });

  // État pour les modules
  const [modules, setModules] = useState([
    { id: 'admin_system', name: 'Administration Système', icon: 'Shield', color: 'danger', active: true },
    { id: 'admin_tech', name: 'Administration Technique', icon: 'Server', color: 'primary', active: true },
    { id: 'agent', name: 'Espace Agent', icon: 'Users', color: 'primary', active: true },
    { id: 'client', name: 'Espace Client', icon: 'User', color: 'primary', active: true },
  ]);

  // État pour les menus
  const [menus, setMenus] = useState({
    admin_system: [
      { id: 1, label: 'Dashboard Global', path: '/admin/dashboard', icon: 'LayoutDashboard', active: true },
      { id: 2, label: 'Gestion Agents', path: '/admin/agents', icon: 'Users', active: true },
    ],
  });

  const handleSaveConfig = () => {
    console.log('Configuration sauvegardée:', config);
    // TODO: Appel API pour sauvegarder
  };

  return (
    <div className="min-h-screen bg-background p-6 md:p-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-heading font-bold text-text mb-2">Paramètres Système</h1>
        <p className="text-gray-400 font-sans">Configuration complète de la plateforme uFaranga</p>
      </div>

      {/* Onglets */}
      <Card className="mb-6 p-0 overflow-hidden">
        <div className="flex gap-0 overflow-x-auto">
          {[
            { id: 'general', label: 'Général', icon: Settings },
            { id: 'apparence', label: 'Apparence', icon: Palette },
            { id: 'modules', label: 'Modules', icon: Layout },
            { id: 'navigation', label: 'Navigation', icon: Menu },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-all whitespace-nowrap font-sans ${
                activeTab === tab.id
                  ? 'border-primary text-primary bg-primary/10'
                  : 'border-transparent text-gray-400 hover:text-text hover:bg-darkGray'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              <span className="text-sm font-medium">{tab.label}</span>
            </button>
          ))}
        </div>
      </Card>

      {/* Contenu des onglets */}
      {activeTab === 'general' && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-heading font-bold text-text">Configuration Générale</h2>
            <button
              onClick={handleSaveConfig}
              className="px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 font-sans"
            >
              <Save className="w-4 h-4" />
              Enregistrer
            </button>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Nom de la plateforme</label>
              <input
                type="text"
                value={config.platformName}
                onChange={(e) => setConfig({ ...config, platformName: e.target.value })}
                className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Slogan</label>
              <input
                type="text"
                value={config.platformSlogan}
                onChange={(e) => setConfig({ ...config, platformSlogan: e.target.value })}
                className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
              />
            </div>
          </div>
        </Card>
      )}

      {activeTab === 'apparence' && (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-heading font-bold text-text">Personnalisation de l'apparence</h2>
            <button
              onClick={handleSaveConfig}
              className="px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 font-sans"
            >
              <Save className="w-4 h-4" />
              Enregistrer
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ColorPicker
              label="Couleur primaire"
              value={config.primaryColor}
              onChange={(color) => setConfig({ ...config, primaryColor: color })}
            />
            <ColorPicker
              label="Couleur secondaire"
              value={config.secondaryColor}
              onChange={(color) => setConfig({ ...config, secondaryColor: color })}
            />
            <ColorPicker
              label="Arrière-plan"
              value={config.backgroundColor}
              onChange={(color) => setConfig({ ...config, backgroundColor: color })}
            />
            <ColorPicker
              label="Arrière-plan des cartes"
              value={config.cardBackground}
              onChange={(color) => setConfig({ ...config, cardBackground: color })}
            />
            <ColorPicker
              label="Couleur du texte"
              value={config.textColor}
              onChange={(color) => setConfig({ ...config, textColor: color })}
            />
          </div>
        </Card>
      )}

      {activeTab === 'modules' && (
        <div className="space-y-6">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-heading font-bold text-text">Gestion des Modules</h2>
              <button
                onClick={() => {
                  setEditingModule(null);
                  setShowModuleModal(true);
                }}
                className="px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 font-sans"
              >
                <Plus className="w-4 h-4" />
                Nouveau Module
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {modules.map((module) => (
                <div
                  key={module.id}
                  className="p-4 bg-background border border-darkGray rounded-lg hover:border-primary transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-lg bg-${module.color}/10 flex items-center justify-center`}>
                        <Shield className={`w-5 h-5 text-${module.color}`} />
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-text font-sans">{module.name}</h3>
                        <p className="text-xs text-gray-400 font-mono">{module.id}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setEditingModule(module);
                          setShowModuleModal(true);
                        }}
                        className="p-1.5 hover:bg-darkGray rounded transition-colors"
                      >
                        <Edit2 className="w-4 h-4 text-gray-400" />
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Supprimer le module "${module.name}" ?`)) {
                            setModules(modules.filter(m => m.id !== module.id));
                          }
                        }}
                        className="p-1.5 hover:bg-darkGray rounded transition-colors"
                      >
                        <Trash2 className="w-4 h-4 text-red-400" />
                      </button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className={`px-2 py-1 rounded text-xs font-medium font-sans ${
                      module.active ? 'bg-green-400/20 text-green-400' : 'bg-gray-400/20 text-gray-400'
                    }`}>
                      {module.active ? 'Actif' : 'Inactif'}
                    </span>
                    <button
                      onClick={() => {
                        setModules(modules.map(m =>
                          m.id === module.id ? { ...m, active: !m.active } : m
                        ));
                      }}
                      className="text-xs text-primary hover:text-blue-400 font-sans"
                    >
                      {module.active ? 'Désactiver' : 'Activer'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {activeTab === 'navigation' && (
        <div className="space-y-6">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-heading font-bold text-text">Gestion de la Navigation</h2>
              <button
                onClick={() => {
                  setEditingMenu(null);
                  setShowMenuModal(true);
                }}
                className="px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 font-sans"
              >
                <Plus className="w-4 h-4" />
                Nouveau Menu
              </button>
            </div>

            <div className="space-y-4">
              {modules.map((module) => (
                <div key={module.id} className="border border-darkGray rounded-lg overflow-hidden">
                  <div className="p-4 bg-card flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Shield className="w-5 h-5 text-primary" />
                      <span className="font-bold text-text font-sans">{module.name}</span>
                    </div>
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="p-4 space-y-2">
                    {menus[module.id]?.map((menu) => (
                      <div
                        key={menu.id}
                        className="flex items-center justify-between p-3 bg-background rounded-lg hover:bg-darkGray transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <Menu className="w-4 h-4 text-gray-400" />
                          <div>
                            <p className="text-sm font-medium text-text font-sans">{menu.label}</p>
                            <p className="text-xs text-gray-400 font-mono">{menu.path}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {menu.active ? (
                            <Eye className="w-4 h-4 text-green-400" />
                          ) : (
                            <EyeOff className="w-4 h-4 text-gray-400" />
                          )}
                          <button className="p-1.5 hover:bg-card rounded transition-colors">
                            <Edit2 className="w-4 h-4 text-gray-400" />
                          </button>
                          <button className="p-1.5 hover:bg-card rounded transition-colors">
                            <Trash2 className="w-4 h-4 text-red-400" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* Modal Nouveau/Éditer Module */}
      {showModuleModal && (
        <Modal
          title={editingModule ? 'Modifier le Module' : 'Nouveau Module'}
          onClose={() => setShowModuleModal(false)}
        >
          <ModuleForm
            module={editingModule}
            onSave={(module) => {
              if (editingModule) {
                setModules(modules.map(m => m.id === module.id ? module : m));
              } else {
                setModules([...modules, { ...module, id: `module_${Date.now()}` }]);
              }
              setShowModuleModal(false);
            }}
            onCancel={() => setShowModuleModal(false)}
          />
        </Modal>
      )}

      {/* Modal Nouveau/Éditer Menu */}
      {showMenuModal && (
        <Modal
          title={editingMenu ? 'Modifier le Menu' : 'Nouveau Menu'}
          onClose={() => setShowMenuModal(false)}
        >
          <MenuForm
            menu={editingMenu}
            modules={modules}
            onSave={(menu) => {
              // TODO: Logique de sauvegarde
              setShowMenuModal(false);
            }}
            onCancel={() => setShowMenuModal(false)}
          />
        </Modal>
      )}
    </div>
  );
};

// Composant ColorPicker
const ColorPicker = ({ label, value, onChange }) => {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">{label}</label>
      <div className="flex items-center gap-3">
        <input
          type="color"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-12 h-12 rounded-lg cursor-pointer border-2 border-darkGray"
        />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-mono"
        />
      </div>
    </div>
  );
};

// Composant Modal
const Modal = ({ title, children, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-darkGray rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-card border-b border-darkGray p-6 flex items-center justify-between">
          <h3 className="text-xl font-heading font-bold text-text">{title}</h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-darkGray rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
};

// Composant ModuleForm
const ModuleForm = ({ module, onSave, onCancel }) => {
  const [formData, setFormData] = useState(module || {
    name: '',
    icon: 'Shield',
    color: 'primary',
    active: true,
  });

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Nom du module</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
          placeholder="Ex: Administration Système"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Icône</label>
        <select
          value={formData.icon}
          onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
        >
          <option value="Shield">Shield</option>
          <option value="Users">Users</option>
          <option value="Server">Server</option>
          <option value="Globe">Globe</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Couleur</label>
        <select
          value={formData.color}
          onChange={(e) => setFormData({ ...formData, color: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
        >
          <option value="primary">Primaire (Bleu)</option>
          <option value="secondary">Secondaire (Orange)</option>
          <option value="danger">Danger (Rouge)</option>
        </select>
      </div>

      <div className="flex items-center gap-3 pt-4">
        <button
          onClick={() => onSave(formData)}
          className="flex-1 px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors font-sans"
        >
          Enregistrer
        </button>
        <button
          onClick={onCancel}
          className="flex-1 px-4 py-2 bg-darkGray hover:bg-gray-700 text-text rounded-lg transition-colors font-sans"
        >
          Annuler
        </button>
      </div>
    </div>
  );
};

// Composant MenuForm
const MenuForm = ({ menu, modules, onSave, onCancel }) => {
  const [formData, setFormData] = useState(menu || {
    label: '',
    path: '',
    icon: 'Menu',
    moduleId: modules[0]?.id || '',
    active: true,
  });

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Module parent</label>
        <select
          value={formData.moduleId}
          onChange={(e) => setFormData({ ...formData, moduleId: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
        >
          {modules.map(m => (
            <option key={m.id} value={m.id}>{m.name}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Label du menu</label>
        <input
          type="text"
          value={formData.label}
          onChange={(e) => setFormData({ ...formData, label: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
          placeholder="Ex: Dashboard Global"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Chemin (URL)</label>
        <input
          type="text"
          value={formData.path}
          onChange={(e) => setFormData({ ...formData, path: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-mono"
          placeholder="/admin/dashboard"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-400 mb-2 font-sans">Icône</label>
        <select
          value={formData.icon}
          onChange={(e) => setFormData({ ...formData, icon: e.target.value })}
          className="w-full px-4 py-2 bg-background border border-darkGray rounded-lg text-text focus:outline-none focus:border-primary font-sans"
        >
          <option value="LayoutDashboard">Dashboard</option>
          <option value="Users">Users</option>
          <option value="Activity">Activity</option>
          <option value="Settings">Settings</option>
        </select>
      </div>

      <div className="flex items-center gap-3 pt-4">
        <button
          onClick={() => onSave(formData)}
          className="flex-1 px-4 py-2 bg-primary hover:bg-blue-700 text-white rounded-lg transition-colors font-sans"
        >
          Enregistrer
        </button>
        <button
          onClick={onCancel}
          className="flex-1 px-4 py-2 bg-darkGray hover:bg-gray-700 text-text rounded-lg transition-colors font-sans"
        >
          Annuler
        </button>
      </div>
    </div>
  );
};

export default ParametresSysteme;
