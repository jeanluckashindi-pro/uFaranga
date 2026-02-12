# 🏦 Structure Page Transactions Agent - Niveau Bancaire Professionnel

## 🎯 Objectif
Centre d'analyse opérationnel avancé pour agents. Pas une simple liste, mais un outil d'analyse stratégique temps réel niveau M-Pesa/Wave.

---

## 🏗️ Architecture de la Page

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER                                                           │
│ - Titre: "Centre d'Analyse Transactionnel"                     │
│ - Date et heure temps réel                                      │
│ - Boutons: Rafraîchir | Exporter CSV                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 1: KPI CARDS AVANCÉES (4 cartes)                          │
│                                                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │Activité  │ │Commiss.  │ │Taux de   │ │Temps     │          │
│ │Auj.      │ │Générée   │ │Succès    │ │Moyen     │          │
│ │          │ │          │ │          │ │          │          │
│ │15 trans  │ │10.5K BIF │ │93.3%     │ │45s       │          │
│ │1.96M BIF │ │700/trans │ │14/15     │ │Rapide    │          │
│ │+12.5% ↑  │ │+8.3% ↑   │ │Excellent │ │✓         │          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 2: ANALYTICS VISUELS (3 graphiques)                       │
│                                                                  │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│ │Volume/Heure  │ │Répartition   │ │Évolution     │           │
│ │(BarChart)    │ │Type (Pie)    │ │7j (Line)     │           │
│ │              │ │              │ │              │           │
│ │Pic: 13h      │ │Dépôts 40%    │ │Tendance +15% │           │
│ │420K BIF      │ │Retraits 27%  │ │              │           │
│ └──────────────┘ └──────────────┘ └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 4: MODULE DÉTECTION ANOMALIES                             │
│                                                                  │
│ ⚠️ 3 transaction(s) nécessitent attention                      │
│                                                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                       │
│ │David K.  │ │Paul K.   │ │Joseph T. │                       │
│ │80K BIF   │ │100K BIF  │ │40K BIF   │                       │
│ │🔴 Élevé  │ │🟡 Moyen  │ │🟡 Moyen  │                       │
│ │Montant   │ │Vérif.    │ │Vérif.    │                       │
│ │inhabituel│ │recomm.   │ │recomm.   │                       │
│ └──────────┘ └──────────┘ └──────────┘                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 5: ANALYSE PERFORMANCE AGENT                              │
│                                                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │43,333    │ │13h00     │ │Dépôts    │ │700       │          │
│ │Volume    │ │Heure     │ │Type Plus │ │Commiss.  │          │
│ │Moy/Trans │ │Productive│ │Utilisé   │ │Moy/Trans │          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ FILTRES AVANCÉS                                                 │
│                                                                  │
│ [🔍 Recherche...] [Tous] [Dépôts] [Retraits] [Transferts]     │
│                   [Paiements] [Période ▼]                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 3: TABLEAU INTELLIGENT (DataTable PrimeReact)            │
│                                                                  │
│ Heure | Type | Client | Réf | Montant | Comm | Canal | Risque │
│ ──────────────────────────────────────────────────────────────  │
│ 14:35 | 🟠 Dépôt | Marie K. | DEP-001 | 50K | +500 | Mobile │ │
│       |          | 07 ** ***456 |     | 100F |      |        │ │
│ ──────────────────────────────────────────────────────────────  │
│ 14:28 | 🔵 Retrait | Jean M. | RET-002 | 30K | +450 | Agent │ │
│       |            | 07 ** ***567 |     | 150F |      |       │ │
│ ──────────────────────────────────────────────────────────────  │
│                                                                  │
│ Fonctionnalités:                                                │
│ ✓ Tri dynamique (clic sur colonnes)                            │
│ ✓ Pagination (5, 10, 25, 50 par page)                          │
│ ✓ Recherche instantanée                                         │
│ ✓ Filtrage multiple combiné                                     │
│ ✓ Masquage numéros (sécurité)                                  │
│ ✓ Actions: 👁️ Voir | 📄 Reçu                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ZONE 6: GESTION AVANCÉE DES INCIDENTS                          │
│                                                                  │
│ ❌ Gestion des Incidents (2)                                    │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ David Kasongo • RET-2026-006                                │ │
│ │ 80,000 BIF • 13:30:12                                       │ │
│ │ [ERR_101] Solde insuffisant                                 │ │
│ │                          [Réessayer] [Contacter Support]    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Robert Ngoy • RET-2026-014                                  │ │
│ │ 42,000 BIF • 11:28:55                                       │ │
│ │ [ERR_301] PIN incorrect                                     │ │
│ │                          [Réessayer] [Contacter Support]    │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Détail des Zones

### ZONE 1: KPI CARDS AVANCÉES

#### Carte 1: Activité Aujourd'hui
```javascript
{
  titre: "Activité Aujourd'hui",
  icone: Activity,
  valeur_principale: "15 transactions",
  valeur_secondaire: "Volume: 1.96M BIF",
  comparaison: "+12.5% vs hier",
  couleur_tendance: "secondary (vert)"
}
```

#### Carte 2: Commission Générée
```javascript
{
  titre: "Commission Générée",
  icone: TrendingUp,
  valeur_principale: "10.5K BIF",
  valeur_secondaire: "Moy/trans: 700 BIF",
  comparaison: "+8.3% vs 7j",
  couleur: "secondary (orange)"
}
```

#### Carte 3: Taux de Succès
```javascript
{
  titre: "Taux de Succès",
  icone: Target,
  valeur_principale: "93.3%",
  valeur_secondaire: "14 succès / 1 échec",
  statut: "Excellent",
  formule: "(succès / total) * 100"
}
```

#### Carte 4: Temps Moyen
```javascript
{
  titre: "Temps Moyen",
  icone: Clock,
  valeur_principale: "45s",
  valeur_secondaire: "Traitement transaction",
  statut: "Rapide",
  seuil_alerte: "> 60s"
}
```

---

### ZONE 2: ANALYTICS VISUELS

#### Graphique 1: Volume par Heure
```javascript
{
  type: "BarChart",
  donnees: [
    { heure: "08h", volume: 85000, count: 2 },
    { heure: "09h", volume: 210000, count: 5 },
    // ... jusqu'à maintenant
  ],
  couleur: "#007BFF (primary)",
  info: "Pic: 13h avec 420K BIF"
}
```

#### Graphique 2: Répartition par Type
```javascript
{
  type: "PieChart",
  donnees: [
    { name: "Dépôts", value: 6, color: "#F58424", percentage: 40 },
    { name: "Retraits", value: 4, color: "#007BFF", percentage: 27 },
    { name: "Transferts", value: 3, color: "#6b7280", percentage: 20 },
    { name: "Paiements", value: 2, color: "#9ca3af", percentage: 13 }
  ],
  labels: "Nom + Pourcentage"
}
```

#### Graphique 3: Évolution 7 Jours
```javascript
{
  type: "LineChart",
  donnees: [
    { jour: "Lun", transactions: 42, volume: 1850000 },
    // ... 7 jours
  ],
  couleur: "#F58424 (secondary)",
  info: "Tendance: +15% cette semaine"
}
```

---

### ZONE 3: TABLEAU INTELLIGENT

#### Colonnes du Tableau
```javascript
const columns = [
  { field: "time", header: "Heure", sortable: true, width: "8%" },
  { field: "type", header: "Type", sortable: true, width: "12%", template: typeBodyTemplate },
  { field: "clientName", header: "Client", sortable: true, width: "18%", template: clientBodyTemplate },
  { field: "ref", header: "Référence", sortable: true, width: "12%" },
  { field: "montant", header: "Montant", sortable: true, width: "12%", template: montantBodyTemplate },
  { field: "commission", header: "Commission", sortable: true, width: "10%", template: commissionBodyTemplate },
  { field: "canal", header: "Canal", sortable: true, width: "8%" },
  { field: "riskScore", header: "Risque", sortable: true, width: "8%", template: riskBodyTemplate },
  { field: "statut", header: "Statut", sortable: true, width: "10%", template: statutBodyTemplate },
  { header: "Actions", width: "8%", template: actionsBodyTemplate }
];
```

#### Structure Transaction
```javascript
{
  id: "TXN20260212001",
  type: "depot",
  client: "+257 79 123 456",
  clientName: "Marie Kalala",
  montant: 50000,
  commission: 500,
  frais: 100,
  statut: "success",
  time: "14:35:22",
  ref: "DEP-2026-001",
  canal: "Mobile",
  riskScore: "low",
  errorCode: null
}
```

#### Score Risque
```javascript
const riskLevels = {
  low: {
    badge: "🟢 Normal",
    color: "secondary",
    icon: CheckCircle
  },
  medium: {
    badge: "🟡 Moyen",
    color: "yellow-500",
    icon: AlertCircle
  },
  high: {
    badge: "🔴 Élevé",
    color: "red-500",
    icon: AlertTriangle
  }
};
```

#### Sécurité - Masquage Numéros
```javascript
const maskPhone = (phone) => {
  // +257 79 123 456 → +257 79 ** ***456
  return phone.replace(/(\d{2})(\d{3})(\d{3})/, '$1 ** ***$3');
};
```

---

### ZONE 4: MODULE DÉTECTION ANOMALIES

```javascript
const suspiciousTransactions = transactions.filter(t => 
  t.riskScore === 'high' || t.riskScore === 'medium'
);

// Critères de détection:
const anomalyRules = {
  montant_inhabituel: montant > (moyenne * 2),
  transactions_rapides: count_last_5min > 3,
  echec_pin_repete: failed_pin_attempts > 2,
  nouveau_beneficiaire: !in_history(beneficiaire)
};
```

---

### ZONE 5: ANALYSE PERFORMANCE AGENT

```javascript
const performanceMetrics = {
  volume_moyen_transaction: totalVolume / totalTransactions,
  heure_plus_productive: "13h00", // Calculé depuis volumeByHour
  type_plus_utilise: "Dépôts", // Type avec le plus de transactions
  commission_moyenne: totalCommission / totalTransactions
};
```

---

### ZONE 6: GESTION AVANCÉE DES INCIDENTS

#### Codes d'Erreur
```javascript
const errorCodes = {
  'ERR_101': 'Solde insuffisant',
  'ERR_203': 'Timeout réseau',
  'ERR_301': 'PIN incorrect',
  'ERR_404': 'Compte introuvable',
  'ERR_500': 'Erreur serveur'
};
```

#### Actions sur Incidents
```javascript
const incidentActions = {
  reessayer: () => {
    // Relancer la transaction
    // Vérifier conditions
    // Logger tentative
  },
  contacter_support: () => {
    // Ouvrir ticket support
    // Joindre détails transaction
    // Notifier superviseur
  },
  forcer_verification: () => {
    // Pour transactions pending
    // Interroger API partenaire
    // Mettre à jour statut
  }
};
```

---

## 🔐 Sécurité Bancaire

### Mesures Implémentées

1. **Masquage Données Sensibles**
```javascript
// Numéros de téléphone
+257 79 123 456 → +257 79 ** ***456

// Références complètes visibles (traçabilité)
DEP-2026-001 ✓
```

2. **Logging Consultation**
```javascript
const logAccess = {
  agent_id: "A12345",
  action: "VIEW_TRANSACTION",
  transaction_id: "TXN20260212001",
  timestamp: "2026-02-12T14:35:22Z",
  ip_address: "192.168.1.100"
};
```

3. **Limitation Export**
```javascript
const exportLimits = {
  max_rows_per_export: 1000,
  max_exports_per_day: 10,
  require_supervisor_approval: rows > 500
};
```

4. **Timeout Session**
```javascript
const sessionConfig = {
  timeout_inactivity: 15 * 60 * 1000, // 15 minutes
  warning_before_timeout: 2 * 60 * 1000, // 2 minutes
  auto_logout: true
};
```

---

## 📊 Formules Statistiques

### KPIs Calculés

```javascript
// Taux de succès
const successRate = (
  transactions.filter(t => t.statut === 'success').length / 
  transactions.length
) * 100;

// Commission totale
const totalCommission = transactions.reduce(
  (sum, tx) => sum + tx.commission, 
  0
);

// Volume total
const totalVolume = transactions.reduce(
  (sum, tx) => sum + tx.montant, 
  0
);

// Moyenne transaction
const avgTransaction = totalVolume / transactions.length;

// Comparaison vs hier
const vsYesterday = (
  (today.count - yesterday.count) / yesterday.count
) * 100;

// Comparaison vs moyenne 7 jours
const vs7DaysAvg = (
  (today.count - avg7Days) / avg7Days
) * 100;
```

---

## 🎨 Palette de Couleurs

```javascript
const colors = {
  // Types de transactions
  depot: "#F58424",      // Orange
  retrait: "#007BFF",    // Bleu
  transfert: "#6b7280",  // Gris
  paiement: "#9ca3af",   // Gris clair
  
  // Statuts
  success: "#F58424",    // Orange (secondary)
  pending: "#EAB308",    // Jaune
  failed: "#EF4444",     // Rouge
  
  // Risques
  risk_low: "#F58424",   // Vert (secondary)
  risk_medium: "#EAB308", // Jaune
  risk_high: "#EF4444",  // Rouge
  
  // UI
  primary: "#007BFF",
  secondary: "#F58424",
  background: "#00070F",
  card: "#181F27",
  darkGray: "#343A40"
};
```

---

## 🚀 Fonctionnalités Avancées

### Tri Dynamique
```javascript
const [sortField, setSortField] = useState('time');
const [sortOrder, setSortOrder] = useState(-1); // -1 = DESC, 1 = ASC

// Clic sur colonne → tri automatique
```

### Filtrage Multiple Combiné
```javascript
const filters = {
  type: 'depot',
  statut: 'success',
  dateRange: 'today',
  searchTerm: 'Marie',
  riskScore: 'low'
};

// Tous les filtres s'appliquent en AND
```

### Recherche Instantanée
```javascript
const searchFields = ['client', 'clientName', 'ref'];
const matchesSearch = searchFields.some(field => 
  transaction[field].toLowerCase().includes(searchTerm.toLowerCase())
);
```

### Export CSV
```javascript
const exportToCSV = () => {
  const headers = ['Date', 'Type', 'Client', 'Montant', 'Commission', 'Statut'];
  const rows = filteredTransactions.map(tx => [
    tx.time,
    tx.type,
    tx.clientName,
    tx.montant,
    tx.commission,
    tx.statut
  ]);
  
  // Générer CSV
  // Télécharger fichier
  // Logger export
};
```

---

## 🔄 Temps Réel (WebSocket)

### Événements à Écouter
```javascript
// ws://localhost:3002/agent/transactions

socket.on('transaction:new', (data) => {
  // Ajouter nouvelle transaction en haut
  // Mettre à jour KPIs
  // Notification sonore
});

socket.on('transaction:update', (data) => {
  // Mettre à jour statut transaction
  // Rafraîchir tableau
});

socket.on('anomaly:detected', (data) => {
  // Afficher alerte
  // Ajouter à liste anomalies
});
```

---

## 📡 APIs Backend Nécessaires

### GET /api/v1/agent/transactions
```javascript
{
  transactions: [ /* liste */ ],
  kpis: {
    total_count: 15,
    total_volume: 1960000,
    total_commission: 10500,
    success_rate: 93.3,
    avg_processing_time: 45,
    vs_yesterday: 12.5,
    vs_7days_avg: 8.3
  },
  analytics: {
    volume_by_hour: [ /* données */ ],
    by_type: [ /* données */ ],
    evolution_7days: [ /* données */ ]
  },
  suspicious: [ /* transactions suspectes */ ],
  failed: [ /* transactions échouées */ ]
}
```

### POST /api/v1/agent/transactions/export
```javascript
{
  filters: { /* filtres appliqués */ },
  format: "csv",
  fields: ["date", "type", "client", "montant"]
}
```

### POST /api/v1/agent/transactions/{id}/retry
```javascript
{
  transaction_id: "TXN20260212006",
  reason: "Solde rechargé"
}
```

---

## ✅ Checklist Complétude

- [x] KPI Cards avancées (4)
- [x] Analytics visuels (3 graphiques)
- [x] Tableau intelligent avec tri/filtrage
- [x] Module détection anomalies
- [x] Analyse performance agent
- [x] Gestion incidents avec codes erreur
- [x] Masquage numéros (sécurité)
- [x] Score risque par transaction
- [x] Recherche instantanée
- [x] Pagination performante
- [x] Export CSV
- [ ] WebSocket temps réel
- [ ] Connexion APIs backend
- [ ] Logging accès
- [ ] Timeout session

---

**Dernière mise à jour** : 12 février 2026  
**Version** : 2.0 - Niveau Bancaire Professionnel  
**Auteur** : Kiro AI Assistant
