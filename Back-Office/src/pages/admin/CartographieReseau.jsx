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
    color: '#007BFF',
    population: 13000000,
    ufarangaUsers: 456000,
    penetration: 3.5 // % du territoire
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
    color: '#007BFF',
    population: 13500000,
    ufarangaUsers: 890000,
    penetration: 6.6
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
    color: '#007BFF',
    population: 99000000,
    ufarangaUsers: 1200000,
    penetration: 1.2
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
    color: '#007BFF',
    population: 65000000,
    ufarangaUsers: 670000,
    penetration: 1.0
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
    color: '#007BFF',
    population: 54000000,
    ufarangaUsers: 2100000,
    penetration: 3.9
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
    color: '#007BFF',
    population: 47000000,
    ufarangaUsers: 980000,
    penetration: 2.1
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
    color: '#F58424',
    population: 17000000,
    ufarangaUsers: 540000,
    penetration: 3.2
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
    color: '#F58424',
    population: 28000000,
    ufarangaUsers: 780000,
    penetration: 2.8
  }
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
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [selectedCountryDetail, setSelectedCountryDetail] = useState(null);
  const [highlightedCountry, setHighlightedCountry] = useState(null);
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/dark-v11');
  const [viewMode, setViewMode] = useState('2d'); // 2D par défaut
  const markersRef = useRef([]);

  // Filtrer les pays
  const filteredCountries = UFARANGA_COUNTRIES.filter(country => 
    country.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    country.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Statistiques globales ou du pays sélectionné
  const displayStats = highlightedCountry ? {
    countries: 1,
    agents: highlightedCountry.agents,
    users: highlightedCountry.users,
    volume: highlightedCountry.volume,
    coverageAfrica: highlightedCountry.penetration,
    coverageWorld: (highlightedCountry.penetration * 0.15).toFixed(2)
  } : {
    countries: UFARANGA_COUNTRIES.length,
    agents: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.agents, 0),
    users: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.users, 0),
    volume: UFARANGA_COUNTRIES.reduce((sum, c) => sum + c.volume, 0),
    coverageAfrica: 15,
    coverageWorld: 0.4
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
      antialias: true,
      attributionControl: false // Enlever les attributions Mapbox
    });

    // Pas de contrôles par défaut

    map.current.on('load', () => {
      // Liste des codes ISO des pays couverts
      const coveredCountries = ['BI', 'RW', 'CD', 'TZ', 'KE', 'UG', 'SN', 'CI'];
      
      // Ajouter une couche pour colorer les pays couverts
      map.current.addLayer({
        id: 'country-fills',
        type: 'fill',
        source: {
          type: 'vector',
          url: 'mapbox://mapbox.country-boundaries-v1'
        },
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...coveredCountries],
        paint: {
          'fill-color': '#007BFF',
          'fill-opacity': 0.4
        }
      });

      // Ajouter une couche pour le pays sélectionné (rouge)
      map.current.addLayer({
        id: 'country-highlight',
        type: 'fill',
        source: {
          type: 'vector',
          url: 'mapbox://mapbox.country-boundaries-v1'
        },
        'source-layer': 'country_boundaries',
        filter: ['==', 'iso_3166_1', ''], // Vide par défaut
        paint: {
          'fill-color': '#8B1538',
          'fill-opacity': 0.6
        }
      });

      // Ajouter les bordures des pays couverts
      map.current.addLayer({
        id: 'country-borders',
        type: 'line',
        source: {
          type: 'vector',
          url: 'mapbox://mapbox.country-boundaries-v1'
        },
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...coveredCountries],
        paint: {
          'line-color': '#F58424',
          'line-width': 3,
          'line-opacity': 1
        }
      });

      // Ajouter les labels au centre de chaque pays
      UFARANGA_COUNTRIES.forEach(country => {
        const labelEl = document.createElement('div');
        labelEl.className = 'country-label';
        labelEl.dataset.countryCode = country.code; // Stocker le code du pays
        labelEl.style.cssText = `
          text-align: center;
          pointer-events: auto;
          cursor: pointer;
          transform: rotate(-15deg);
          text-shadow: 
            2px 2px 0px rgba(0,0,0,0.8),
            4px 4px 0px rgba(0,0,0,0.6),
            6px 6px 0px rgba(0,0,0,0.4),
            8px 8px 10px rgba(0,0,0,0.3);
          transition: transform 0.2s;
        `;
        labelEl.innerHTML = `
          <div style="font-family: 'Anton', sans-serif; font-size: 20px; color: white; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 1px;">
            ${country.name}
          </div>
          <div style="font-size: 12px; color: white; margin-bottom: 2px; font-weight: 600;">
            ${(country.population / 1000000).toFixed(1)}M habitants
          </div>
          <div style="font-size: 12px; color: white; font-weight: 700;">
            uFaranga: ${(country.ufarangaUsers / 1000).toFixed(0)}K
          </div>
          <div style="font-size: 11px; color: white; opacity: 0.9;">
            ${country.penetration}% du territoire
          </div>
        `;

        labelEl.addEventListener('mouseenter', () => {
          labelEl.style.transform = 'rotate(-15deg) scale(1.1)';
        });
        labelEl.addEventListener('mouseleave', () => {
          labelEl.style.transform = 'rotate(-15deg) scale(1)';
        });

        new mapboxgl.Marker(labelEl, { anchor: 'center' })
          .setLngLat([country.lng, country.lat])
          .addTo(map.current);
      });

      setMapLoaded(true);
    });

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Mettre à jour les marqueurs - DÉSACTIVÉ
  /*
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
  */

  // Gérer les clics sur les labels de pays
  useEffect(() => {
    const handleLabelClick = (e) => {
      const label = e.target.closest('.country-label');
      if (label && label.dataset.countryCode) {
        const country = UFARANGA_COUNTRIES.find(c => c.code === label.dataset.countryCode);
        if (country) {
          setHighlightedCountry(country);
          setSelectedCountryDetail(country);
        }
      }
    };

    document.addEventListener('click', handleLabelClick);
    return () => document.removeEventListener('click', handleLabelClick);
  }, []);

  // Mettre à jour la couleur du pays sélectionné
  useEffect(() => {
    if (!map.current || !mapLoaded) return;
    
    if (highlightedCountry) {
      map.current.setFilter('country-highlight', ['==', 'iso_3166_1', highlightedCountry.code]);
    } else {
      map.current.setFilter('country-highlight', ['==', 'iso_3166_1', '']);
    }
  }, [highlightedCountry, mapLoaded]);

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
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10">
          <div className="bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg shadow-lg px-4 py-2">
            {highlightedCountry && (
              <div className="text-center mb-2 pb-2 border-b border-darkGray">
                <span className="text-xs text-secondary font-semibold uppercase">{highlightedCountry.name}</span>
                <button 
                  onClick={() => setHighlightedCountry(null)}
                  className="ml-2 text-xs text-gray-400 hover:text-danger"
                >
                  <X className="w-3 h-3 inline" />
                </button>
              </div>
            )}
            <div className="flex items-center gap-4">
              <div className="text-center">
                <div className="text-xs text-gray-400 mb-0.5">Pays</div>
                <div className="text-xl font-bold text-primary">{displayStats.countries}</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400 mb-0.5">Agents</div>
                <div className="text-xl font-bold text-secondary">{(displayStats.agents / 1000).toFixed(1)}K</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400 mb-0.5">Utilisateurs</div>
                <div className="text-xl font-bold text-text">{(displayStats.users / 1000000).toFixed(1)}M</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400 mb-0.5">Volume</div>
                <div className="text-xl font-bold text-text">{(displayStats.volume / 1000000000).toFixed(1)}B BIF</div>
              </div>
              <div className="h-8 w-px bg-darkGray"></div>
              <div className="text-center">
                <div className="text-xs text-gray-400 mb-0.5">Couverture</div>
                <div className="flex items-center gap-2">
                  <div className="text-center">
                    <div className="text-sm font-bold text-secondary">Afrique</div>
                    <div className="text-xs text-gray-400">{displayStats.coverageAfrica}%</div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm font-bold text-primary">Monde</div>
                    <div className="text-xs text-gray-400">{displayStats.coverageWorld}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Badge pays sélectionné */}
        {selectedCountry && (
          <div className="absolute top-16 left-1/2 transform -translate-x-1/2 z-10">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg shadow-lg">
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
            className="absolute top-4 right-4 w-80 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg shadow-2xl overflow-hidden"
            style={{ maxHeight: 'calc(100vh - 100px)', cursor: 'move' }}
            draggable="true"
            onDragStart={(e) => {
              e.dataTransfer.effectAllowed = 'move';
            }}
          >
            {/* Header */}
            <div className="p-3 border-b border-darkGray flex items-center justify-between bg-darkGray/30 cursor-move">
              <div className="flex items-center gap-2">
                <GlobeIcon className="w-4 h-4 text-primary" />
                <h3 className="text-sm font-semibold text-text">Réseau uFaranga</h3>
              </div>
              <button
                onClick={() => setIsPanelOpen(false)}
                className="p-1 hover:bg-danger/20 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-400 hover:text-danger" />
              </button>
            </div>

            {/* Search */}
            <div className="p-3 border-b border-darkGray">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Rechercher un pays..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text text-sm placeholder-gray-500 focus:outline-none focus:border-darkGray transition-colors"
                />
              </div>
            </div>

            {/* Countries List */}
            <div className="overflow-y-auto" style={{ maxHeight: 'calc(100vh - 250px)' }}>
              <div className="p-2">
                <p className="text-xs text-gray-400 px-2 py-1 mb-1">
                  {filteredCountries.length} pays trouvés
                </p>
                <div className="space-y-1">
                  {filteredCountries.map((country) => (
                  <div
                    key={country.code}
                    onClick={() => flyToCountry(country)}
                    className={`p-3 rounded-lg cursor-pointer transition-all border ${
                      selectedCountry?.code === country.code
                        ? 'bg-primary/20 border-primary text-white'
                        : 'bg-background/50 hover:bg-darkGray border-darkGray text-gray-300'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-start gap-2 flex-1 min-w-0">
                        <span
                          className={`h-2.5 w-2.5 rounded-full flex-shrink-0 mt-1`}
                          style={{ backgroundColor: STATUS_COLORS[country.status] }}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-sm truncate mb-1">{country.name}</p>
                          <div className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-xs">
                            <div className="text-gray-400">
                              <span className="opacity-60">Agents:</span> <span className="text-secondary font-semibold">{country.agents.toLocaleString()}</span>
                            </div>
                            <div className="text-gray-400">
                              <span className="opacity-60">Users:</span> <span className="text-text font-semibold">{(country.users / 1000).toFixed(0)}K</span>
                            </div>
                            <div className="text-gray-400 col-span-2">
                              <span className="opacity-60">Volume:</span> <span className="text-primary font-semibold">{(country.volume / 1000000000).toFixed(1)}B BIF</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <MapPin className="w-4 h-4 flex-shrink-0 mt-0.5 opacity-50" />
                    </div>
                  </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal détails du pays */}
        {selectedCountryDetail && (
          <div className="absolute inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setSelectedCountryDetail(null)}>
            <div className="bg-card border border-darkGray rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
              {/* Header */}
              <div className="p-6 border-b border-darkGray bg-darkGray/30 sticky top-0 z-10">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-3xl font-anton uppercase text-secondary">{selectedCountryDetail.name}</h2>
                    <p className="text-sm text-gray-400 mt-1">Analyse approfondie de la couverture uFaranga</p>
                  </div>
                  <button
                    onClick={() => setSelectedCountryDetail(null)}
                    className="p-2 hover:bg-danger/20 rounded-lg transition-colors"
                  >
                    <X className="w-6 h-6 text-gray-400 hover:text-danger" />
                  </button>
                </div>
              </div>

              {/* Contenu */}
              <div className="p-6 space-y-6">
                {/* Stats principales - Grid 4 colonnes */}
                <div className="grid grid-cols-4 gap-4">
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="text-xs text-gray-400 mb-1">Population totale</div>
                    <div className="text-2xl font-bold text-text">{(selectedCountryDetail.population / 1000000).toFixed(1)}M</div>
                    <div className="text-xs text-gray-500 mt-1">habitants</div>
                  </div>
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="text-xs text-gray-400 mb-1">Utilisateurs uFaranga</div>
                    <div className="text-2xl font-bold text-primary">{(selectedCountryDetail.ufarangaUsers / 1000).toFixed(0)}K</div>
                    <div className="text-xs text-secondary mt-1">+{((selectedCountryDetail.ufarangaUsers / selectedCountryDetail.population) * 100).toFixed(1)}% pop.</div>
                  </div>
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="text-xs text-gray-400 mb-1">Agents actifs</div>
                    <div className="text-2xl font-bold text-secondary">{selectedCountryDetail.agents.toLocaleString()}</div>
                    <div className="text-xs text-gray-500 mt-1">{(selectedCountryDetail.ufarangaUsers / selectedCountryDetail.agents).toFixed(0)} users/agent</div>
                  </div>
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="text-xs text-gray-400 mb-1">Volume mensuel</div>
                    <div className="text-2xl font-bold text-text">{(selectedCountryDetail.volume / 1000000000).toFixed(2)}B</div>
                    <div className="text-xs text-gray-500 mt-1">BIF</div>
                  </div>
                </div>

                {/* Taux de pénétration nationale */}
                <div className="bg-background border border-darkGray rounded-lg p-5">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-text">Taux de pénétration du territoire national</h3>
                    <div className="text-3xl font-bold text-secondary">{selectedCountryDetail.penetration}%</div>
                  </div>
                  <div className="h-6 bg-darkGray rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-primary via-secondary to-danger transition-all duration-500"
                      style={{ width: `${selectedCountryDetail.penetration}%` }}
                    />
                  </div>
                  <div className="mt-3 text-xs text-gray-400">
                    {selectedCountryDetail.ufarangaUsers.toLocaleString()} utilisateurs sur {selectedCountryDetail.population.toLocaleString()} habitants
                  </div>
                </div>

                {/* Couverture par zone - Grid 3 colonnes */}
                <div>
                  <h3 className="text-lg font-semibold text-text mb-3">Couverture par zone géographique</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-background border border-darkGray rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-sm text-gray-400">Zone Urbaine</div>
                        <div className="text-2xl font-bold text-primary">{(selectedCountryDetail.penetration * 2.5).toFixed(1)}%</div>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: `${Math.min(selectedCountryDetail.penetration * 2.5, 100)}%` }} />
                      </div>
                      <div className="text-xs text-gray-500 mt-2">{(selectedCountryDetail.ufarangaUsers * 0.6 / 1000).toFixed(0)}K utilisateurs</div>
                    </div>
                    <div className="bg-background border border-darkGray rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-sm text-gray-400">Zone Rurale</div>
                        <div className="text-2xl font-bold text-secondary">{(selectedCountryDetail.penetration * 0.8).toFixed(1)}%</div>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-secondary" style={{ width: `${selectedCountryDetail.penetration * 0.8}%` }} />
                      </div>
                      <div className="text-xs text-gray-500 mt-2">{(selectedCountryDetail.ufarangaUsers * 0.3 / 1000).toFixed(0)}K utilisateurs</div>
                    </div>
                    <div className="bg-background border border-darkGray rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-sm text-gray-400">Zone Périurbaine</div>
                        <div className="text-2xl font-bold text-text">{(selectedCountryDetail.penetration * 1.5).toFixed(1)}%</div>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-text" style={{ width: `${selectedCountryDetail.penetration * 1.5}%` }} />
                      </div>
                      <div className="text-xs text-gray-500 mt-2">{(selectedCountryDetail.ufarangaUsers * 0.1 / 1000).toFixed(0)}K utilisateurs</div>
                    </div>
                  </div>
                </div>

                {/* Analyses approfondies - Grid 2 colonnes */}
                <div className="grid grid-cols-2 gap-4">
                  {/* Performance */}
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <h4 className="text-sm font-semibold text-text mb-3">Performance du réseau</h4>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">Transactions/jour</span>
                        <span className="text-sm font-bold text-primary">{(selectedCountryDetail.volume / 30000000).toFixed(0)}K</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">Volume/agent</span>
                        <span className="text-sm font-bold text-secondary">{(selectedCountryDetail.volume / selectedCountryDetail.agents / 1000000).toFixed(1)}M BIF</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">Taux d'activité</span>
                        <span className="text-sm font-bold text-text">87%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">Croissance mensuelle</span>
                        <span className="text-sm font-bold text-secondary">+12%</span>
                      </div>
                    </div>
                  </div>

                  {/* Démographie */}
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <h4 className="text-sm font-semibold text-text mb-3">Profil démographique</h4>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">18-25 ans</span>
                        <span className="text-sm font-bold text-primary">35%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">26-40 ans</span>
                        <span className="text-sm font-bold text-secondary">42%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">41-60 ans</span>
                        <span className="text-sm font-bold text-text">18%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400">60+ ans</span>
                        <span className="text-sm font-bold text-gray-400">5%</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Services les plus utilisés */}
                <div className="bg-background border border-darkGray rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-text mb-3">Services les plus utilisés</h4>
                  <div className="space-y-2">
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-400">Transferts d'argent</span>
                        <span className="text-xs font-bold text-primary">45%</span>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '45%' }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-400">Paiement de factures</span>
                        <span className="text-xs font-bold text-secondary">28%</span>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-secondary" style={{ width: '28%' }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-400">Recharge téléphonique</span>
                        <span className="text-xs font-bold text-text">18%</span>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-text" style={{ width: '18%' }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs text-gray-400">Épargne</span>
                        <span className="text-xs font-bold text-gray-400">9%</span>
                      </div>
                      <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                        <div className="h-full bg-gray-400" style={{ width: '9%' }} />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Statut et objectifs */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-xs text-gray-400 mb-1">Statut du déploiement</div>
                        <div className="text-lg font-semibold text-text capitalize">{selectedCountryDetail.status.replace('_', ' ')}</div>
                      </div>
                      <div 
                        className="w-6 h-6 rounded-full"
                        style={{ backgroundColor: STATUS_COLORS[selectedCountryDetail.status] }}
                      />
                    </div>
                  </div>
                  <div className="bg-background border border-darkGray rounded-lg p-4">
                    <div className="text-xs text-gray-400 mb-1">Objectif 2026</div>
                    <div className="text-lg font-semibold text-secondary">{(selectedCountryDetail.penetration * 2.5).toFixed(1)}%</div>
                    <div className="text-xs text-gray-500 mt-1">de pénétration nationale</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CartographieReseau;
