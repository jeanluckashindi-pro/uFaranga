import { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { MAPBOX_TOKEN } from '../../config/mapbox';
import {
  MapPin, Search, Home, Layers, X, Users, Globe as GlobeIcon,
  ChevronRight, Building2, MapPinned, GripVertical, ChevronDown, ChevronUp
} from 'lucide-react';
import apiService from '../../services/api';
import { RadialSpinner } from '../../components/common/Spinner';

mapboxgl.accessToken = MAPBOX_TOKEN;

const COUNTRY_SOURCE_ID = 'country-boundaries';
const SOUSREGION_LAYER_PREFIX = 'country-border-sousregion-';

const COULEUR_NON_OCCUPE = '#007BFF';   // blue (legacy)
const COULEUR_OCCUPE = '#F58424';       // secondary (pays/zone occupés)
const COULEUR_GRIS = '#6B7280';
/** Pays du système : bleu transparent (tous les pays de la base) */
const COULEUR_PAYS_SYSTEME = '#007BFF'; // blue, opacity via paint
const COULEUR_PROVINCE_NON_OCCUPE = '#4B5563'; // gray-600
const COULEUR_PROVINCE = COULEUR_PROVINCE_NON_OCCUPE;  // provinces non occupées = gris
const COULEUR_DISTRICT_NON_OCCUPE = '#4B5563'; // gray-600
const COULEUR_DISTRICT = '#F58424';     // districts occupés = secondary
const COULEUR_QUARTIER = '#10b981';     // emerald
const ZONE_SOURCE_ID = 'zones-selected-country';

/** Palette pro par sous-région (vision géographique cohérente, couleurs distinctes) */
const SOUS_REGION_PALETTE = {
  'afrique-australe': '#0EA5E9',      // sky-500
  'afrique-de-lest': '#8B5CF6',      // violet-500
  'afrique-centrale': '#059669',      // emerald-600
  'afrique-de-louest': '#D97706',     // amber-600
  'afrique-du-nord': '#DC2626',       // red-600
  'afrique-orientale': '#8B5CF6',
  'afrique-occidentale': '#D97706',
  'southern-africa': '#0EA5E9',
  'eastern-africa': '#8B5CF6',
  'western-africa': '#D97706',
  'middle-africa': '#059669',
  'northern-africa': '#DC2626',
};
const SOUS_REGION_FALLBACK = '#64748B'; // slate-500

function slugSousRegion(s) {
  if (!s || typeof s !== 'string') return 'autre';
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/'/g, '')
    .replace(/\s+/g, '-')
    .replace(/l-est/g, 'lest')
    .replace(/l-ouest/g, 'louest')
    .replace(/[^a-z0-9-]/g, '')
    .trim() || 'autre';
}

function getCouleurSousRegion(sousRegion) {
  const slug = slugSousRegion(sousRegion);
  return SOUS_REGION_PALETTE[slug] ?? SOUS_REGION_FALLBACK;
}

function isActifAutorise(item) {
  return item && item.est_actif === true && item.autorise_systeme === true;
}

/** Construit la liste des pays avec provinces/districts/quartiers imbriqués à partir de la réponse API. */
function buildLocalisationTree(response) {
  if (!response) return [];
  // Format déjà imbriqué (pays avec .provinces)
  if (Array.isArray(response) && response.length > 0 && response[0].provinces) {
    return response;
  }
  // Format plat : { pays: [], provinces: [], districts: [], quartiers: [] }
  const paysList = response.pays ?? [];
  const provincesList = response.provinces ?? [];
  const districtsList = response.districts ?? [];
  const quartiersList = response.quartiers ?? [];
  if (!Array.isArray(paysList) || paysList.length === 0) return [];

  const sid = (x) => (x != null ? String(x) : '');
  const paysById = {};
  paysList.forEach((p) => { paysById[sid(p.id)] = { ...p, provinces: [] }; });

  const provincesById = {};
  provincesList.forEach((pr) => {
    const paysRef = pr.pays ?? pr.pays_id;
    const paysId = sid(typeof paysRef === 'object' && paysRef != null ? paysRef.id : paysRef);
    if (paysId && paysById[paysId]) {
      const prov = { ...pr, districts: [] };
      provincesById[sid(pr.id)] = prov;
      paysById[paysId].provinces.push(prov);
    }
  });

  districtsList.forEach((d) => {
    const provRef = d.province ?? d.province_id;
    const provId = sid(typeof provRef === 'object' && provRef != null ? provRef.id : provRef);
    if (provId && provincesById[provId]) {
      const dist = {
        ...d,
        quartiers: (quartiersList || []).filter((q) => {
          const qDist = q.district ?? q.district_id;
          return sid(typeof qDist === 'object' && qDist != null ? qDist.id : qDist) === sid(d.id);
        }),
      };
      provincesById[provId].districts.push(dist);
    }
  });

  return Object.values(paysById);
}

function CartographieReseau() {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [countriesData, setCountriesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null); // { type: 'pays'|'province'|'district', data }
  const [expandedProvinces, setExpandedProvinces] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [isPanelOpen, setIsPanelOpen] = useState(true);
  const [mapStyle, setMapStyle] = useState('mapbox://styles/mapbox/dark-v11');
  const [viewMode, setViewMode] = useState('2d');
  const [statsExpanded, setStatsExpanded] = useState(false);
  const [statsPosition, setStatsPosition] = useState(null);
  const [panelPosition, setPanelPosition] = useState(null);
  const [draggingCard, setDraggingCard] = useState(null);
  const dragStartRef = useRef({ x: 0, y: 0, left: 0, top: 0 });
  const mapWrapperRef = useRef(null);
  const statsCardRef = useRef(null);
  const panelRef = useRef(null);
  const zonesSourceId = ZONE_SOURCE_ID;
  const selectedCountryRef = useRef(null);
  selectedCountryRef.current = selectedCountry;

  const fetchLocalisationComplete = useCallback(async () => {
    setLoading(true);
    setFetchError(null);
    try {
      const response = await apiService.getLocalisationComplete();
      const list = buildLocalisationTree(response);
      setCountriesData(list);
    } catch (err) {
      console.error('Erreur chargement localisation complète:', err);
      setCountriesData([]);
      setFetchError(err?.message || 'Impossible de charger les données.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLocalisationComplete();
  }, [fetchLocalisationComplete]);

  const allCountryCodes = countriesData.map((p) => p.code_iso_2).filter(Boolean);
  const activeCountryCodes = countriesData
    .filter((p) => isActifAutorise(p))
    .map((p) => p.code_iso_2)
    .filter(Boolean);

  const filteredCountries = countriesData.filter(
    (c) =>
      (c.nom || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (c.code_iso_2 || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  /** Pays filtrés groupés par sous-région pour l’affichage panneau (ordre stable, libellés propres) */
  const filteredCountriesBySousRegion = useMemo(() => {
    const groups = {};
    filteredCountries.forEach((c) => {
      const sr = c.sous_region || 'Autre';
      if (!groups[sr]) groups[sr] = [];
      groups[sr].push(c);
    });
    return Object.entries(groups).sort((a, b) => (a[0] || '').localeCompare(b[0] || ''));
  }, [filteredCountries]);

  // Grouper les pays par sous-région pour la carte et la légende
  const sousRegionToCodes = useMemo(() => {
    const m = {};
    countriesData.forEach((p) => {
      const sr = p.sous_region || 'Autre';
      if (!m[sr]) m[sr] = [];
      if (p.code_iso_2) m[sr].push(p.code_iso_2);
    });
    return m;
  }, [countriesData]);

  const displayStats = selectedCountry
    ? {
        countries: 1,
        agents: selectedCountry.nombre_agents ?? 0,
        users: selectedCountry.nombre_utilisateurs ?? 0,
        provinces: selectedCountry.provinces?.length ?? 0,
        districts: (selectedCountry.provinces || []).reduce(
          (acc, p) => acc + (p.districts?.length ?? 0),
          0
        ),
      }
    : {
        countries: countriesData.length,
        agents: countriesData.reduce((s, c) => s + (c.nombre_agents ?? 0), 0),
        users: countriesData.reduce((s, c) => s + (c.nombre_utilisateurs ?? 0), 0),
        provinces: countriesData.reduce((s, c) => s + (c.provinces?.length ?? 0), 0),
        districts: countriesData.reduce(
          (s, c) => s + (c.provinces || []).reduce((a, p) => a + (p.districts?.length ?? 0), 0),
          0
        ),
      };

  const reapplyLayers = useCallback(
    (highlightCode = '') => {
      if (!map.current || !map.current.getLayer('country-fills-click')) return;
      const codes = allCountryCodes.length ? allCountryCodes : ['__none__'];
      const activeCodes = activeCountryCodes.length ? activeCountryCodes : ['__none__'];

      const style = map.current.getStyle();
      const layersToRemove = (style?.layers || [])
        .filter((l) => l.id.startsWith(SOUSREGION_LAYER_PREFIX) || l.id.startsWith('country-fill-sousregion-'))
        .map((l) => l.id);
      layersToRemove.forEach((id) => {
        if (map.current.getLayer(id)) map.current.removeLayer(id);
        if (map.current.getSource(id)) map.current.removeSource(id);
      });
      // Nettoyer les sources orphelines (ancien code ou hot-reload)
      Object.keys(style?.sources || {}).forEach((sourceId) => {
        if (sourceId.startsWith(SOUSREGION_LAYER_PREFIX) || sourceId.startsWith('country-fill-sousregion-')) {
          try {
            if (map.current.getSource(sourceId)) map.current.removeSource(sourceId);
          } catch (_) { /* ignoré */ }
        }
      });

      if (!map.current.getSource(COUNTRY_SOURCE_ID)) return;
      const systemFilter = codes.length && codes[0] !== '__none__' ? ['in', 'iso_3166_1', ...codes] : ['==', 'iso_3166_1', '__none__'];
      if (!map.current.getLayer('country-fills-inactive')) {
        map.current.addLayer(
          {
            id: 'country-fills-inactive',
            type: 'fill',
            source: COUNTRY_SOURCE_ID,
            'source-layer': 'country_boundaries',
            filter: systemFilter,
            paint: { 'fill-color': COULEUR_PAYS_SYSTEME, 'fill-opacity': 0.35 },
          },
          'country-fills-active'
        );
      } else {
        map.current.setFilter('country-fills-inactive', systemFilter);
      }

      map.current.setFilter('country-fills-click', ['in', 'iso_3166_1', ...codes]);
      map.current.setFilter('country-fills-active', ['in', 'iso_3166_1', ...activeCodes]);
      map.current.setFilter('country-borders-active', ['in', 'iso_3166_1', ...activeCodes]);
      map.current.setFilter('country-highlight', ['==', 'iso_3166_1', highlightCode || '']);
    },
    [allCountryCodes, activeCountryCodes]
  );

  const handleDragStart = useCallback((card, e) => {
    if (e.button !== 0 || !mapWrapperRef.current) return;
    const el = card === 'stats' ? statsCardRef.current : panelRef.current;
    if (!el) return;
    const wr = mapWrapperRef.current.getBoundingClientRect();
    const cr = el.getBoundingClientRect();
    const left = cr.left - wr.left;
    const top = cr.top - wr.top;
    setStatsPosition((prev) => (card === 'stats' ? (prev ?? { x: left, y: top }) : prev));
    setPanelPosition((prev) => (card === 'panel' ? (prev ?? { x: left, y: top }) : prev));
    setDraggingCard(card);
    dragStartRef.current = { x: e.clientX, y: e.clientY, left, top };
  }, []);

  useEffect(() => {
    if (!draggingCard) return;
    const onMove = (e) => {
      const { x, y, left, top } = dragStartRef.current;
      const dx = e.clientX - x;
      const dy = e.clientY - y;
      if (draggingCard === 'stats') {
        setStatsPosition({ x: left + dx, y: top + dy });
      } else {
        setPanelPosition({ x: left + dx, y: top + dy });
      }
    };
    const onUp = () => setDraggingCard(null);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, [draggingCard]);

  // Initialiser la carte et les couches
  useEffect(() => {
    if (map.current || !mapContainer.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: mapStyle,
      center: [25, -2],
      zoom: 4,
      pitch: 0,
      bearing: 0,
      antialias: true,
      attributionControl: false,
    });

    map.current.on('load', () => {
      const codes = allCountryCodes.length ? allCountryCodes : ['__none__'];
      const activeCodes = activeCountryCodes.length ? activeCountryCodes : ['__none__'];

      if (!map.current.getSource(COUNTRY_SOURCE_ID)) {
        map.current.addSource(COUNTRY_SOURCE_ID, {
          type: 'vector',
          url: 'mapbox://mapbox.country-boundaries-v1',
        });
      }

      const systemFilterLoad = (codes[0] === '__none__' || !codes.length) ? ['==', 'iso_3166_1', '__none__'] : ['in', 'iso_3166_1', ...codes];
      map.current.addLayer({
        id: 'country-fills-inactive',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: systemFilterLoad,
        paint: { 'fill-color': COULEUR_PAYS_SYSTEME, 'fill-opacity': 0.35 },
      });
      map.current.addLayer({
        id: 'country-fills-active',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...activeCodes],
        paint: { 'fill-color': COULEUR_OCCUPE, 'fill-opacity': 0.5 },
      });

      map.current.addLayer({
        id: 'country-highlight',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['==', 'iso_3166_1', ''],
        paint: { 'fill-color': COULEUR_OCCUPE, 'fill-opacity': 0.35 },
      });

      map.current.addLayer({
        id: 'country-borders-active',
        type: 'line',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...activeCodes],
        paint: {
          'line-color': COULEUR_OCCUPE,
          'line-width': 2,
          'line-opacity': 1,
        },
      });

      map.current.addLayer({
        id: 'country-fills-click',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...codes],
        paint: { 'fill-color': '#000', 'fill-opacity': 0 },
      });

      map.current.on('click', 'country-fills-click', (e) => {
        const feat = e.features?.[0];
        const iso = feat?.properties?.iso_3166_1;
        if (!iso) return;
        const country = countriesData.find((c) => c.code_iso_2 === iso);
        if (country) {
          flyToCountry(country);
          setSelectedCountry(country);
          setSelectedRegion({ type: 'pays', data: country });
        }
      });

      map.current.getCanvas().style.cursor = '';
      map.current.on('mouseenter', 'country-fills-click', () => {
        map.current.getCanvas().style.cursor = 'pointer';
      });
      map.current.on('mouseleave', 'country-fills-click', () => {
        map.current.getCanvas().style.cursor = '';
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

  // Mettre à jour les couches quand les données changent
  useEffect(() => {
    if (!map.current || !mapLoaded) return;
    if (!map.current.getLayer('country-fills-click')) return;
    reapplyLayers(selectedCountry?.code_iso_2 || '');
  }, [mapLoaded, countriesData, selectedCountry, reapplyLayers]);

  // Zones (provinces, districts, quartiers) en cercles colorés avec animations
  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    const removeZones = () => {
      ['zones-quartiers', 'zones-districts', 'zones-provinces', 'zones-quartiers-stroke', 'zones-districts-stroke', 'zones-provinces-stroke'].forEach((id) => {
        if (map.current.getLayer(id)) map.current.removeLayer(id);
      });
      if (map.current.getSource(zonesSourceId)) map.current.removeSource(zonesSourceId);
    };

    if (!selectedCountry?.provinces?.length) {
      removeZones();
      return;
    }

    const parseCoord = (v) => {
      if (v == null) return NaN;
      const s = String(v).trim().replace(',', '.');
      const n = parseFloat(s);
      return Number.isFinite(n) ? n : NaN;
    };
    const countryLng = parseCoord(selectedCountry.longitude_centre);
    const countryLat = parseCoord(selectedCountry.latitude_centre);
    const defaultMapCentre = [25, -2];
    const countryCentre = Number.isFinite(countryLng) && Number.isFinite(countryLat)
      ? [countryLng, countryLat]
      : defaultMapCentre;

    const lngLat = (item, fallback) => {
      const lat = parseCoord(item.latitude_centre ?? item.latitude);
      const lng = parseCoord(item.longitude_centre ?? item.longitude);
      if (Number.isFinite(lat) && Number.isFinite(lng)) return [lng, lat];
      return fallback ?? null;
    };

    const features = [];
    (selectedCountry.provinces || []).forEach((prov) => {
      const pos = lngLat(prov, countryCentre);
      if (pos) {
        features.push({
          type: 'Feature',
          geometry: { type: 'Point', coordinates: pos },
          properties: { id: String(prov.id), nom: prov.nom || '', level: 'province', occupé: isActifAutorise(prov) ? 1 : 0 },
        });
      }
      (prov.districts || []).forEach((dist) => {
        const posD = lngLat(dist, pos || countryCentre);
        if (posD) {
          features.push({
            type: 'Feature',
            geometry: { type: 'Point', coordinates: posD },
            properties: { id: String(dist.id), nom: dist.nom || '', level: 'district', occupé: isActifAutorise(dist) ? 1 : 0, province_id: String(prov.id) },
          });
        }
        (dist.quartiers || []).forEach((q) => {
          const posQ = lngLat(q, posD || pos || countryCentre);
          if (posQ) {
            features.push({
              type: 'Feature',
              geometry: { type: 'Point', coordinates: posQ },
              properties: { id: String(q.id), nom: q.nom || '', level: 'quartier', occupé: isActifAutorise(q) ? 1 : 0 },
            });
          }
        });
      });
    });

    removeZones();
    const geo = { type: 'FeatureCollection', features };

    map.current.addSource(zonesSourceId, { type: 'geojson', data: geo });

    const findRegion = (id, level) => {
      const c = selectedCountryRef.current;
      if (!c) return null;
      if (level === 'province') return c.provinces?.find((p) => String(p.id) === id) || null;
      for (const p of c.provinces || []) {
        if (level === 'district') { const d = p.districts?.find((dd) => String(dd.id) === id); if (d) return d; }
        for (const d of p.districts || []) {
          if (level === 'quartier') { const q = d.quartiers?.find((qq) => String(qq.id) === id); if (q) return q; }
        }
      }
      return null;
    };

    const handleZoneClick = (e) => {
      const f = e.features?.[0];
      if (!f) return;
      const { id, level } = f.properties;
      const type = level === 'province' ? 'province' : level === 'district' ? 'district' : 'quartier';
      const data = findRegion(id, level);
      if (data) {
        setSelectedRegion({ type, data });
        if (type === 'province') setExpandedProvinces((prev) => new Set(prev).add(id));
      }
    };

    // Ordre: provinces (grands) en dessous, puis districts, puis quartiers (petits) au-dessus
    map.current.addLayer({
      id: 'zones-provinces',
      type: 'circle',
      source: zonesSourceId,
      filter: ['==', ['get', 'level'], 'province'],
      paint: {
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 12, 8, 28, 12, 48],
        'circle-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, COULEUR_PROVINCE],
        'circle-opacity': 0,
        'circle-stroke-width': 2,
        'circle-stroke-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, 'rgba(0,123,255,0.8)'],
      },
    });
    map.current.addLayer({
      id: 'zones-districts',
      type: 'circle',
      source: zonesSourceId,
      filter: ['==', ['get', 'level'], 'district'],
      paint: {
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 6, 8, 14, 12, 24],
        'circle-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, COULEUR_DISTRICT_NON_OCCUPE],
        'circle-opacity': 0,
        'circle-stroke-width': 1.5,
        'circle-stroke-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, 'rgba(75,85,99,0.8)'],
      },
    });
    map.current.addLayer({
      id: 'zones-quartiers',
      type: 'circle',
      source: zonesSourceId,
      filter: ['==', ['get', 'level'], 'quartier'],
      paint: {
        'circle-radius': ['interpolate', ['linear'], ['zoom'], 5, 3, 8, 8, 12, 14],
        'circle-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, COULEUR_QUARTIER],
        'circle-opacity': 0,
        'circle-stroke-width': 1,
        'circle-stroke-color': ['case', ['==', ['get', 'occupé'], 1], COULEUR_OCCUPE, 'rgba(16,185,129,0.8)'],
      },
    });

    const selectedProvinceId = selectedRegion?.type === 'province' ? String(selectedRegion?.data?.id ?? '') : '';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (!map.current.getLayer('zones-provinces')) return;
        map.current.setPaintProperty('zones-provinces', 'circle-opacity', 0.5);
        map.current.setPaintProperty('zones-districts', 'circle-opacity', selectedProvinceId
          ? ['case', ['==', ['get', 'province_id'], selectedProvinceId], 0.7, 0.22]
          : 0.5);
        map.current.setPaintProperty('zones-quartiers', 'circle-opacity', 0.55);
      });
    });

    ['zones-provinces', 'zones-districts', 'zones-quartiers'].forEach((layerId) => {
      map.current.on('click', layerId, handleZoneClick);
      map.current.on('mouseenter', layerId, () => { map.current.getCanvas().style.cursor = 'pointer'; });
      map.current.on('mouseleave', layerId, () => { map.current.getCanvas().style.cursor = ''; });
    });

    return () => {
      removeZones();
      ['zones-provinces', 'zones-districts', 'zones-quartiers'].forEach((layerId) => {
        if (map.current) {
          map.current.off('click', layerId);
          map.current.off('mouseenter', layerId);
          map.current.off('mouseleave', layerId);
        }
      });
    };
  }, [mapLoaded, selectedCountry, selectedRegion]);

  useEffect(() => {
    if (!map.current || !mapLoaded) return;
    if (!map.current.getLayer('country-highlight')) return;
    map.current.setFilter('country-highlight', [
      '==',
      'iso_3166_1',
      selectedCountry?.code_iso_2 || '',
    ]);
  }, [selectedCountry, mapLoaded]);

  const flyToCountry = (country) => {
    if (!map.current || !country) return;
    const lng = parseFloat(country.longitude_centre);
    const lat = parseFloat(country.latitude_centre);
    if (Number.isFinite(lng) && Number.isFinite(lat)) {
      map.current.flyTo({ center: [lng, lat], zoom: 6, duration: 1500 });
    }
    setSelectedCountry(country);
    setSelectedRegion({ type: 'pays', data: country });
  };

  const changeMapStyle = (style) => {
    if (!map.current) return;
    const center = map.current.getCenter();
    const zoom = map.current.getZoom();
    const pitch = map.current.getPitch();
    const bearing = map.current.getBearing();

    map.current.setStyle(style);
    setMapStyle(style);

    map.current.once('style.load', () => {
      map.current.jumpTo({ center, zoom, pitch, bearing });
      const codes = allCountryCodes.length ? allCountryCodes : ['__none__'];
      const activeCodes = activeCountryCodes.length ? activeCountryCodes : ['__none__'];

      if (!map.current.getSource(COUNTRY_SOURCE_ID)) {
        map.current.addSource(COUNTRY_SOURCE_ID, {
          type: 'vector',
          url: 'mapbox://mapbox.country-boundaries-v1',
        });
      }

      const systemFilterStyle = codes.length ? ['in', 'iso_3166_1', ...codes] : ['==', 'iso_3166_1', '__none__'];
      map.current.addLayer({
        id: 'country-fills-inactive',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: systemFilterStyle,
        paint: { 'fill-color': COULEUR_PAYS_SYSTEME, 'fill-opacity': 0.35 },
      });
      map.current.addLayer({
        id: 'country-fills-active',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...activeCodes],
        paint: { 'fill-color': COULEUR_OCCUPE, 'fill-opacity': 0.5 },
      });
      map.current.addLayer({
        id: 'country-highlight',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['==', 'iso_3166_1', selectedCountry?.code_iso_2 || ''],
        paint: { 'fill-color': COULEUR_OCCUPE, 'fill-opacity': 0.35 },
      });
      map.current.addLayer({
        id: 'country-borders-active',
        type: 'line',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...activeCodes],
        paint: {
          'line-color': COULEUR_OCCUPE,
          'line-width': 2,
          'line-opacity': 1,
        },
      });
      map.current.addLayer({
        id: 'country-fills-click',
        type: 'fill',
        source: COUNTRY_SOURCE_ID,
        'source-layer': 'country_boundaries',
        filter: ['in', 'iso_3166_1', ...codes],
        paint: { 'fill-color': '#000', 'fill-opacity': 0 },
      });

      map.current.on('click', 'country-fills-click', (e) => {
        const feat = e.features?.[0];
        const iso = feat?.properties?.iso_3166_1;
        if (!iso) return;
        const country = countriesData.find((c) => c.code_iso_2 === iso);
        if (country) {
          flyToCountry(country);
          setSelectedCountry(country);
          setSelectedRegion({ type: 'pays', data: country });
        }
      });
      map.current.on('mouseenter', 'country-fills-click', () => {
        map.current.getCanvas().style.cursor = 'pointer';
      });
      map.current.on('mouseleave', 'country-fills-click', () => {
        map.current.getCanvas().style.cursor = '';
      });
    });
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
        pitch: 0,
        bearing: 0,
        duration: 1500,
      });
    }
    setSelectedCountry(null);
    setSelectedRegion(null);
    setExpandedProvinces(new Set());
  };

  const toggleProvince = (provinceId) => {
    setExpandedProvinces((prev) => {
      const next = new Set(prev);
      if (next.has(provinceId)) next.delete(provinceId);
      else next.add(provinceId);
      return next;
    });
  };

  return (
    <div
      className="w-full h-screen flex flex-col bg-background"
      style={{ height: 'calc(100vh - 73px)' }}
    >
      <div ref={mapWrapperRef} className="flex-1 relative">
        <div ref={mapContainer} className="w-full h-full" />

        {loading && (
          <div className="absolute inset-0 z-20 flex flex-col overflow-hidden">
            <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" />
            <div className="absolute inset-0 flex items-center justify-center transition-opacity duration-300">
              <div className="flex flex-col items-center gap-5">
                <RadialSpinner size="medium" color="primary" />
                <span className="text-sm font-medium text-primary animate-pulse">Chargement de la carte...</span>
              </div>
            </div>
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-[92%] max-w-2xl rounded-xl overflow-hidden bg-card/90 border border-darkGray p-5 shadow-xl">
              <div className="skeleton-shimmer-dark h-4 rounded w-1/4 mb-4" />
              <div className="flex gap-6">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} className="flex-1 flex flex-col gap-2">
                    <div className="skeleton-shimmer-dark h-3 rounded w-full" />
                    <div className="skeleton-shimmer-dark h-8 rounded w-14" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

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

        {/* Carte statistiques : réductible par défaut, déplaçable */}
        <div
          ref={statsCardRef}
          className={`absolute z-10 ${statsPosition == null ? 'top-4 left-1/2 -translate-x-1/2' : ''}`}
          style={statsPosition != null ? { left: statsPosition.x, top: statsPosition.y } : undefined}
        >
          <div
            className="bg-card/95 backdrop-blur-sm border border-darkGray rounded-xl shadow-xl overflow-hidden min-w-0"
            onClick={() => !statsExpanded && setStatsExpanded(true)}
          >
            <div
              className={`flex items-center gap-2 px-3 py-1.5 border-b border-darkGray/50 bg-darkGray/20 cursor-grab active:cursor-grabbing select-none ${draggingCard === 'stats' ? 'opacity-90' : ''}`}
              onMouseDown={(e) => { e.stopPropagation(); handleDragStart('stats', e); }}
            >
              <GripVertical className="w-4 h-4 text-gray-500 flex-shrink-0" />
              {selectedCountry && (
                <span className="text-xs text-secondary font-semibold truncate flex-1 min-w-0">
                  {selectedCountry.nom}
                </span>
              )}
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); setStatsExpanded((v) => !v); }}
                className="p-1 rounded hover:bg-darkGray/50 text-gray-400 hover:text-text ml-auto"
                title={statsExpanded ? 'Réduire' : 'Agrandir'}
              >
                {statsExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
              {selectedCountry && (
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); setSelectedCountry(null); }}
                  className="p-1 hover:bg-danger/20 rounded text-gray-400 hover:text-danger"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>
            {statsExpanded ? (
              <div className="px-4 py-3">
                <div className="flex items-center gap-4 flex-wrap">
                  <div className="text-center min-w-[3rem]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide mb-0.5">Pays</div>
                    <div className="text-lg font-bold text-primary">{displayStats.countries}</div>
                  </div>
                  <div className="h-8 w-px bg-darkGray" />
                  <div className="text-center min-w-[3rem]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide mb-0.5">Agents</div>
                    <div className="text-lg font-bold text-secondary">{(displayStats.agents / 1000).toFixed(1)}K</div>
                  </div>
                  <div className="h-8 w-px bg-darkGray" />
                  <div className="text-center min-w-[3rem]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide mb-0.5">Utilisateurs</div>
                    <div className="text-lg font-bold text-text">{(displayStats.users / 1000000).toFixed(2)}M</div>
                  </div>
                  <div className="h-8 w-px bg-darkGray" />
                  <div className="text-center min-w-[3rem]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide mb-0.5">Provinces</div>
                    <div className="text-lg font-bold text-text">{displayStats.provinces}</div>
                  </div>
                  <div className="h-8 w-px bg-darkGray" />
                  <div className="text-center min-w-[3rem]">
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide mb-0.5">Districts</div>
                    <div className="text-lg font-bold text-text">{displayStats.districts}</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-3 px-4 py-2">
                <div className="flex items-center gap-1.5" title="Pays">
                  <GlobeIcon className="w-4 h-4 text-primary" />
                  <span className="text-sm font-bold text-primary">{displayStats.countries}</span>
                </div>
                <div className="w-px h-5 bg-darkGray" />
                <div className="flex items-center gap-1.5" title="Agents">
                  <Users className="w-4 h-4 text-secondary" />
                  <span className="text-sm font-bold text-secondary">{(displayStats.agents / 1000).toFixed(1)}K</span>
                </div>
                <div className="w-px h-5 bg-darkGray" />
                <div className="flex items-center gap-1.5" title="Utilisateurs">
                  <Users className="w-4 h-4 text-text" />
                  <span className="text-sm font-bold text-text">{(displayStats.users / 1000000).toFixed(2)}M</span>
                </div>
                <div className="w-px h-5 bg-darkGray" />
                <div className="flex items-center gap-1.5" title="Provinces">
                  <Building2 className="w-4 h-4 text-text" />
                  <span className="text-sm font-bold text-text">{displayStats.provinces}</span>
                </div>
                <div className="w-px h-5 bg-darkGray" />
                <div className="flex items-center gap-1.5" title="Districts">
                  <MapPinned className="w-4 h-4 text-text" />
                  <span className="text-sm font-bold text-text">{displayStats.districts}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {selectedCountry && (
          <div className="absolute top-16 left-1/2 transform -translate-x-1/2 z-10">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-card/95 backdrop-blur-sm border border-darkGray rounded-lg shadow-lg">
              <GlobeIcon className="w-4 h-4 text-secondary" />
              <span className="text-secondary font-semibold text-sm">{selectedCountry.nom}</span>
              <button
                onClick={() => setSelectedCountry(null)}
                className="ml-1 hover:bg-secondary/30 rounded-full p-0.5 transition-colors"
              >
                <X className="w-3 h-3 text-secondary" />
              </button>
            </div>
          </div>
        )}

        {isPanelOpen && (
          <div
            ref={panelRef}
            className={`absolute z-10 w-96 bg-card/95 backdrop-blur-sm border border-darkGray rounded-xl shadow-2xl overflow-hidden flex flex-col ${panelPosition == null ? 'top-4 right-4' : ''}`}
            style={{
              maxHeight: 'calc(100vh - 100px)',
              ...(panelPosition != null ? { left: panelPosition.x, top: panelPosition.y } : {}),
            }}
          >
            <div
              className="p-3 border-b border-darkGray flex items-center justify-between bg-darkGray/30 cursor-grab active:cursor-grabbing select-none"
              onMouseDown={(e) => { if (e.target.closest('button') == null) handleDragStart('panel', e); }}
            >
              <div className="flex items-center gap-2 min-w-0">
                <GripVertical className="w-4 h-4 text-gray-500 flex-shrink-0" />
                <GlobeIcon className="w-4 h-4 text-primary flex-shrink-0" />
                <h3 className="text-sm font-semibold text-text truncate">Cartographie</h3>
              </div>
              <button
                type="button"
                onClick={() => setIsPanelOpen(false)}
                className="p-1 hover:bg-danger/20 rounded transition-colors flex-shrink-0"
              >
                <X className="w-4 h-4 text-gray-400 hover:text-danger" />
              </button>
            </div>
            <div className="p-3 border-b border-darkGray">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Rechercher un pays..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-background border border-darkGray rounded-lg text-text text-sm placeholder-gray-500 focus:outline-none focus:border-darkGray"
                />
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-2">
              {fetchError && (
                <div className="p-3 mb-2 rounded-lg bg-red-500/10 border border-red-500/30 text-sm text-red-400 space-y-2">
                  <p>{fetchError}</p>
                  <p className="text-xs opacity-90">Vérifiez que le backend est démarré et que <code className="bg-red-500/20 px-1 rounded">VITE_API_URL</code> pointe vers l’API (ex. http://127.0.0.1:8000).</p>
                  <button
                    type="button"
                    onClick={() => fetchLocalisationComplete()}
                    className="text-xs font-medium text-primary hover:underline"
                  >
                    Réessayer
                  </button>
                </div>
              )}
              {loading ? (
                <div className="space-y-2 p-2" aria-label="Chargement">
                  <div className="skeleton-shimmer-dark h-4 w-36 rounded" />
                  {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
                    <div key={i} className="p-3 rounded-lg border border-darkGray/40 flex items-center gap-3">
                      <div className="skeleton-shimmer-dark h-2.5 w-2.5 rounded-full flex-shrink-0" />
                      <div className="flex-1 space-y-2">
                        <div className="skeleton-shimmer-dark h-4 rounded w-32" />
                        <div className="skeleton-shimmer-dark h-3 rounded w-44" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : !selectedCountry ? (
                <>
                  <p className="text-xs text-gray-400 px-2 py-1 mb-2">
                    {filteredCountries.length === 0
                      ? `Aucun pays chargé. Vérifiez `
                      : `${filteredCountries.length} pays — cliquez sur la carte ou sur un pays`}
                  </p>
                  {filteredCountries.length === 0 && !fetchError && (
                    <button
                      type="button"
                      onClick={() => fetchLocalisationComplete()}
                      className="text-xs font-medium text-primary hover:underline mb-2"
                    >
                      Réessayer le chargement
                    </button>
                  )}
                  <div className="space-y-4">
                    {filteredCountriesBySousRegion.map(([sousRegionLabel, countries]) => {
                      const color = getCouleurSousRegion(sousRegionLabel);
                      return (
                        <div key={sousRegionLabel || 'autre'} className="rounded-lg overflow-hidden border border-darkGray/50 bg-background/40">
                          <div
                            className="px-3 py-2 flex items-center gap-2 border-b border-darkGray/40"
                            style={{ borderLeftWidth: 4, borderLeftColor: color }}
                          >
                            <span
                              className="h-2 w-2 rounded-full flex-shrink-0"
                              style={{ backgroundColor: color }}
                            />
                            <span className="text-xs font-semibold text-text uppercase tracking-wide">
                              {sousRegionLabel || 'Autre'}
                            </span>
                            <span className="text-[10px] text-gray-500 ml-auto">
                              {countries.length} pays
                            </span>
                          </div>
                          <div className="p-1.5 space-y-1">
                            {countries.map((country) => {
                              const actif = isActifAutorise(country);
                              return (
                                <div
                                  key={country.id}
                                  onClick={() => flyToCountry(country)}
                                  className={`p-2.5 rounded-md cursor-pointer transition-all border ${
                                    actif
                                      ? 'bg-secondary/20 border-secondary/50 text-text'
                                      : 'bg-primary/10 border-primary/30 hover:bg-primary/20 text-gray-300'
                                  }`}
                                >
                                  <div className="flex items-center justify-between gap-2">
                                    <div className="flex items-center gap-2 flex-1 min-w-0">
                                      <span
                                        className="h-2 w-2 rounded-full flex-shrink-0"
                                        style={{
                                          backgroundColor: actif ? COULEUR_OCCUPE : COULEUR_NON_OCCUPE,
                                          border: `1px solid ${actif ? COULEUR_OCCUPE : 'rgba(0,123,255,0.6)'}`,
                                          opacity: actif ? 1 : 0.8,
                                        }}
                                      />
                                      <div className="min-w-0">
                                        <p className="font-medium text-sm truncate">{country.nom}</p>
                                        <p className="text-[10px] text-gray-500">
                                          {country.nombre_agents ?? 0} agents · {(country.nombre_utilisateurs ?? 0).toLocaleString()} users
                                        </p>
                                      </div>
                                    </div>
                                    <MapPin className="w-3.5 h-3.5 flex-shrink-0 opacity-50" />
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-2 px-2">
                    <span className="text-xs text-gray-400">Provinces / Districts</span>
                    <button
                      onClick={() => {
                        setSelectedCountry(null);
                        setSelectedRegion(null);
                      }}
                      className="text-xs text-primary hover:underline"
                    >
                      Retour aux pays
                    </button>
                  </div>
                  {(selectedCountry.provinces || []).map((prov) => {
                    const actif = isActifAutorise(prov);
                    const expanded = expandedProvinces.has(prov.id);
                    return (
                      <div key={prov.id} className="mb-1">
                        <div
                          onClick={() => {
                            toggleProvince(prov.id);
                            setSelectedRegion({ type: 'province', data: prov });
                          }}
                          className={`p-2.5 rounded-lg cursor-pointer transition-all border flex items-center justify-between ${
                            actif
                              ? 'bg-secondary/20 border-secondary/60 border-l-4 border-l-secondary'
                              : 'bg-primary/10 border-primary/30 hover:bg-primary/20'
                          } ${selectedRegion?.type === 'province' && selectedRegion?.data?.id === prov.id ? 'ring-1 ring-secondary' : ''}`}
                        >
                          <div className="flex items-center gap-2 flex-1 min-w-0">
                            <ChevronRight
                              className={`w-4 h-4 flex-shrink-0 transition-transform ${expanded ? 'rotate-90' : ''}`}
                            />
                            <Building2 className="w-4 h-4 flex-shrink-0 text-gray-400" />
                            <span className="font-medium text-sm truncate">{prov.nom}</span>
                            {actif && (
                              <span className="text-[10px] px-1.5 py-0.5 rounded bg-secondary/40 text-secondary font-semibold">
                                Occupé
                              </span>
                            )}
                          </div>
                        </div>
                        {expanded && (prov.districts || []).length > 0 && (
                          <div className="ml-4 mt-1 space-y-1 border-l border-darkGray pl-2">
                            {(prov.districts || []).map((dist) => {
                              const distActif = isActifAutorise(dist);
                              return (
                                <div
                                  key={dist.id}
                                  onClick={() => setSelectedRegion({ type: 'district', data: dist })}
                                  className={`p-2 rounded cursor-pointer transition-all border ${
                                    distActif
                                      ? 'bg-secondary/15 border-secondary/40 border-l-2 border-l-secondary'
                                      : 'bg-primary/10 border-primary/20 hover:bg-primary/15'
                                  } ${selectedRegion?.type === 'district' && selectedRegion?.data?.id === dist.id ? 'ring-1 ring-secondary' : ''}`}
                                >
                                  <div className="flex items-center gap-2">
                                    <MapPinned className="w-3 h-3 flex-shrink-0 text-gray-400" />
                                    <span className="text-xs font-medium">{dist.nom}</span>
                                    {distActif && (
                                      <span className="text-[10px] px-1 rounded bg-secondary/30 text-secondary font-medium">
                                        Occupé
                                      </span>
                                    )}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </>
              )}
            </div>

            {selectedRegion?.data && (
              <div className="border-t border-darkGray p-3 bg-background/80 max-h-64 overflow-y-auto">
                <h4 className="text-xs font-semibold text-gray-400 uppercase mb-2">
                  Détails — {selectedRegion.type === 'pays' ? 'Pays' : selectedRegion.type === 'province' ? 'Province' : selectedRegion.type === 'district' ? 'District' : 'Quartier'}
                </h4>
                <DetailRegion region={selectedRegion.data} type={selectedRegion.type} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function DetailRegion({ region, type }) {
  if (!region) return null;
  const actif = isActifAutorise(region);
  const nom = region.nom || region.nom_anglais || '—';
  const stats = region.statistiques || {};
  const meta = region.metadonnees || {};

  return (
    <div className="space-y-3 text-sm">
      <div className="flex items-center justify-between gap-2">
        <span className="text-text font-semibold truncate">{nom}</span>
        <span
          className={`text-xs px-2 py-0.5 rounded font-medium flex-shrink-0 ${
            actif ? 'bg-secondary/25 text-secondary border border-secondary/50' : 'bg-primary/15 text-primary border border-primary/40'
          }`}
        >
          {actif ? 'Occupé' : 'Non occupé'}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-x-3 gap-y-2 text-xs">
        <div className="bg-card/50 rounded px-2 py-1.5">
          <span className="text-gray-400 block text-[10px] uppercase">Agents</span>
          <span className="font-semibold text-text">{(region.nombre_agents ?? 0).toLocaleString()}</span>
        </div>
        <div className="bg-card/50 rounded px-2 py-1.5">
          <span className="text-gray-400 block text-[10px] uppercase">Utilisateurs</span>
          <span className="font-semibold text-text">{(region.nombre_utilisateurs ?? 0).toLocaleString()}</span>
        </div>
        <div className="bg-card/50 rounded px-2 py-1.5">
          <span className="text-gray-400 block text-[10px] uppercase">Agents actifs</span>
          <span className="font-semibold text-secondary">{(region.nombre_agents_actifs ?? 0).toLocaleString()}</span>
        </div>
        <div className="bg-card/50 rounded px-2 py-1.5">
          <span className="text-gray-400 block text-[10px] uppercase">Users actifs</span>
          <span className="font-semibold text-secondary">{(region.nombre_utilisateurs_actifs ?? 0).toLocaleString()}</span>
        </div>
      </div>
      {Object.keys(stats).length > 0 && (
        <div className="pt-2 border-t border-darkGray">
          <div className="text-[10px] text-gray-400 uppercase font-semibold mb-1.5">Statistiques</div>
          <div className="flex flex-wrap gap-1.5">
            {Object.entries(stats).map(([k, v]) => (
              <span key={k} className="text-xs bg-darkGray/50 px-2 py-0.5 rounded">
                {k.replace(/_/g, ' ')}: {String(v)}
              </span>
            ))}
          </div>
        </div>
      )}
      {type === 'pays' && (meta.capitale || meta.population != null) && (
        <div className="text-xs text-gray-400 pt-1 border-t border-darkGray/50">
          {meta.capitale && <span>Capitale: <strong className="text-text">{meta.capitale}</strong></span>}
          {meta.population != null && (
            <span className={meta.capitale ? ' ml-2' : ''}>Pop. {Number(meta.population).toLocaleString()}</span>
          )}
        </div>
      )}
      {(type === 'province' || type === 'district') && meta.chef_lieu && (
        <div className="text-xs text-gray-400 pt-1 border-t border-darkGray/50">
          Chef-lieu: <strong className="text-text">{meta.chef_lieu}</strong>
        </div>
      )}
    </div>
  );
}

export default CartographieReseau;
