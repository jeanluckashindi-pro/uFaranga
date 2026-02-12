import React from 'react';
import {
  TrendingUp, Users, Wallet, CreditCard, ArrowUpRight, ArrowDownRight,
  DollarSign, Activity, ShoppingBag, Send
} from 'lucide-react';

const Dashboard = () => {
  const stats = [
    {
      label: 'Revenus totaux',
      value: '125,450,000 FBU',
      change: '+12.5%',
      trend: 'up',
      icon: DollarSign,
      color: 'from-green-500 to-emerald-600'
    },
    {
      label: 'Utilisateurs actifs',
      value: '24,567',
      change: '+8.2%',
      trend: 'up',
      icon: Users,
      color: 'from-blue-500 to-cyan-600'
    },
    {
      label: 'Transactions',
      value: '156,789',
      change: '+15.3%',
      trend: 'up',
      icon: Activity,
      color: 'from-purple-500 to-pink-600'
    },
    {
      label: 'Volume',
      value: '2.5B FBU',
      change: '+22.1%',
      trend: 'up',
      icon: TrendingUp,
      color: 'from-orange-500 to-red-600'
    }
  ];

  const recentTransactions = [
    { id: 'TRX001', user: 'Jean Dupont', type: 'Transfert', amount: 50000, status: 'completed', time: 'Il y a 2 min' },
    { id: 'TRX002', user: 'Marie Uwimana', type: 'Dépôt', amount: 100000, status: 'completed', time: 'Il y a 5 min' },
    { id: 'TRX003', user: 'David N.', type: 'Retrait', amount: 75000, status: 'pending', time: 'Il y a 8 min' },
    { id: 'TRX004', user: 'Sophie T.', type: 'Paiement', amount: 25000, status: 'completed', time: 'Il y a 12 min' },
    { id: 'TRX005', user: 'Eric K.', type: 'Recharge', amount: 5000, status: 'completed', time: 'Il y a 15 min' },
  ];

  const topServices = [
    { name: 'Transferts', count: 45678, percentage: 35, color: 'bg-blue-500' },
    { name: 'Dépôts/Retraits', count: 38456, percentage: 30, color: 'bg-green-500' },
    { name: 'Paiements', count: 25634, percentage: 20, color: 'bg-purple-500' },
    { name: 'Recharge', count: 19234, percentage: 15, color: 'bg-orange-500' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Tableau de bord</h1>
        <p className="text-gray-400">Vue d'ensemble de votre plateforme</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.color} flex items-center justify-center`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <div className={`flex items-center gap-1 text-sm ${
                stat.trend === 'up' ? 'text-green-400' : 'text-red-400'
              }`}>
                {stat.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                {stat.change}
              </div>
            </div>
            <div className="text-sm text-gray-400 mb-1">{stat.label}</div>
            <div className="text-2xl font-bold">{stat.value}</div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Recent Transactions */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Transactions récentes</h2>
            <button className="text-sm text-primary hover:text-primary/80">Voir tout</button>
          </div>
          <div className="space-y-4">
            {recentTransactions.map((tx) => (
              <div key={tx.id} className="flex items-center justify-between p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
                    <Send className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <div className="font-semibold">{tx.user}</div>
                    <div className="text-sm text-gray-400">{tx.type} • {tx.time}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-mono font-bold">{tx.amount.toLocaleString()} FBU</div>
                  <div className={`text-xs ${
                    tx.status === 'completed' ? 'text-green-400' : 'text-orange-400'
                  }`}>
                    {tx.status === 'completed' ? 'Terminé' : 'En cours'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Services */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold mb-6">Services populaires</h2>
          <div className="space-y-4">
            {topServices.map((service, i) => (
              <div key={i}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold">{service.name}</span>
                  <span className="text-sm text-gray-400">{service.count.toLocaleString()}</span>
                </div>
                <div className="relative h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div
                    className={`absolute inset-y-0 left-0 ${service.color} rounded-full transition-all duration-500`}
                    style={{ width: `${service.percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-4 gap-4">
        {[
          { icon: Users, label: 'Nouvel utilisateur', color: 'from-blue-500 to-cyan-600' },
          { icon: CreditCard, label: 'Émettre carte', color: 'from-purple-500 to-pink-600' },
          { icon: ShoppingBag, label: 'Nouveau marchand', color: 'from-green-500 to-emerald-600' },
          { icon: Wallet, label: 'Ajuster solde', color: 'from-orange-500 to-red-600' },
        ].map((action, i) => (
          <button
            key={i}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition-colors text-left"
          >
            <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${action.color} flex items-center justify-center mb-4`}>
              <action.icon className="w-6 h-6 text-white" />
            </div>
            <div className="font-semibold">{action.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
