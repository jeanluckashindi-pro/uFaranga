import React, { useState } from 'react';
import { Search, Filter, Download, Eye, CheckCircle, Clock, XCircle } from 'lucide-react';

const Transactions = () => {
  const [filter, setFilter] = useState('all');

  const transactions = [
    { id: 'TRX001234', date: '2024-02-11 14:30', user: 'Jean Dupont', type: 'Transfert', amount: 50000, status: 'completed', from: 'Compte A', to: 'Compte B' },
    { id: 'TRX001235', date: '2024-02-11 14:25', user: 'Marie Uwimana', type: 'Dépôt', amount: 100000, status: 'completed', from: 'Cash', to: 'Compte' },
    { id: 'TRX001236', date: '2024-02-11 14:20', user: 'David N.', type: 'Retrait', amount: 75000, status: 'pending', from: 'Compte', to: 'Cash' },
    { id: 'TRX001237', date: '2024-02-11 14:15', user: 'Sophie T.', type: 'Paiement', amount: 25000, status: 'completed', from: 'Compte', to: 'Marchand' },
    { id: 'TRX001238', date: '2024-02-11 14:10', user: 'Eric K.', type: 'Recharge', amount: 5000, status: 'failed', from: 'Compte', to: 'Opérateur' },
  ];

  const getStatusBadge = (status) => {
    const styles = {
      completed: 'bg-green-500/20 text-green-400 border-green-500/30',
      pending: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
      failed: 'bg-red-500/20 text-red-400 border-red-500/30'
    };
    const icons = {
      completed: CheckCircle,
      pending: Clock,
      failed: XCircle
    };
    const Icon = icons[status];
    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs border ${styles[status]}`}>
        <Icon className="w-3 h-3" />
        {status === 'completed' ? 'Terminé' : status === 'pending' ? 'En cours' : 'Échoué'}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Transactions</h1>
          <p className="text-gray-400">Gérez toutes les transactions de la plateforme</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-primary/90 rounded-lg transition-colors">
          <Download className="w-4 h-4" />
          Exporter
        </button>
      </div>

      {/* Filters */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher par ID, utilisateur..."
              className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:border-primary"
            />
          </div>
          <select className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary">
            <option>Tous les types</option>
            <option>Transfert</option>
            <option>Dépôt</option>
            <option>Retrait</option>
            <option>Paiement</option>
          </select>
          <select className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary">
            <option>Tous les statuts</option>
            <option>Terminé</option>
            <option>En cours</option>
            <option>Échoué</option>
          </select>
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700">
            <Filter className="w-4 h-4" />
            Filtres
          </button>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-800 border-b border-gray-700">
              <tr>
                <th className="text-left px-6 py-4 text-sm font-semibold">ID Transaction</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Date & Heure</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Utilisateur</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Type</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Montant</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Statut</th>
                <th className="text-left px-6 py-4 text-sm font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-gray-800/50 transition-colors">
                  <td className="px-6 py-4">
                    <span className="font-mono text-sm text-primary">{tx.id}</span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400">{tx.date}</td>
                  <td className="px-6 py-4">
                    <div className="font-semibold">{tx.user}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm">{tx.type}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-mono font-bold">{tx.amount.toLocaleString()} FBU</span>
                  </td>
                  <td className="px-6 py-4">
                    {getStatusBadge(tx.status)}
                  </td>
                  <td className="px-6 py-4">
                    <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-800">
          <div className="text-sm text-gray-400">
            Affichage de 1 à 5 sur 156,789 transactions
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
              Précédent
            </button>
            <button className="px-4 py-2 bg-primary rounded-lg">1</button>
            <button className="px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">2</button>
            <button className="px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">3</button>
            <button className="px-4 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
              Suivant
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Transactions;
