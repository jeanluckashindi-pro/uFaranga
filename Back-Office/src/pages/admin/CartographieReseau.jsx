import { useState, useRef, useEffect } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { 
  MAPBOX_TOKEN
} from '../../config/mapbox';
import {
  MapPin, Search, Home, Layers, Move, X, Users, TrendingUp, Globe as GlobeIcon
} from 'lucide-react';

mapboxgl.accessToken = MAPBOX_TOKEN;

// Pays utilisant l'infrastructure uFaranga
const UFARANGA_COUNTRIES = [
  { 
    name: 'Burundi', 
    code: 'BI',
    lat: -3.3731, 
    lng: 29.9189,
    agents: 1234,
    users: 456000,
    volume: 2300000000, // BIF
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'Rwanda', 
    code: 'RW',
    lat: -1.9403, 
    lng: 29.8739,
    agents: 2156,
    users: 890000,
    volume: 5600000000,
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'RD Congo', 
    code: 'CD',
    lat: -4.0383, 
    lng: 21.7587,
    agents: 3421,
    users: 1200000,
    volume: 8900000000,
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'Tanzanie', 
    code: 'TZ',
    lat: -6.3690, 
    lng: 34.8888,
    agents: 1876,
    users: 670000,
    volume: 4200000000,
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'Kenya', 
    code: 'KE',
    lat: -0.0236, 
    lng: 37.9062,
    agents: 4532,
    users: 2100000,
    volume: 12000000000,
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'Ouganda', 
    code: 'UG',
    lat: 1.3733, 
    lng: 32.2903,
    agents: 2987,
    users: 980000,
    volume: 6700000000,
    status: 'actif',
    color: '#007BFF'
  },
  { 
    name: 'Sénégal', 
    code: 'SN',
    lat: 14.4974, 
    lng: -14.4524,
    agents: 1654,
    users: 540000,
    volume: 3400000000,
    status: 'en_deploiement',
    color: '#F58424'
  },
  { 
    name: 'Côte d\'Ivoire', 
    code: 'CI',
    lat: 7.5400, 
    lng: -5.5471,
    agents: 2234,
    users: 780000,
    volume: 5100000000,
    status: 'en_deploiement',
    color: '#F58424'
  },
];

const STATUS_COLORS = {
  actif: '#42b72a',
  en_deploiement: '#F58424',
  inactif: '#8B1538'
};

function CartographieReseau() {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [isPanelOpen, setIsPanelOpen] = useState(true);
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/dark-v11');
  const [viewMode, setViewMode] = useState('2d'); // 2D par défaut
  const markersRef = useRef([]);

  // Filtrer les pays
  const filteredCountries = UFARANGA_COUNTRIES.filter(country => 
    country.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    country.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Statistiques globales
  const stats = {
    countries: UFARANGA_COUNTRIES.length,
    agents: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.agents, 0),
    users: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.users, 0),
    volume: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.volume, 0)
  };

  // Initialiser la carte
  useEffect(() => {
    if (map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: mapStyle,
      center: [25, -2], // Centre Afrique de l'Est
      zoom: 4,
      pitch: 0, // Vue 2D
      bearing: 0,
      antialias: true
    });

    map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
    map.current.addControl(new mapboxgl.FullscreenControl(), 'top-right');

    map.current.on('load', () => {
      setMapLoaded(true);
    });

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Mettre à jour les marqueurs
  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    // Supprimer les anciens marqueurs
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    // Ajouter les marqueurs des pays
    filteredCountries.forEach(country => {
      const el = document.createElement('div');
      el.innerHTML = `
        <div style="position: relative;">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="${country.color}" stroke="white" stroke-width="1.5" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.4)); transition: all 0.2s;">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3" fill="white"></circle>
          </svg>
          <div style="position: absolute; top: -8px; right: -8px; background: ${STATUS_COLORS[country.status]}; color: white; border-radius: 50%; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; border: 2px solid white;">
            ${country.code}
          </div>
        </div>
      `;
      el.style.cursor = 'pointer';

      el.addEventListener('mouseenter', () => {
        el.firstElementChild.firstElementChild.style.transform = 'scale(1.2)';
      });
      el.addEventListener('mouseleave', () => {
        el.firstElementChild.firstElementChild.style.transform = 'scale(1)';
      });

      el.addEventListener('click', () => {
        flyToCountry(country);
      });

      const marker = new mapboxgl.Marker(el)
        .setLngLat([country.lng, country.lat])
        .setPopup(
          new mapboxgl.Popup({ offset: 20 })
            .setHTML(`
              <div style="padding: 12px; min-width: 250px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                  <h3 style="font-weight: bold; font-size: 18px; color: #00070F;">${country.name}</h3>
                  <span style="padding: 2px 8px; border-radius: 9999px; font-size: 11px; font-weight: 600; ${
                    country.status === 'actif'
                      ? 'background: #dcfce7; color: #16a34a;'
                      : 'background: #fff3cd; color: #856404;'
                  }">
                    ${country.status === 'actif' ? 'Actif' : 'En déploiement'}
                  </span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 12px;">
                  <div style="display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #666;">Agents:</span>
                    <span style="font-weight: 600; color: #007BFF;">${country.agents.toLocaleString()}</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #666;">Utilisateurs:</span>
                    <span style="font-weight: 600; color: #F58424;">${(country.users / 1000).toFixed(0)}K</span>
                  </div>
                  <div style="display: flex; justify-content: space-between; font-size: 13px;">
                    <span style="color: #666;">Volume:</span>
                    <span style="font-weight: 600; color: #16a34a;">${(country.volume / 1000000000).toFixed(1)}B</span>
                  </div>
                </div>
              </div>
            `)
        )
        .addTo(map.current);

      markersRef.current.push(marker);
    });
  }, [mapLoaded, filteredCountries]);

  const flyToCountry = (country) => {
    if (map.current) {
      map.current.flyTo({
        center: [country.lng, country.lat],
        zoom: 7,
        pitch: 0, // Rester en 2D
        bearing: 0,
        duration: 2000
      });
      setSelectedCountry(country);
    }
  };

  const changeMapStyle = (style) => {
    if (map.current) {
      map.current.setStyle(style);
      setMapStyle(style);
    }
  };

  const toggleViewMode = () => {
    if (map.current) {
      if (viewMode === '2d') {
        map.current.easeTo({ pitch: 45, bearing: 0, duration: 1000 });
        setViewMode('3d');
      } else {
        map.current.easeTo({ pitch: 0, bearing: 0, duration: 1000 });
        setViewMode('2d');
      }
    }
  };

  const resetView = () => {
    if (map.current) {
      map.current.flyTo({
        center: [25, -2],
        zoom: 4,
        pitch: 0, // Rester en 2D
        bearing: 0,
        duration: 1500
      });
      setSelectedCountry(null);
    }
  };

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Carte - Plein écran */}
      <div className="flex-1 relative">
        <div ref={mapContainer} className="w-full h-full" />

        {/* Contrôles de la carte */}
        <div className="absolute top-4 left-4 flex flex-col gap-2">
          <button
            onClick={() => setIsPanelOpen(!isPanelOpen)}
            className="p-3 bg-card/95 backdrop-blur-sm border border-primary rounded-lg shadow-lg hover:bg-primary hover:text-white transition-all"
            title="Ouvrir/Fermer le panneau"
          >
            <Search className="w-5 h-5" />
          </button>

          <button
            onClick={resetView}
            className="p-3 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg shadow-lg hover:border-primary hover:text-primary transition-all"
            title="Réinitialiser la vue"
          >
            <Home className="w-5 h-5" />
          </button>

          <button
            onClick={toggleViewMode}
            className={`p-3 backdrop-blur-sm border rounded-lg shadow-lg transition-all ${
              viewMode === '3d'
                ? 'bg-primary text-white border-primary'
                : 'bg-card/95 border-darkGray hover:border-primary'
            }`}
            title={viewMode === '2d' ? 'Passer en 3D' : 'Passer en 2D'}
          >
            <Layers className="w-5 h-5" />
          </button>

          <div className="flex flex-col gap-1 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg p-2 shadow-lg">
            <button
              onClick={() => changeMapStyle('mapbox://styles/mapbox/dark-v11')}
              className={`px-3 py-2 rounded transition-all text-xs font-semibold ${
                mapStyle === 'mapbox://styles/mapbox/dark-v11'
                  ? 'bg-primary text-white'
                  : 'hover:bg-darkGray text-gray-400'
              }`}
            >
              Sombre
            </button>
            <button
              onClick={() => changeMapStyle('mapbox://styles/mapbox/streets-v12')}
              className={`px-3 py-2 rounded transition-all text-xs font-semibold ${
                mapStyle === 'mapbox://styles/mapbox/streets-v12'
                  ? 'bg-primary text-white'
                  : 'hover:bg-darkGray text-gray-400'
              }`}
            >
              Rues
            </button>
            <button
              onClick={() => changeMapStyle('mapbox://styles/mapbox/satellite-streets-v12')}
              className={`px-3 py-2 rounded transition-all text-xs font-semibold ${
                mapStyle === 'mapbox://styles/mapbox/satellite-streets-v12'
                  ? 'bg-primary text-white'
                  : 'hover:bg-darkGray text-gray-400'
              }`}
            >
              Satellite
            </button>
          </div>
        </div>

        {/* Stats globales - En haut au centre */}
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2">
          <div className="bg-card/95 backdrop-blur-sm border border-primary rounded-lg shadow-lg px-6 py-3">
            <div className="flex items-center gap-6">
              <div className="text-center">
                <div className="text-xs text-gray-400">Pays</div>
                <div className="text-lg font-bold text-primary">{stats.countries}</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400">Agents</div>
                <div className="text-lg font-bold text-secondary">{(stats.agents / 1000).toFixed(1)}K</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400">Utilisateurs</div>
                <div className="text-lg font-bold text-text">{(stats.users / 1000000).toFixed(1)}M</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400">Volume</div>
                <div className="text-lg font-bold text-text">{(stats.volume / 1000000000).toFixed(1)}B</div>
              </div>
            </div>
          </div>
        </div>

        {/* Badge pays sélectionné */}
        {selectedCountry && (
          <div className="absolute top-20 left-1/2 transform -translate-x-1/2">
            <div className="flex items-center gap-2 px-4 py-2 bg-card/95 backdrop-blur-sm border border-secondary rounded-lg shadow-lg">
              <GlobeIcon className="w-4 h-4 text-secondary" />
              <span className="text-secondary font-semibold text-sm">{selectedCountry.name}</span>
              <button
                onClick={() => setSelectedCountry(null)}
                className="ml-1 hover:bg-secondary/30 rounded-full p-0.5 transition-colors"
              >
                <X className="w-3 h-3 text-secondary" />
              </button>
            </div>
          </div>
        )}

        {/* Panneau de recherche */}
        {isPanelOpen && (
          <div 
            className="absolute top-4 right-4 w-80 bg-card/95 backdrop-blur-sm border border-primary rounded-lg shadow-2xl"
            style={{ maxHeight: 'calc(100vh - 200px)' }}
          >
            <div className="p-3 border-b border-darkGray flex items-center justify-between cursor-move bg-primary/10">
              <div className="flex items-center gap-2">
                <Move className="w-4 h-4 text-primary" />
                <h3 className="text-sm font-semibold text-text">Réseau uFaranga</h3>
              </div>
              <button
                onClick={() => setIsPanelOpen(false)}
                className="p-1 hover:bg-danger/20 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-400 hover:text-danger" />
              </button>
            </div>

            <div className="p-3 space-y-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Rechercher un pays..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text text-sm placeholder-gray-500 focus:outline-none focus:border-primary transition-colors"
                />
              </div>
            </div>

            <div className="max-h-96 overflow-y-auto border-t border-darkGray">
              <div className="p-2 space-y-1">
                <p className="text-xs text-gray-400 px-2 py-1">
                  {filteredCountries.length} pays
                </p>
                {filteredCountries.map((country) => (
                  <div
                    key={country.code}
                    onClick={() => flyToCountry(country)}
                    className={`p-2 rounded-lg cursor-pointer transition-all ${
                      selectedCountry?.code === country.code
                        ? 'bg-primary text-white'
                        : 'bg-background/50 hover:bg-background text-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 flex-1 min-w-0">
                        <span
                          className={`h-2 w-2 rounded-full flex-shrink-0`}
                          style={{ backgroundColor: STATUS_COLORS[country.status] }}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-xs truncate">{country.name}</p>
                          <p className="text-xs opacity-70">{country.agents.toLocaleString()} agents</p>
                        </div>
                      </div>
                      <MapPin className="w-3 h-3 flex-shrink-0" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Légende */}
        <div className="absolute bottom-4 right-4 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg p-3 shadow-2xl">
          <p className="text-xs font-semibold text-text mb-2">Statut</p>
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: STATUS_COLORS.actif }}></div>
              <span className="text-xs text-gray-400">Actif</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: STATUS_COLORS.en_deploiement }}></div>
              <span className="text-xs text-gray-400">En déploiement</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CartographieReseau;
