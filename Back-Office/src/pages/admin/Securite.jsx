import { useState, useRef } from 'react';
import { Toast } from 'primereact/toast';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  Shield, AlertTriangle, Lock, Unlock, Eye, EyeOff,
  Activity, TrendingUp, TrendingDown, CheckCircle, XCircle,
  RefreshCw, Download, Filter, Search, Globe, Server
} from 'lucide-react';

function Securite() {
  const toast = useRef(null);
  const [timeRange, setTimeRange] = useState('24h');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [filterLevel, setFilterLevel] = useState('all');

  const securityMetrics = {
    threatLevel: { value: 'MEDIUM', score: 65, change: -12.3, trend: 'down' },
    blockedAttacks: { value: 1247, change: 8.5, trend: 'up' },
    activeThreats: { value: 23, change: -15.2, trend: 'down' },
    securityScore: { value: 94.7, change: 2.1, trend: 'up', target: 98 }
  };

  const threatDistribution = [
    { name: 'Brute Force', value: 342, color: '#DC3545' },
    { name: 'SQL Injection', value: 156, color: '#F58424' },
    { name: 'XSS', value: 89, color: '#FFC107' },
    { name: 'DDoS', value: 234, color: '#007BFF' },
    { name: 'Phishing', value: 178, color: '#28A745' },
    { name: 'Autres', value: 248, color: '#6C757D' }
  ];

  const securityEvents = Array.from({ length: 24 }, (_, i) => ({
    heure: `${i}h`,
    menaces: Math.floor(Math.random() * 50) + 10,
    bloquees: Math.floor(Math.random() * 45) + 8,
    critiques: Math.floor(Math.random() * 5),
    score: 85 + Math.floor(Math.random() * 15)
  }));

  const recentThreats = [
    { id: 1, type: 'Brute Force', ip: '192.168.1.45', pays: 'Nigeria', severite: 'HIGH', statut: 'Bloqué', temps: '2 min' },
    { id: 2, type: 'SQL Injection', ip: '10.0.0.123', pays: 'Russie', severite: 'CRITICAL', statut: 'Bloqué', temps: '5 min' },
    { id: 3, type: 'DDoS', ip: '172.16.0.89', pays: 'Chine', severite: 'HIGH', statut: 'En cours', temps: '8 min' },
    { id: 4, type: 'XSS', ip: '192.168.2.67', pays: 'Brésil', severite: 'MEDIUM', statut: 'Analysé', temps: '12 min' },
    { id: 5, type: 'Phishing', ip: '10.1.1.234', pays: 'Inde', severite: 'LOW', statut: 'Bloqué', temps: '15 min' }
  ];

  const firewallRules = [
    { id: 1, nom: 'Block Suspicious IPs', type: 'IP Blacklist', actif: true, hits: 1247 },
    { id: 2, nom: 'Rate Limiting API', type: 'Rate Limit', actif: true, hits: 892 },
    { id: 3, nom: 'SQL Injection Filter', type: 'WAF', actif: true, hits: 456 },
    { id: 4, nom: 'Geographic Blocking', type: 'Geo-Filter', actif: false, hits: 0 },
    { id: 5, nom: 'Bot Detection', type: 'Anti-Bot', actif: true, hits: 2341 }
  ];

  const SecurityKPICard = ({ title, value, change, trend, icon: Icon, subtitle, level }) => {
    const isPositive = trend === 'down' ? change < 0 : change > 0;
    
    const getLevelColor = () => {
      if (level === 'CRITICAL') return 'text-red-500 bg-red-500/20';
      if (level === 'HIGH') return 'text-orange-500 bg-orange-500/20';
      if (level === 'MEDIUM') return 'text-yellow-500 bg-yellow-500/20';
      if (level === 'LOW') return 'text-green-500 bg-green-500/20';
      return isPositive ? 'text-green-500 bg-green-500/20' : 'text-red-500 bg-red-500/20';
    };

    return (
      <div className="border border-darkGray bg-card rounded-lg p-5 hover:border-primary/50 transition-all">
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <p className="text-xs text-gray-400 uppercase font-semibold tracking-wide mb-1">{title}</p>
            <p className="text-3xl font-bold text-text mb-1">{value}</p>
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

  const getSeverityBadge = (severity) => {
    const colors = {
      CRITICAL: 'bg-red-500/20 text-red-500 border-red-500/50',
      HIGH: 'bg-orange-500/20 text-orange-500 border-orange-500/50',
      MEDIUM: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
      LOW: 'bg-green-500/20 text-green-500 border-green-500/50'
    };
    return colors[severity] || colors.LOW;
  };

  const getStatusBadge = (status) => {
    const colors = {
      'Bloqué': 'bg-green-500/20 text-green-500',
      'En cours': 'bg-orange-500/20 text-orange-500',
      'Analysé': 'bg-blue-500/20 text-blue-500'
    };
    return colors[status] || 'bg-gray-500/20 text-gray-500';
  };

  return (
    <div className="p-4 md:p-6 space-y-6 w-full max-w-full overflow-x-hidden">
      <Toast ref={toast} />

      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex-1 min-w-0">
          <h1 className="text-4xl font-anton uppercase text-text tracking-tight">
            Security Operations Center
          </h1>
          <p className="text-gray-400 mt-2 text-sm md:text-base">
            Surveillance et protection en temps réel
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
          </select>
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`p-2 rounded-lg ${autoRefresh ? 'bg-primary text-white' : 'bg-card border border-darkGray'}`}
          >
            <RefreshCw className={`w-5 h-5 ${autoRefresh ? 'animate-spin' : ''}`} />
          </button>
          <button className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg font-semibold">
            <Download size={18} />
            Rapport
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <SecurityKPICard
          title="Niveau de Menace"
          value={securityMetrics.threatLevel.value}
          change={securityMetrics.threatLevel.change}
          trend={securityMetrics.threatLevel.trend}
          icon={Shield}
          subtitle={`Score: ${securityMetrics.threatLevel.score}/100`}
          level={securityMetrics.threatLevel.value}
        />
        <SecurityKPICard
          title="Attaques Bloquées"
          value={securityMetrics.blockedAttacks.value.toLocaleString()}
          change={securityMetrics.blockedAttacks.change}
          trend={securityMetrics.blockedAttacks.trend}
          icon={Lock}
          subtitle="Dernières 24h"
        />
        <SecurityKPICard
          title="Menaces Actives"
          value={securityMetrics.activeThreats.value}
          change={securityMetrics.activeThreats.change}
          trend={securityMetrics.activeThreats.trend}
          icon={AlertTriangle}
          subtitle="En cours d'analyse"
          level="HIGH"
        />
        <SecurityKPICard
          title="Score Sécurité"
          value={`${securityMetrics.securityScore.value}%`}
          change={securityMetrics.securityScore.change}
          trend={securityMetrics.securityScore.trend}
          icon={CheckCircle}
          subtitle={`Objectif: ${securityMetrics.securityScore.target}%`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
            <Activity className="w-5 h-5 text-primary" />
            Événements de Sécurité (24h)
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={securityEvents}>
              <CartesianGrid strokeDasharray="3 3" stroke="#343A40" />
              <XAxis dataKey="heure" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#181F27',
                  border: '1px solid #343A40',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="menaces" stroke="#F58424" strokeWidth={2} name="Menaces Détectées" />
              <Line type="monotone" dataKey="bloquees" stroke="#28A745" strokeWidth={2} name="Bloquées" />
              <Line type="monotone" dataKey="critiques" stroke="#DC3545" strokeWidth={2} name="Critiques" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
            <Shield className="w-5 h-5 text-secondary" />
            Distribution des Menaces
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={threatDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {threatDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="border border-darkGray bg-card rounded-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-anton uppercase text-text flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-danger" />
            Menaces Récentes
          </h2>
          <div className="flex items-center gap-2">
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              className="px-3 py-1.5 bg-darkGray border border-darkGray rounded-lg text-text text-sm"
            >
              <option value="all">Toutes</option>
              <option value="critical">Critiques</option>
              <option value="high">Élevées</option>
            </select>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-darkGray">
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Type</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">IP Source</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Pays</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Sévérité</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Statut</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Temps</th>
                <th className="text-left py-3 px-4 text-xs font-semibold text-gray-400 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {recentThreats.map((threat) => (
                <tr key={threat.id} className="border-b border-darkGray/50 hover:bg-darkGray/30 transition-colors">
                  <td className="py-3 px-4 text-sm text-text font-medium">{threat.type}</td>
                  <td className="py-3 px-4 text-sm text-gray-400 font-mono">{threat.ip}</td>
                  <td className="py-3 px-4 text-sm text-gray-400">{threat.pays}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold border ${getSeverityBadge(threat.severite)}`}>
                      {threat.severite}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBadge(threat.statut)}`}>
                      {threat.statut}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-400">Il y a {threat.temps}</td>
                  <td className="py-3 px-4">
                    <button className="text-primary hover:text-primary/80 text-sm font-semibold">
                      Détails
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="border border-darkGray bg-card rounded-lg p-6">
        <h2 className="text-xl font-anton uppercase text-text mb-6 flex items-center gap-2">
          <Server className="w-5 h-5 text-primary" />
          Règles Firewall Actives
        </h2>
        <div className="space-y-3">
          {firewallRules.map((rule) => (
            <div key={rule.id} className="flex items-center justify-between p-4 bg-darkGray/30 rounded-lg hover:bg-darkGray/50 transition-colors">
              <div className="flex items-center gap-4 flex-1">
                <div className={`w-3 h-3 rounded-full ${rule.actif ? 'bg-green-500' : 'bg-gray-500'}`} />
                <div className="flex-1">
                  <p className="text-text font-semibold">{rule.nom}</p>
                  <p className="text-xs text-gray-400">{rule.type}</p>
                </div>
              </div>
              <div className="flex items-center gap-6">
                <div className="text-right">
                  <p className="text-sm text-gray-400">Hits</p>
                  <p className="text-lg font-bold text-text">{rule.hits.toLocaleString()}</p>
                </div>
                <button className={`px-4 py-2 rounded-lg font-semibold text-sm ${
                  rule.actif ? 'bg-green-500/20 text-green-500' : 'bg-gray-500/20 text-gray-500'
                }`}>
                  {rule.actif ? 'Actif' : 'Inactif'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Securite;
