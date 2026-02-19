import { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Tag } from 'primereact/tag';
import { Dialog } from 'primereact/dialog';
import { 
  Globe, MapPin, Plus, Edit2, Search, Download,
  CheckCircle, XCircle, Map, ArrowLeft, Building2, Eye,
  Power, Shield, MapPinned, Layers
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Skeleton } from '../../components/common';
import api from '../../services/api';

const GestionPays = () => {
  const navigate = useNavigate();
  const [pays, setPays] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(true);
  const [globalFilter, setGlobalFilter] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [selectedPays, setSelectedPays] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [actionType, setActionType] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [paysDetail, setPaysDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [lazyParams, setLazyParams] = useState({
    first: 0,
    rows: 10,
    page: 0,
  });
  const [statsGlobales, setStatsGlobales] = useState({
    total: 0,
    actifs: 0,
    autorises: 0,
    inactifs: 0,
  });

  // Charger les stats globales
  useEffect(() => {
    fetchStatsGlobales();
  }, []);

  const fetchStatsGlobales = async () => {
    try {
      // Charger tous les pays pour les stats
      const response = await api.request('/api/v1/localisation/pays/?limit=1000');
      const allPays = response.results || [];
      
      setStatsGlobales({
        total: response.count || 0,
        actifs: allPays.filter(p => p.est_actif).length,
        autorises: allPays.filter(p => p.autorise_systeme).length,
        inactifs: allPays.filter(p => !p.est_actif).length,
      });
    } catch (error) {
      console.error('Erreur chargement stats:', error);
    }
  };

  // Charger la liste des pays
  useEffect(() => {
    fetchPays();
  }, [globalFilter, selectedStatus, lazyParams]);

  const fetchPays = async () => {
    try {
      setLoading(true);
      
      // Construire les paramètres de requête
      const params = new URLSearchParams();
      
      // Filtrage par recherche
      if (globalFilter) {
        params.append('nom', globalFilter);
      }
      
      // Filtrage par statut
      if (selectedStatus === 'actif') {
        params.append('est_actif', 'true');
      } else if (selectedStatus === 'inactif') {
        params.append('est_actif', 'false');
      } else if (selectedStatus === 'autorise') {
        params.append('autorise_systeme', 'true');
      }
      
      // Pagination
      params.append('limit', lazyParams.rows);
      params.append('offset', lazyParams.first);
      
      const queryString = params.toString();
      const endpoint = `/api/v1/localisation/pays/${queryString ? `?${queryString}` : ''}`;
      
      const response = await api.request(endpoint);
      setPays(response.results || []);
      setTotalRecords(response.count || 0);
    } catch (error) {
      console.error('Erreur chargement pays:', error);
    } finally {
      setLoading(false);
    }
  };

  const onPage = (event) => {
    setLazyParams(event);
  };

  // Charger les détails d'un pays (avec provinces, districts, etc.)
  const fetchPaysDetail = async (paysId) => {
    try {
      setLoadingDetail(true);
      const response = await api.request(`/api/v1/localisation/pays/${paysId}/`);
      setPaysDetail(response);
    } catch (error) {
      console.error('Erreur chargement détails pays:', error);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleViewDetail = async (pays) => {
    // Naviguer vers la page de détails
    navigate(`/admin/pays/${pays.id}`);
  };

  const handleToggleAction = (pays, type) => {
    setSelectedPays(pays);
    setActionType(type);
    setShowConfirmDialog(true);
  };

  const confirmAction = async () => {
    if (!selectedPays || !actionType) return;

    try {
      setActionLoading(true);
      const updateData = {};
      
      if (actionType === 'actif') {
        updateData.est_actif = !selectedPays.est_actif;
      } else if (actionType === 'autorise') {
        updateData.autorise_systeme = !selectedPays.autorise_systeme;
      }

      await api.request(`/api/v1/localisation/pays/${selectedPays.id}/`, {
        method: 'PATCH',
        body: JSON.stringify(updateData),
      });

      // Recharger la liste
      await fetchPays();
      await fetchStatsGlobales();
      setShowConfirmDialog(false);
      setSelectedPays(null);
      setActionType(null);
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const statusOptions = [
    { label: 'Tous', value: 'all' },
    { label: 'Actifs', value: 'actif' },
    { label: 'Autorisés', value: 'autorise' },
    { label: 'Inactifs', value: 'inactif' }
  ];

  // Templates pour les colonnes
  const codeBodyTemplate = (rowData) => {
    return (
      <div className="flex items-center gap-2">
        <span className="font-mono text-primary font-semibold">{rowData.code_iso_2}</span>
        <span className="text-gray-500">/</span>
        <span className="font-mono text-gray-400 text-xs">{rowData.code_iso_3}</span>
      </div>
    );
  };

  const statutBodyTemplate = (rowData) => {
    return (
      <Tag 
        value={rowData.est_actif ? 'Actif' : 'Inactif'} 
        severity={rowData.est_actif ? 'success' : 'danger'} 
      />
    );
  };

  const autoriseBodyTemplate = (rowData) => {
    return (
      <Tag 
        value={rowData.autorise_systeme ? 'Oui' : 'Non'} 
        severity={rowData.autorise_systeme ? 'info' : 'warning'} 
      />
    );
  };

  const coordonneesBodyTemplate = (rowData) => {
    return (
      <div className="text-xs font-mono text-gray-400">
        <div>{rowData.latitude_centre}</div>
        <div>{rowData.longitude_centre}</div>
      </div>
    );
  };

  const dateBodyTemplate = (rowData) => {
    return new Date(rowData.date_creation).toLocaleDateString('fr-FR');
  };

  const actionsBodyTemplate = (rowData) => {
    return (
      <div className="flex gap-2">
        <button
          onClick={() => handleViewDetail(rowData)}
          className="p-2 bg-primary/10 text-primary rounded hover:bg-primary/20 transition-colors"
          title="Voir détails"
        >
          <Eye className="w-4 h-4" />
        </button>
        <button
          onClick={() => handleToggleAction(rowData, 'actif')}
          className={`p-2 rounded transition-colors ${
            rowData.est_actif 
              ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20' 
              : 'bg-green-500/10 text-green-400 hover:bg-green-500/20'
          }`}
          title={rowData.est_actif ? 'Désactiver' : 'Activer'}
        >
          <Power className="w-4 h-4" />
        </button>
        <button
          onClick={() => handleToggleAction(rowData, 'autorise')}
          className={`p-2 rounded transition-colors ${
            rowData.autorise_systeme 
              ? 'bg-orange-500/10 text-orange-400 hover:bg-orange-500/20' 
              : 'bg-blue-500/10 text-blue-400 hover:bg-blue-500/20'
          }`}
          title={rowData.autorise_systeme ? 'Retirer autorisation' : 'Autoriser'}
        >
          <Shield className="w-4 h-4" />
        </button>
      </div>
    );
  };

  // Skeleton Loading Component
  const DataTableSkeleton = () => (
    <div className="bg-card border border-darkGray rounded-lg p-6">
      <div className="space-y-4">
        {[...Array(10)].map((_, i) => (
          <div key={i} className="flex items-center gap-4">
            <Skeleton className="h-12 w-full" />
          </div>
        ))}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-6 md:p-10">
        {/* Header Skeleton */}
        <div className="mb-6">
          <Skeleton className="h-8 w-64 mb-4" />
          <div className="flex items-center justify-between">
            <div>
              <Skeleton className="h-10 w-80 mb-2" />
              <Skeleton className="h-4 w-96" />
            </div>
            <Skeleton className="h-10 w-40" />
          </div>
        </div>

        {/* Stats Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-card border border-darkGray rounded-lg p-4">
              <div className="flex items-center gap-3">
                <Skeleton className="h-12 w-12 rounded-lg" />
                <div className="flex-1">
                  <Skeleton className="h-4 w-24 mb-2" />
                  <Skeleton className="h-8 w-16" />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Filters Skeleton */}
        <div className="bg-card border border-darkGray rounded-lg p-4 mb-6">
          <div className="flex gap-4">
            <Skeleton className="h-10 flex-1" />
            <Skeleton className="h-10 w-48" />
            <Skeleton className="h-10 w-32" />
          </div>
        </div>

        {/* DataTable Skeleton */}
        <DataTableSkeleton />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-6 md:p-10">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/admin/couverture-mondiale')}
          className="flex items-center gap-2 text-gray-400 hover:text-text transition-colors mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Retour à Couverture Mondiale</span>
        </button>
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-anton uppercase text-text">Gestion des Pays</h1>
            <p className="text-sm text-gray-400 mt-1">Configuration et gestion des pays dans le système</p>
          </div>
          <div className="flex gap-3">
            <button 
              onClick={() => navigate('/admin/cartographie-couverture')}
              className="flex items-center gap-2 px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary/90 transition-colors"
            >
              <Layers className="w-5 h-5" />
              <span>Cartographie</span>
            </button>
            <button 
              onClick={() => navigate('/admin/carte-mondiale')}
              className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              <MapPinned className="w-5 h-5" />
              <span>Carte Mondiale</span>
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">
              <Plus className="w-5 h-5" />
              <span>Ajouter un pays</span>
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-card border border-darkGray rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Globe className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Pays</p>
              <p className="text-2xl font-bold text-text">{statsGlobales.total}</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-darkGray rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-secondary/10 rounded-lg">
              <CheckCircle className="w-6 h-6 text-secondary" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Actifs</p>
              <p className="text-2xl font-bold text-secondary">{statsGlobales.actifs}</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-darkGray rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Map className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Autorisés</p>
              <p className="text-2xl font-bold text-text">{statsGlobales.autorises}</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-darkGray rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-danger/10 rounded-lg">
              <XCircle className="w-6 h-6 text-danger" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Inactifs</p>
              <p className="text-2xl font-bold text-danger">{statsGlobales.inactifs}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-card border border-darkGray rounded-lg p-4 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <InputText
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              placeholder="Rechercher par nom, code ISO..."
              className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text"
            />
          </div>
          
          <Dropdown
            value={selectedStatus}
            options={statusOptions}
            onChange={(e) => setSelectedStatus(e.value)}
            className="w-full md:w-48"
          />

          <button className="flex items-center gap-2 px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary/90 transition-colors">
            <Download className="w-5 h-5" />
            <span>Exporter</span>
          </button>
        </div>
      </div>

      {/* DataTable */}
      <div className="bg-card border border-darkGray rounded-lg overflow-hidden">
        <DataTable
          value={pays}
          lazy
          paginator
          first={lazyParams.first}
          rows={lazyParams.rows}
          totalRecords={totalRecords}
          onPage={onPage}
          rowsPerPageOptions={[5, 10, 25, 50]}
          loading={loading}
          className="custom-datatable"
          emptyMessage="Aucun pays trouvé"
        >
          <Column field="nom" header="Pays" sortable style={{ minWidth: '150px' }} />
          <Column field="nom_anglais" header="Nom Anglais" sortable />
          <Column header="Codes ISO" body={codeBodyTemplate} />
          <Column header="Coordonnées" body={coordonneesBodyTemplate} />
          <Column field="est_actif" header="Statut" body={statutBodyTemplate} sortable />
          <Column field="autorise_systeme" header="Autorisé" body={autoriseBodyTemplate} sortable />
          <Column field="date_creation" header="Date Création" body={dateBodyTemplate} sortable />
          <Column header="Actions" body={actionsBodyTemplate} />
        </DataTable>
      </div>

      {/* Dialog Détails Pays */}
      <Dialog
        visible={showDetailModal}
        onHide={() => {
          setShowDetailModal(false);
          setSelectedPays(null);
          setPaysDetail(null);
        }}
        header="Détails du Pays"
        style={{ width: '700px' }}
        className="custom-dialog"
      >
        {selectedPays && (
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 bg-background rounded-lg">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <Globe className="w-8 h-8 text-primary" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-text">{selectedPays.nom}</h3>
                <p className="text-sm text-gray-400">{selectedPays.nom_anglais}</p>
                <p className="text-xs text-gray-500 font-mono mt-1">
                  {selectedPays.code_iso_2} / {selectedPays.code_iso_3}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-background rounded-lg">
                <p className="text-xs text-gray-400 mb-1">Latitude Centre</p>
                <p className="text-sm font-medium text-text font-mono">{selectedPays.latitude_centre}</p>
              </div>
              <div className="p-3 bg-background rounded-lg">
                <p className="text-xs text-gray-400 mb-1">Longitude Centre</p>
                <p className="text-sm font-medium text-text font-mono">{selectedPays.longitude_centre}</p>
              </div>
            </div>

            <div className="flex gap-2">
              <div className={`flex-1 p-3 rounded-lg ${
                selectedPays.autorise_systeme 
                  ? 'bg-secondary/10 border border-secondary/30' 
                  : 'bg-gray-500/10 border border-gray-500/30'
              }`}>
                <p className="text-xs text-gray-400 mb-1">Autorisé Système</p>
                <p className={`text-sm font-bold ${
                  selectedPays.autorise_systeme ? 'text-secondary' : 'text-gray-400'
                }`}>
                  {selectedPays.autorise_systeme ? 'Oui' : 'Non'}
                </p>
              </div>
              <div className={`flex-1 p-3 rounded-lg ${
                selectedPays.est_actif 
                  ? 'bg-green-500/10 border border-green-500/30' 
                  : 'bg-red-500/10 border border-red-500/30'
              }`}>
                <p className="text-xs text-gray-400 mb-1">Statut</p>
                <p className={`text-sm font-bold ${
                  selectedPays.est_actif ? 'text-green-400' : 'text-red-400'
                }`}>
                  {selectedPays.est_actif ? 'Actif' : 'Inactif'}
                </p>
              </div>
            </div>

            <div className="p-3 bg-background rounded-lg">
              <p className="text-xs text-gray-400 mb-1">Date de création</p>
              <p className="text-sm font-medium text-text">
                {new Date(selectedPays.date_creation).toLocaleString('fr-FR')}
              </p>
            </div>

            {loadingDetail ? (
              <div className="flex items-center justify-center py-8">
                <Skeleton className="h-20 w-full" />
              </div>
            ) : paysDetail && paysDetail.provinces && paysDetail.provinces.length > 0 ? (
              <div>
                <h4 className="text-sm font-bold text-text mb-3 flex items-center gap-2">
                  <Building2 className="w-4 h-4 text-primary" />
                  Provinces ({paysDetail.provinces.length})
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 max-h-60 overflow-y-auto">
                  {paysDetail.provinces.map((province) => (
                    <div
                      key={province.id}
                      className="p-3 bg-background border border-darkGray rounded-lg"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <p className="text-sm font-medium text-text">{province.nom}</p>
                        <span className="text-xs text-gray-400 font-mono">{province.code}</span>
                      </div>
                      <p className="text-xs text-gray-400">
                        {province.districts?.length || 0} district(s)
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        )}
      </Dialog>

      {/* Dialog Confirmation Action */}
      <Dialog
        visible={showConfirmDialog}
        onHide={() => {
          setShowConfirmDialog(false);
          setSelectedPays(null);
          setActionType(null);
        }}
        header="Confirmation"
        style={{ width: '450px' }}
        className="custom-dialog"
      >
        {selectedPays && actionType && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-4 bg-background rounded-lg">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                actionType === 'actif' 
                  ? (selectedPays.est_actif ? 'bg-red-500/10' : 'bg-green-500/10')
                  : (selectedPays.autorise_systeme ? 'bg-orange-500/10' : 'bg-blue-500/10')
              }`}>
                {actionType === 'actif' ? (
                  <Power className={`w-6 h-6 ${selectedPays.est_actif ? 'text-red-400' : 'text-green-400'}`} />
                ) : (
                  <Shield className={`w-6 h-6 ${selectedPays.autorise_systeme ? 'text-orange-400' : 'text-blue-400'}`} />
                )}
              </div>
              <div>
                <h3 className="text-base font-bold text-text">{selectedPays.nom}</h3>
                <p className="text-sm text-gray-400">{selectedPays.code_iso_2}</p>
              </div>
            </div>

            <p className="text-sm text-gray-300">
              {actionType === 'actif' ? (
                selectedPays.est_actif 
                  ? `Êtes-vous sûr de vouloir désactiver ce pays ? Il ne sera plus visible dans le système.`
                  : `Êtes-vous sûr de vouloir activer ce pays ? Il sera visible dans le système.`
              ) : (
                selectedPays.autorise_systeme 
                  ? `Êtes-vous sûr de vouloir retirer l'autorisation système pour ce pays ?`
                  : `Êtes-vous sûr de vouloir autoriser ce pays dans le système ?`
              )}
            </p>

            <div className="flex gap-3 justify-end">
              <button
                onClick={() => {
                  setShowConfirmDialog(false);
                  setSelectedPays(null);
                  setActionType(null);
                }}
                disabled={actionLoading}
                className="px-4 py-2 bg-darkGray text-text rounded-lg hover:bg-darkGray/80 transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={confirmAction}
                disabled={actionLoading}
                className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${
                  actionType === 'actif'
                    ? (selectedPays.est_actif 
                        ? 'bg-red-500 hover:bg-red-600 text-white' 
                        : 'bg-green-500 hover:bg-green-600 text-white')
                    : (selectedPays.autorise_systeme 
                        ? 'bg-orange-500 hover:bg-orange-600 text-white' 
                        : 'bg-blue-500 hover:bg-blue-600 text-white')
                }`}
              >
                {actionLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Traitement...</span>
                  </>
                ) : (
                  <span>Confirmer</span>
                )}
              </button>
            </div>
          </div>
        )}
      </Dialog>
    </div>
  );
};

export default GestionPays;
