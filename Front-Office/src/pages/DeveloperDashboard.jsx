import { useState } from 'react';
import {
  Key, Copy, Eye, EyeOff, CheckCircle, AlertCircle,
  RefreshCw, Trash2, Settings, BarChart3, Code,
  Webhook, FileText, Download, Shield, Activity
} from 'lucide-react';

const DeveloperDashboard = () => {
  const [showSecretKey, setShowSecretKey] = useState(false);
  const [copiedKey, setCopiedKey] = useState('');

  // Données simulées
  const apiKeys = {
    sandbox: {
      publicKey: 'pk_test_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O',
      secretKey: 'sk_test_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O',
      webhookSecret: 'whsec_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O'
    },
    production: {
      publicKey: 'pk_live_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O',
      secretKey: 'sk_live_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O',
      webhookSecret: 'whsec_live_51H7xKjL4Kx8Qz9Y0Z1X2W3V4U5T6S7R8Q9P0O'
    }
  };

  const stats = [
    { label: 'Transactions ce mois', value: '1,234', icon: Activity, color: 'primary' },
    { label: 'Volume total', value: '45.2M BIF', icon: BarChart3, color: 'secondary' },
    { label: 'Taux de succès', value: '99.8%', icon: CheckCircle, color: 'secondary' },
    { label: 'Webhooks envoyés', value: '3,456', icon: Webhook, color: 'primary' }
  ];

  const recentTransactions = [
    { id: 'txn_001', amount: '50,000 BIF', status: 'success', date: '2026-02-11 14:32' },
    { id: 'txn_002', amount: '125,000 BIF', status: 'success', date: '2026-02-11 13:15' },
    { id: 'txn_003', amount: '75,000 BIF', status: 'failed', date: '2026-02-11 12:08' },
    { id: 'txn_004', amount: '200,000 BIF', status: 'success', date: '2026-02-11 11:45' },
    { id: 'txn_005', amount: '30,000 BIF', status: 'pending', date: '2026-02-11 10:22' }
  ];

  const copyToClipboard = (text, keyName) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(keyName);
    setTimeout(() => setCopiedKey(''), 2000);
  };

  const regenerateKey = (keyType) => {
    if (confirm(`Êtes-vous sûr de vouloir régénérer votre ${keyType} ? L'ancienne clé sera immédiatement invalidée.`)) {
      alert('Clé régénérée avec succès !');
    }
  };

  return (
    <div className="min-h-screen bg-black py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-4xl font-anton uppercase mb-2">TABLEAU DE BORD DÉVELOPPEUR</h1>
                <p className="text-gray-400">Gérez vos clés API et suivez vos transactions</p>
              </div>
              <a
                href="/sandbox"
                className="bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
              >
                <Code className="w-5 h-5" />
                Tester l'API
              </a>
            </div>

            {/* Stats */}
            <div className="grid md:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="flex items-center justify-between mb-3">
                    <stat.icon className={`w-8 h-8 text-${stat.color}`} />
                  </div>
                  <div className="text-3xl font-bold mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* API Keys Section */}
          <div className="grid lg:grid-cols-2 gap-6 mb-12">
            {/* Sandbox Keys */}
            <div className="border border-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-secondary/20 flex items-center justify-center">
                    <Key className="w-5 h-5 text-secondary" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold">Clés Sandbox</h2>
                    <p className="text-sm text-gray-400">Environnement de test</p>
                  </div>
                </div>
                <span className="px-3 py-1 bg-secondary/20 text-secondary text-xs font-semibold rounded-full">
                  TEST
                </span>
              </div>

              <div className="space-y-4">
                {/* Public Key */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">API Key (Publique)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={apiKeys.sandbox.publicKey}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => copyToClipboard(apiKeys.sandbox.publicKey, 'sandbox-public')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-secondary/50 transition-colors"
                    >
                      {copiedKey === 'sandbox-public' ? (
                        <CheckCircle className="w-5 h-5 text-secondary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Secret Key */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">Secret Key (Privée)</label>
                  <div className="flex gap-2">
                    <input
                      type={showSecretKey ? 'text' : 'password'}
                      value={apiKeys.sandbox.secretKey}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => setShowSecretKey(!showSecretKey)}
                      className="border border-gray-800 px-4 rounded-lg hover:border-secondary/50 transition-colors"
                    >
                      {showSecretKey ? (
                        <EyeOff className="w-5 h-5 text-gray-400" />
                      ) : (
                        <Eye className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                    <button
                      onClick={() => copyToClipboard(apiKeys.sandbox.secretKey, 'sandbox-secret')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-secondary/50 transition-colors"
                    >
                      {copiedKey === 'sandbox-secret' ? (
                        <CheckCircle className="w-5 h-5 text-secondary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Webhook Secret */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">Webhook Secret</label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={apiKeys.sandbox.webhookSecret}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => copyToClipboard(apiKeys.sandbox.webhookSecret, 'sandbox-webhook')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-secondary/50 transition-colors"
                    >
                      {copiedKey === 'sandbox-webhook' ? (
                        <CheckCircle className="w-5 h-5 text-secondary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                <button
                  onClick={() => regenerateKey('clés Sandbox')}
                  className="w-full mt-4 border border-gray-800 px-4 py-2 rounded-lg hover:border-secondary/50 transition-colors text-sm font-semibold inline-flex items-center justify-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  Régénérer les clés
                </button>
              </div>
            </div>

            {/* Production Keys */}
            <div className="border border-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">
                    <Key className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold">Clés Production</h2>
                    <p className="text-sm text-gray-400">Environnement réel</p>
                  </div>
                </div>
                <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-semibold rounded-full">
                  LIVE
                </span>
              </div>

              <div className="space-y-4">
                {/* Public Key */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">API Key (Publique)</label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={apiKeys.production.publicKey}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => copyToClipboard(apiKeys.production.publicKey, 'prod-public')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-primary/50 transition-colors"
                    >
                      {copiedKey === 'prod-public' ? (
                        <CheckCircle className="w-5 h-5 text-primary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Secret Key */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">Secret Key (Privée)</label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={apiKeys.production.secretKey}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => setShowSecretKey(!showSecretKey)}
                      className="border border-gray-800 px-4 rounded-lg hover:border-primary/50 transition-colors"
                    >
                      {showSecretKey ? (
                        <EyeOff className="w-5 h-5 text-gray-400" />
                      ) : (
                        <Eye className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                    <button
                      onClick={() => copyToClipboard(apiKeys.production.secretKey, 'prod-secret')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-primary/50 transition-colors"
                    >
                      {copiedKey === 'prod-secret' ? (
                        <CheckCircle className="w-5 h-5 text-primary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Webhook Secret */}
                <div>
                  <label className="text-xs text-gray-400 mb-2 block">Webhook Secret</label>
                  <div className="flex gap-2">
                    <input
                      type="password"
                      value={apiKeys.production.webhookSecret}
                      readOnly
                      className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm font-mono"
                    />
                    <button
                      onClick={() => copyToClipboard(apiKeys.production.webhookSecret, 'prod-webhook')}
                      className="border border-gray-800 px-4 rounded-lg hover:border-primary/50 transition-colors"
                    >
                      {copiedKey === 'prod-webhook' ? (
                        <CheckCircle className="w-5 h-5 text-primary" />
                      ) : (
                        <Copy className="w-5 h-5 text-gray-400" />
                      )}
                    </button>
                  </div>
                </div>

                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 flex gap-2 mt-4">
                  <AlertCircle className="w-5 h-5 text-red-500 shrink-0" />
                  <p className="text-xs text-gray-300">
                    Ne partagez jamais vos clés de production. Elles donnent accès à votre compte réel.
                  </p>
                </div>

                <button
                  onClick={() => regenerateKey('clés Production')}
                  className="w-full mt-4 border border-gray-800 px-4 py-2 rounded-lg hover:border-primary/50 transition-colors text-sm font-semibold inline-flex items-center justify-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  Régénérer les clés
                </button>
              </div>
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="border border-gray-800 rounded-xl p-6 mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-anton uppercase">TRANSACTIONS RÉCENTES</h2>
              <a href="#" className="text-primary text-sm font-semibold hover:underline">
                Voir tout
              </a>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">ID Transaction</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Montant</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Statut</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentTransactions.map((tx) => (
                    <tr key={tx.id} className="border-b border-gray-800 hover:bg-gray-900/30">
                      <td className="py-3 px-4 font-mono text-sm">{tx.id}</td>
                      <td className="py-3 px-4 font-semibold">{tx.amount}</td>
                      <td className="py-3 px-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          tx.status === 'success' ? 'bg-secondary/20 text-secondary' :
                          tx.status === 'failed' ? 'bg-red-500/20 text-red-500' :
                          'bg-yellow-500/20 text-yellow-500'
                        }`}>
                          {tx.status === 'success' ? 'Succès' : tx.status === 'failed' ? 'Échoué' : 'En attente'}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-400">{tx.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-3 gap-6">
            <a
              href="/developpeurs"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <FileText className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Documentation</h3>
              <p className="text-sm text-gray-400">Guides et références API</p>
            </a>

            <a
              href="/sandbox"
              className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors"
            >
              <Code className="w-8 h-8 text-secondary mb-3" />
              <h3 className="font-bold mb-2">Sandbox</h3>
              <p className="text-sm text-gray-400">Tester l'API en mode test</p>
            </a>

            <a
              href="/support"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <Shield className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Support</h3>
              <p className="text-sm text-gray-400">Aide et assistance technique</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeveloperDashboard;
