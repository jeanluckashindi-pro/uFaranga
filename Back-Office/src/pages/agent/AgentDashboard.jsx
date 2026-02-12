import { useState } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  TrendingUp, TrendingDown, DollarSign, Activity,
  Users, ArrowUpRight, ArrowDownRight, AlertCircle,
  ArrowDownToLine, ArrowUpFromLine, ArrowLeftRight, CreditCard
} from 'lucide-react';

function AgentDashboard() {
  // KPIs
  const [kpis] = useState({
    floatBalance: 2500000,
    cashBalance: 1800000,
    depositsToday: 856000,
    withdrawalsToday: 623000,
    commissionsToday: 45600,
    commissionsMonth: 1234500,
    transactionsToday: 47,
    floatMin: 1000000
  });

  // Données pour graphique en barres - Transactions par type
  const transactionsByType = [
    { name: 'Lun', depots: 450000, retraits: 320000, transferts: 180000 },
    { name: 'Mar', depots: 520000, retraits: 380000, transferts: 210000 },
    { name: 'Mer', depots: 480000, retraits: 350000, transferts: 190000 },
    { name: 'Jeu', depots: 610000, retraits: 420000, transferts: 240000 },
    { name: 'Ven', depots: 720000, retraits: 510000, transferts: 280000 },
    { name: 'Sam', depots: 890000, retraits: 640000, transferts: 320000 },
    { name: 'Dim', depots: 856000, retraits: 623000, transferts: 295000 }
  ];

  // Données pour graphique en ligne - Évolution des commissions
  const commissionsData = [
    { jour: 'J-6', commissions: 38000 },
    { jour: 'J-5', commissions: 42000 },
    { jour: 'J-4', commissions: 39500 },
    { jour: 'J-3', commissions: 47000 },
    { jour: 'J-2', commissions: 51000 },
    { jour: 'J-1', commissions: 58000 },
    { jour: "Auj", commissions: 45600 }
  ];

  // Données pour graphique en camembert - Répartition des transactions
  const transactionDistribution = [
    { name: 'Dépôts', value: 856000, color: '#F58424' },
    { name: 'Retraits', value: 623000, color: '#007BFF' },
    { name: 'Transferts', value: 295000, color: '#6b7280' },
    { name: 'Paiements', value: 187000, color: '#9ca3af' }
  ];

  // Transactions récentes
  const recentTransactions = [
    { id: 'TXN001', type: 'depot', client: '+257 79 123 456', amount: 50000, commission: 500, time: '14:35', status: 'success' },
    { id: 'TXN002', type: 'retrait', client: '+257 79 234 567', amount: 30000, commission: 450, time: '14:28', status: 'success' },
    { id: 'TXN003', type: 'transfert', client: '+257 79 345 678', amount: 25000, commission: 250, time: '14:15', status: 'success' },
    { id: 'TXN004', type: 'depot', client: '+257 79 456 789', amount: 100000, commission: 1000, time: '13:52', status: 'success' },
    { id: 'TXN005', type: 'paiement', client: '+257 79 567 890', amount: 15000, commission: 200, time: '13:45', status: 'pending' }
  ];

  const floatPercentage = ((kpis.floatBalance / (kpis.floatMin * 3)) * 100).toFixed(0);
  const isFloatLow = kpis.floatBalance < kpis.floatMin * 1.5;

  const getTypeIcon = (type) => {
    const icons = {
      depot: ArrowDownToLine,
      retrait: ArrowUpFromLine,
      transfert: ArrowLeftRight,
      paiement: CreditCard
    };
    return icons[type] || Activity;
  };

  const getStatusBadge = (status) => {
    if (status === 'success') return <span className="px-2 py-1 bg-secondary/20 text-secondary text-xs rounded-full">Succès</span>;
    if (status === 'pending') return <span className="px-2 py-1 bg-yellow-500/20 text-yellow-500 text-xs rounded-full">En cours</span>;
    return <span className="px-2 py-1 bg-red-500/20 text-red-500 text-xs rounded-full">Échec</span>;
  };

  return (
    <div className="p-6 space-y-6">
      {/* Alert Float Faible */}
      {isFloatLow && (
        <div className="bg-red-500/10 border border-darkGray rounded-lg p-4 flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <div className="flex-1">
            <p className="text-text font-semibold">Float proche du minimum</p>
            <p className="text-gray-400 text-sm">Votre solde float est en dessous du seuil recommandé</p>
          </div>
          <button className="px-4 py-2 bg-text text-background rounded-lg hover:bg-lightGray transition-colors">
            Recharger
          </button>
        </div>
      )}

      {/* KPIs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Float Balance */}
        <div className={`border rounded-lg p-6 bg-card ${isFloatLow ? 'border-darkGray' : 'border-darkGray'}`}>
          <div className="flex items-center justify-between mb-2">
            <p className="text-gray-400 text-sm">Float Balance</p>
            <DollarSign className={`w-5 h-5 ${isFloatLow ? 'text-red-500' : 'text-secondary'}`} />
          </div>
          <p className="text-3xl font-bold text-text mb-2">{(kpis.floatBalance / 1000).toFixed(0)}K BIF</p>
          <div className="h-2 bg-darkGray rounded-full overflow-hidden">
            <div 
              className={`h-full ${isFloatLow ? 'bg-red-500' : 'bg-secondary'}`}
              style={{ width: `${floatPercentage}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">{floatPercentage}% du maximum</p>
        </div>

        {/* Cash Balance */}
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <p className="text-gray-400 text-sm">Cash Physique</p>
            <DollarSign className="w-5 h-5 text-primary" />
          </div>
          <p className="text-3xl font-bold text-text mb-2">{(kpis.cashBalance / 1000).toFixed(0)}K BIF</p>
          <div className="flex items-center gap-1 text-primary text-sm">
            <ArrowUpRight className="w-4 h-4" />
            <span>+12% vs hier</span>
          </div>
        </div>

        {/* Commissions Today */}
        <div className="border border-darkGray hover:border-darkGray bg-card rounded-lg p-6 transition-colors">
          <div className="flex items-center justify-between mb-2">
            <p className="text-gray-400 text-sm">Commissions Jour</p>
            <TrendingUp className="w-5 h-5 text-secondary" />
          </div>
          <p className="text-3xl font-bold text-text mb-2">{(kpis.commissionsToday / 1000).toFixed(1)}K BIF</p>
          <div className="flex items-center gap-1 text-secondary text-sm">
            <ArrowUpRight className="w-4 h-4" />
            <span>+8% vs hier</span>
          </div>
        </div>

        {/* Transactions Today */}
        <div className="border border-darkGray hover:border-darkGray bg-card rounded-lg p-6 transition-colors">
          <div className="flex items-center justify-between mb-2">
            <p className="text-gray-400 text-sm">Transactions</p>
            <Activity className="w-5 h-5 text-primary" />
          </div>
          <p className="text-3xl font-bold text-text mb-2">{kpis.transactionsToday}</p>
          <div className="flex items-center gap-1 text-gray-400 text-sm">
            <Users className="w-4 h-4" />
            <span>Clients servis</span>
          </div>
        </div>
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Graphique en Barres - Transactions par type */}
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h3 className="text-xl font-anton uppercase text-text mb-4">Transactions Hebdomadaires</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={transactionsByType}>
              <CartesianGrid strokeDasharray="3 3" stroke="#343A40" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#181F27', border: '1px solid #343A40', borderRadius: '8px' }}
                labelStyle={{ color: '#F9F9F9' }}
              />
              <Legend />
              <Bar dataKey="depots" fill="#F58424" name="Dépôts" />
              <Bar dataKey="retraits" fill="#007BFF" name="Retraits" />
              <Bar dataKey="transferts" fill="#6b7280" name="Transferts" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Graphique en Ligne - Évolution commissions */}
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h3 className="text-xl font-anton uppercase text-text mb-4">Évolution Commissions</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={commissionsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#343A40" />
              <XAxis dataKey="jour" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#181F27', border: '1px solid #343A40', borderRadius: '8px' }}
                labelStyle={{ color: '#F9F9F9' }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="commissions" 
                stroke="#F58424" 
                strokeWidth={3}
                dot={{ fill: '#F58424', r: 5 }}
                name="Commissions (BIF)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Graphique Camembert + Transactions récentes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graphique en Camembert */}
        <div className="border border-darkGray bg-card rounded-lg p-6">
          <h3 className="text-xl font-anton uppercase text-text mb-4">Répartition</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={transactionDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {transactionDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#181F27', border: '1px solid #343A40', borderRadius: '8px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Transactions récentes */}
        <div className="lg:col-span-2 border border-darkGray bg-card rounded-lg p-6">
          <h3 className="text-xl font-anton uppercase text-text mb-4">Transactions Récentes</h3>
          <div className="space-y-3">
            {recentTransactions.map((tx) => {
              const IconComponent = getTypeIcon(tx.type);
              return (
                <div key={tx.id} className="flex items-center justify-between p-3 bg-darkBlue rounded-lg hover:bg-darkGray transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <IconComponent className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-text font-semibold">{tx.client}</p>
                      <p className="text-gray-400 text-sm">{tx.id} • {tx.time}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-text font-bold">{tx.amount.toLocaleString()} BIF</p>
                    <p className="text-secondary text-sm">+{tx.commission} BIF</p>
                  </div>
                  <div>
                    {getStatusBadge(tx.status)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Actions rapides */}
      <div className="border border-darkGray bg-card rounded-lg p-6">
        <h3 className="text-xl font-anton uppercase text-text mb-4">Actions Rapides</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="p-6 bg-text text-background rounded-lg hover:bg-lightGray transition-colors flex flex-col items-center gap-2">
            <ArrowDownToLine className="w-8 h-8" />
            <span className="font-semibold">Dépôt</span>
          </button>
          <button className="p-6 border border-darkGray hover:border-darkGray bg-card rounded-lg transition-colors flex flex-col items-center gap-2">
            <ArrowUpFromLine className="w-8 h-8 text-text" />
            <span className="font-semibold text-text">Retrait</span>
          </button>
          <button className="p-6 border border-darkGray hover:border-darkGray bg-card rounded-lg transition-colors flex flex-col items-center gap-2">
            <ArrowLeftRight className="w-8 h-8 text-text" />
            <span className="font-semibold text-text">Transfert</span>
          </button>
          <button className="p-6 border border-darkGray hover:border-darkGray bg-card rounded-lg transition-colors flex flex-col items-center gap-2">
            <CreditCard className="w-8 h-8 text-text" />
            <span className="font-semibold text-text">Paiement</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default AgentDashboard;
