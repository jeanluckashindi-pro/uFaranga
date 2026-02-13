import { useState, useRef } from 'react';
import { Toast } from 'primereact/toast';
import {
  ComposedChart, Line, Bar, Area, BarChart, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import {
  AlertOctagon, TrendingUp, TrendingDown, Eye, Ban,
  RefreshCw, Download, Brain, Target, Users, DollarSign,
  Clock, MapPin, Smartphone, CreditCard, Activity
} from 'lucide-react';

function Fraude() {
  const toast = useRef(null);
  const [timeRange, setTimeRange] = useState('24h');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [filterRisk, setFilterRisk] = useState('all');

  const fraudeMetrics = {
    fraudeDetectee: { value: 342, change: -18.5, trend: 'down', montant: 45600000 },
    tauxFraude: { value: 0.87, change: -12.3, trend: 'down', target: 0.5 },
    casEnCours: { value: 23, change: 5.2, trend: 'up' },
    precisionIA: { value: 96.8, change: 2.1, trend: 'up', falsePositive: 3.2 }
  };

  const fraudeTrends = Array.from({ length: 30 }, (_, i) => ({
    jour: `J-${30 - i}`,
    detectees: Math.floor(Math.random() * 50) + 20,
    bloquees: Math.floor(Math.random() * 45) + 18,
    montant: Math.floor(Math.random() * 10000000) + 5000000,
    taux: (Math.random() * 1.5) + 0.3
  }));

  const fraudePatterns = [
    { pattern: 'Transactions Multiples', score: 95, occurrences: 156 },
    { pattern: 'Montants Suspects', score: 88, occurrences: 234 },
    { pattern: 'Géolocalisation', score: 82, occurrences: 89 },
    { pattern: 'Horaires Inhabituels', score: 76, occurrences: 178 },
    { pattern: 'Nouveaux Appareils', score: 71, occurrences: 123 },
    { pattern: 'Comportement Anormal', score: 68, occurrences: 201 }
  ];

  const riskDistribution = [
    { niveau: 'Critique', agents: 12, clients: 34, montant: 15600000 },
    { niveau: 'Élevé', agents: 45, clients: 123, montant: 23400000 },
    { niveau: 'Moyen', agents: 89, clients: 267, montant: 8900000 },
    { niveau: 'Faible', agents: 234, clients: 1456, montant: 2300000 }
  ];

  const suspiciousTransactions = [
    { id: 'TRX-8901', agent: 'Agent-234', client: 'Client-5678', montant: 2500000, risque: 'CRITICAL', raison: 'Montant inhabituel + Géolocalisation', temps: '3 min', statut: 'En analyse' },
    { id: 'TRX-8902', agent: 'Agent-567', client: 'Client-9012', montant: 1800000, risque: 'HIGH', raison: 'Transactions multiples rapides', temps: '8 min', statut: 'Bloqué' },
    { id: 'TRX-8903', agent: 'Agent-123', client: 'Client-3456', montant: 950000, risque: 'HIGH', raison: 'Nouvel appareil + Horaire suspect', temps: '12 min', statut: 'En analyse' },
    { id: 'TRX-8904', agent: 'Agent-890', client: 'Client-7890', montant: 3200000, risque: 'CRITICAL', raison: 'Pattern de fraude connu', temps: '15 min', statut: 'Bloqué' },
    { id: 'TRX-8905', agent: 'Agent-456', client: 'Client-2345', montant: 670000, risque: 'MEDIUM', raison: 'Comportement inhabituel', temps: '18 min', statut: 'Validé' }
  ];

  const mlInsights = [
    { categorie: 'Précision', score: 96.8 },
    { categorie: 'Rappel', score: 94.2 },
    { categorie: 'F1-Score', score: 95.5 },
    { categorie: 'Spécificité', score: 97.1 },
    { categorie: 'ROC-AUC', score: 98.3 }
  ];

  const FraudeKPICard = ({ title, value, change, trend, icon: Icon, subtitle, unit = '', level }) => {
    const isPositive = trend === 'down' ? change < 0 : change > 0;
    
    const getLevelColor = () => {
      if (level === 'CRITICAL') return 'text-red-500 bg-red-500/20';
      if (level === 'HIGH') return 'text-orange-500 bg-orange-500/20';
      return isPositive ? 'text-green-500 bg-green-500/20' : 'text-red-500 bg-red-500/20';
    };

    return (
      <div className="border border-darkGray bg-card rounded-lg p-5 hover:border-primary/50 transition-all">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <p className="text-xs text-gray-400 uppercase font-semibold tracking-wide mb-1">{title}</p>
            <p className="text-3xl font-bold text-text mb-1">{value}{unit}</p>
            {subtitle && <p className="text-xs text-gray-400">{subtitle}</p>}
          </div>
          <div className={`p-3 rounded-lg ${getLevelColor()}`}>
            <Icon className="w-6 h-6" />
          </div>
        </div>
        
        {change !== undefined && (
          <div className="flex items-center gap-2">
            {isPositive ? <TrendingUp className="w-4 h-4 text-green-500" /> : <TrendingDown className="w-4 h-4 text-red-500" />}
            <span className={`text-sm font-semibold ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
              {Math.abs(change)}%
            </span>
            <span className="text-xs text-gray-400">vs hier</span>
          </div>
        )}
      </div>
    );
  };

  const getRiskBadge = (risk) => {
    const colors = {
      CRITICAL: 'bg-red-500/20 text-red-500 border-red-500/50',
      HIGH: 'bg-orange-500/20 text-orange-500 border-orange-500/50',
      MEDIUM: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
      LOW: 'bg-green-500/20 text-green-500 border-green-500/50'
    };
    return colors[risk] || colors.LOW;
  };

  const getStatusBadge = (status) => {
    const colors = {
      'Bloqué': 'bg-red-500/20 text-red-500',
      'En analyse': 'bg-orange-500/20 text-orange-500',
      'Validé': 'bg-green-500/20 text-green-500'
    };
    return colors[status] || 'bg-gray-500/20 text-gray-500';
  };

  return (
    <div className="p-4 md:p-6 space-y-6 w-full max-w-full overflow-x-hidden">
      <Toast ref={toast} />

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-4xl font-anton uppercase text-text tracking-tight">
            Fraud Detection Intelligence
          </h1>
          <p className="text-gray-400 mt-2 text-sm md:text-base">
            Détection et prévention par IA en temps réel
          </p>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 bg-card border border-darkGray rounded-lg text-text text-sm"
          >
            <option value="1h">Dernière heure</option>
            <option value="24h">24 heures</option>
            <option value="7d">7 jours</option>
            <option value="30d">30 jours</option>
          </select>
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`p-2 rounded-lg ${autoRefresh ? 'bg-primary text-white' : 'bg-card border border-darkGray'}`}
          >
            <RefreshCw className={`w-5 h-5 ${autoRefresh ? 'animate-spin' : ''}`} />
          </button>
          <button className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg font-semibold">
            <Download size={18} />
            Exporter
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <FraudeKPICard
          title="Fraudes Détectées"
          value={fraudeMetrics.fraudeDetectee.value}
          change={fraudeMetrics.fraudeDetectee.change}
          trend={fraudeMetrics.fraudeDetectee.trend}
          icon={AlertOctagon}
          subtitle={`Montant: ${(fraudeMetrics.fraudeDetectee.montant / 1000000).toFixed(1)}M BIF`}
          level="HIGH"
        />
        <FraudeKPICard
          title="Taux de Fraude"
          value={fraudeMetrics.tauxFraude.value}
          change={fraudeMetrics.tauxFraude.change}
          trend={fraudeMetrics.tauxFraude.trend}
          icon={Target}
          unit="%"
          subtitle={`Objectif: ${fraudeMetrics.tauxFraude.target}%`}
        />
        <FraudeKPICard
          title="Cas en Cours"
          value={fraudeMetrics.casEnCours.value}
          change={fraudeMetrics.casEnCours.change}
          trend={fraudeMetrics.casEnCours.trend}
          icon={Eye}
          subtitle="Analyse en temps réel"
          level="CRITICAL"
        />
        <FraudeKPICard
          title="Précision IA"
          value={fraudeMetrics.precisionIA.value}
          change={fraudeMetrics.precisionIA.change}
          trend={fraudeMetrics.precisionIA.trend}
          icon={Brain}
          unit="%"
          subtitle={`Faux positifs: ${fraudeMetrics.precisionIA.falsePositive}%`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
            <Activity className="w-5 h-5 text-danger" />
            Évolution des Fraudes (30 jours)
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <ComposedChart data={fraudeTrends}>
              <defs>
                <linearGradient id="colorMontant" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#DC3545" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#DC3545" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#343A40" />
              <XAxis dataKey="jour" stroke="#9ca3af" style={{ fontSize: '11px' }} />
              <YAxis yAxisId="left" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#181F27',
                  border: '1px solid #343A40',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Area
                yAxisId="right"
                type="monotone"
                dataKey="montant"
                stroke="#DC3545"
                fill="url(#colorMontant)"
                name="Montant (BIF)"
              />
              <Bar yAxisId="left" dataKey="detectees" fill="#F58424" name="Détectées" />
              <Bar yAxisId="left" dataKey="bloquees" fill="#28A745" name="Bloquées" />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="taux"
                stroke="#007BFF"
                strokeWidth={3}
                name="Taux (%)"
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
            <Brain className="w-5 h-5 text-primary" />
            Performance du Modèle IA
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={mlInsights}>
              <PolarGrid stroke="#343A40" />
              <PolarAngleAxis dataKey="categorie" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#9ca3af" />
              <Radar
                name="Score"
                dataKey="score"
                stroke="#007BFF"
                fill="#007BFF"
                fillOpacity={0.6}
              />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-400">Modèle entraîné sur 2.4M transactions</p>
            <p className="text-xs text-gray-500 mt-1">Dernière mise à jour: Il y a 2h</p>
          </div>
        </div>
      </div>

      <div className="border border-darkGray bg-card rounded-lg p-6">
        <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
          <Target className="w-5 h-5 text-secondary" />
          Patterns de Fraude Détectés
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {fraudePatterns.map((pattern, index) => (
            <div key={index} className="bg-darkGray/30 rounded-lg p-4 hover:bg-darkGray/50 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <p className="text-text font-semibold mb-1">{pattern.pattern}</p>
                  <p className="text-xs text-gray-400">{pattern.occurrences} occurrences</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-primary">{pattern.score}</p>
                  <p className="text-xs text-gray-400">Score</p>
                </div>
              </div>
              <div className="h-2 bg-darkGray rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all ${
                    pattern.score >= 90 ? 'bg-red-500' : pattern.score >= 75 ? 'bg-orange-500' : 'bg-yellow-500'
                  }`}
                  style={{ width: `${pattern.score}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="border border-darkGray bg-card rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-anton uppercase text-text flex items-center gap-2">
            <AlertOctagon className="w-5 h-5 text-danger" />
            Transactions Suspectes
          </h2>
          <select
            value={filterRisk}
            onChange={(e) => setFilterRisk(e.target.value)}
            className="px-3 py-1.5 bg-darkGray border border-darkGray rounded-lg text-text text-sm"
          >
            <option value="all">Tous les risques</option>
            <option value="critical">Critiques</option>
            <option value="high">Élevés</option>
          </select>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-darkGray">
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Transaction</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Agent</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Client</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Montant</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Risque</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Raison</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Statut</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {suspiciousTransactions.map((trx) => (
                <tr key={trx.id} className="border-b border-darkGray/50 hover:bg-darkGray/30 transition-colors">
                  <td className="py-3 px-4 text-sm text-text font-mono font-semibold">{trx.id}</td>
                  <td className="py-3 px-4 text-sm text-gray-400">{trx.agent}</td>
                  <td className="py-3 px-4 text-sm text-gray-400">{trx.client}</td>
                  <td className="py-3 px-4 text-sm text-text font-semibold">{(trx.montant / 1000).toFixed(0)}K</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold border ${getRiskBadge(trx.risque)}`}>
                      {trx.risque}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-xs text-gray-400 max-w-xs truncate">{trx.raison}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBadge(trx.statut)}`}>
                      {trx.statut}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-2">
                      <button className="text-primary hover:text-primary/80 text-sm">
                        <Eye size={16} />
                      </button>
                      <button className="text-danger hover:text-danger/80 text-sm">
                        <Ban size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="border border-darkGray bg-card rounded-lg p-6">
        <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
          <Users className="w-5 h-5 text-primary" />
          Distribution du Risque
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={riskDistribution}>
            <CartesianGrid strokeDasharray="3 3" stroke="#343A40" />
            <XAxis dataKey="niveau" stroke="#9ca3af" style={{ fontSize: '12px' }} />
            <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#181F27',
                border: '1px solid #343A40',
                borderRadius: '8px'
              }}
            />
            <Legend />
            <Bar dataKey="agents" fill="#007BFF" name="Agents" />
            <Bar dataKey="clients" fill="#F58424" name="Clients" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Fraude;
