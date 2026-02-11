import { useState } from 'react';
import {
  Code, Zap, Shield, Globe, Terminal,
  Book, CheckCircle, Copy, ExternalLink,
  Webhook, FileCode, Key, ArrowRight,
  Database, Server, ChevronRight, Smartphone,
  Package, Play, ShoppingCart, Store
} from 'lucide-react';

const Developers = () => {
  const [activeEndpoint, setActiveEndpoint] = useState('payment');
  const [copiedCode, setCopiedCode] = useState(false);

  // API Endpoints
  const endpoints = [
    {
      id: 'payment',
      method: 'POST',
      path: '/api/v1/payments',
      description: 'Initier un paiement',
      params: ['amount', 'currency', 'recipient', 'description'],
      example: `{
  "amount": 50000,
  "currency": "BIF",
  "recipient": "+25779123456",
  "description": "Commande #12345"
}`
    },
    {
      id: 'transfer',
      method: 'POST',
      path: '/api/v1/transfers',
      description: 'Effectuer un transfert',
      params: ['amount', 'currency', 'from', 'to'],
      example: `{
  "amount": 100000,
  "currency": "BIF",
  "from": "account_id",
  "to": "+25769987654"
}`
    },
    {
      id: 'balance',
      method: 'GET',
      path: '/api/v1/balance',
      description: 'Consulter le solde du compte',
      params: ['account_id'],
      example: `// GET request - no body`
    },
    {
      id: 'transaction',
      method: 'GET',
      path: '/api/v1/transactions/:id',
      description: 'Récupérer les détails d\'une transaction',
      params: ['transaction_id'],
      example: `// GET /api/v1/transactions/txn_abc123`
    },
  ];

  // SDKs
  const sdks = [
    { lang: 'JavaScript', icon: FileCode, command: 'npm install ufaranga-js', color: 'yellow-500' },
    { lang: 'Python', icon: Code, command: 'pip install ufaranga', color: 'blue-500' },
    { lang: 'PHP', icon: Server, command: 'composer require ufaranga/sdk', color: 'purple-500' },
    { lang: 'Java', icon: Terminal, command: 'maven add ufaranga-sdk', color: 'red-500' },
  ];

  // Plugins
  const plugins = [
    { name: 'WooCommerce', desc: 'Plugin WordPress pour boutiques en ligne', downloads: '500+', icon: Globe },
    { name: 'Shopify', desc: 'App Shopify pour paiements uFaranga', downloads: '200+', icon: ShoppingCart },
    { name: 'PrestaShop', desc: 'Module PrestaShop e-commerce', downloads: '150+', icon: Store },
  ];

  // Webhooks events
  const webhookEvents = [
    { event: 'payment.success', desc: 'Paiement réussi et confirmé' },
    { event: 'payment.failed', desc: 'Paiement échoué ou refusé' },
    { event: 'transfer.completed', desc: 'Transfert terminé avec succès' },
    { event: 'balance.updated', desc: 'Solde du compte mis à jour' },
  ];

  // Code examples
  const codeExamples = {
    init: `// Initialiser le SDK
const Ufaranga = require('ufaranga-js');

const client = new Ufaranga({
  apiKey: process.env.UFARANGA_API_KEY,
  environment: 'production' // ou 'sandbox'
});`,
    payment: `// Créer un paiement
const payment = await client.payments.create({
  amount: 50000,
  currency: 'BIF',
  recipient: '+25779123456',
  description: 'Abonnement Premium - Mars 2026',
  metadata: {
    order_id: '12345',
    customer_email: 'jean@example.com'
  }
});

console.log('Paiement créé:', payment.id);
// Retourne: { id, status, amount, ... }`,
    webhook: `// Configuration Webhook (Express.js)
app.post('/webhooks/ufaranga', (req, res) => {
  const signature = req.headers['x-ufaranga-signature'];
  
  // Vérifier la signature
  const isValid = client.webhooks.verify(
    req.body,
    signature,
    process.env.WEBHOOK_SECRET
  );
  
  if (!isValid) {
    return res.status(401).send('Invalid signature');
  }
  
  const { event, data } = req.body;
  
  switch (event) {
    case 'payment.success':
      console.log('Paiement reçu:', data.payment_id);
      // Débloquer la commande, envoyer email, etc.
      break;
      
    case 'payment.failed':
      console.log('Paiement échoué:', data.reason);
      // Notifier le client
      break;
  }
  
  res.status(200).send('OK');
});`
  };

  const copyCode = (code) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Code className="w-5 h-5" />
              <span className="font-semibold">API & Intégrations</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              API UFARANGA
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Intégrez les paiements mobiles dans vos applications en quelques minutes
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/developpeurs/inscription"
                className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2"
              >
                <Key className="w-5 h-5" />
                Obtenir une clé API
              </a>
              <button className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center gap-2">
                <Book className="w-5 h-5" />
                Documentation
              </button>
            </div>
            <p className="text-sm text-gray-400 mt-4">
              Gratuit jusqu'à 1,000 transactions/mois • Sandbox illimité
            </p>
          </div>
        </div>
      </section>

      {/* Quick Start */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-4">
              DÉMARRAGE RAPIDE
            </h2>
            <p className="text-center text-gray-400 mb-12">Votre premier paiement en 5 minutes</p>

            <div className="grid md:grid-cols-3 gap-6 mb-10">
              <div className="border border-gray-800 rounded-xl p-6 text-center hover:border-primary/50 transition-colors">
                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl font-bold text-primary">1</span>
                </div>
                <h3 className="font-bold mb-2">Créez un compte développeur</h3>
                <p className="text-sm text-gray-400">Obtenez vos clés API en 30 secondes</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 text-center hover:border-primary/50 transition-colors">
                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl font-bold text-primary">2</span>
                </div>
                <h3 className="font-bold mb-2">Installez le SDK</h3>
                <p className="text-sm text-gray-400">npm, pip, composer ou maven</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 text-center hover:border-primary/50 transition-colors">
                <div className="w-16 h-16 rounded-full bg-secondary/20 flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl font-bold text-secondary">3</span>
                </div>
                <h3 className="font-bold mb-2">Premier paiement</h3>
                <p className="text-sm text-gray-400">5 lignes de code suffisent</p>
              </div>
            </div>

            {/* Code Example */}
            <div className="border border-gray-800 rounded-xl overflow-hidden">
              <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-gray-900/50">
                <span className="text-sm text-gray-400 font-mono">quick_start.js</span>
                <button
                  onClick={() => copyCode(codeExamples.init + '\n\n' + codeExamples.payment)}
                  className="text-xs text-gray-400 hover:text-white transition-colors flex items-center gap-1"
                >
                  {copiedCode ? <CheckCircle className="w-4 h-4 text-secondary" /> : <Copy className="w-4 h-4" />}
                  {copiedCode ? 'Copié !' : 'Copier'}
                </button>
              </div>
              <pre className="p-6 text-sm text-green-400 overflow-x-auto bg-black">
                <code>{codeExamples.init}{'\n\n'}{codeExamples.payment}</code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* API Endpoints */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-anton uppercase mb-4">ENDPOINTS PRINCIPAUX</h2>
              <p className="text-gray-400 text-lg">API REST complète avec tous les endpoints financiers</p>
            </div>

            <div className="grid gap-4">
              {endpoints.map((endpoint) => (
                <div
                  key={endpoint.id}
                  className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-all cursor-pointer"
                  onClick={() => setActiveEndpoint(endpoint.id)}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-4">
                      <span className={`px-3 py-1 rounded-lg font-mono text-sm font-bold ${endpoint.method === 'GET'
                          ? 'bg-secondary/20 text-secondary'
                          : 'bg-primary/20 text-primary'
                        }`}>
                        {endpoint.method}
                      </span>
                      <code className="text-white font-mono">{endpoint.path}</code>
                    </div>
                    <ChevronRight className={`w-5 h-5 text-gray-500 transition-transform ${activeEndpoint === endpoint.id ? 'rotate-90' : ''}`} />
                  </div>
                  <p className="text-gray-400 text-sm mb-2">{endpoint.description}</p>

                  {activeEndpoint === endpoint.id && (
                    <div className="mt-4 pt-4 border-t border-gray-800">
                      <div className="mb-3">
                        <div className="text-xs text-gray-500 mb-2">Paramètres:</div>
                        <div className="flex flex-wrap gap-2">
                          {endpoint.params.map((param, i) => (
                            <span key={i} className="px-2 py-1 rounded bg-primary/10 text-primary text-xs font-mono">
                              {param}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 mb-2">Exemple:</div>
                        <pre className="p-3 rounded-lg bg-gray-900 text-secondary text-xs overflow-x-auto">
                          <code>{endpoint.example}</code>
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* SDKs */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-anton uppercase mb-4">SDKS OFFICIELS</h2>
              <p className="text-gray-400 text-lg">Bibliothèques pour tous les langages populaires</p>
            </div>

            <div className="grid md:grid-cols-4 gap-6">
              {sdks.map((sdk, i) => (
                <div key={i} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-all">
                  <div className="w-14 h-14 rounded-2xl bg-primary/20 flex items-center justify-center mb-4">
                    <sdk.icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="font-bold text-white mb-2">{sdk.lang}</h3>
                  <code className="text-xs text-gray-400 bg-gray-900 px-2 py-1 rounded block mb-4">{sdk.command}</code>
                  <button className="text-primary font-bold text-sm flex items-center gap-1 hover:gap-2 transition-all">
                    Docs <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Webhooks */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="border border-secondary/30 rounded-xl p-10 bg-gradient-to-br from-secondary/5 to-black">
              <div className="grid md:grid-cols-2 gap-10">
                <div>
                  <Webhook className="w-12 h-12 text-secondary mb-4" />
                  <h2 className="text-3xl font-anton uppercase mb-4">WEBHOOKS TEMPS RÉEL</h2>
                  <p className="text-gray-300 mb-6">
                    Recevez des notifications instantanées pour tous les événements importants : paiements, transferts, mises à jour de solde.
                  </p>

                  <div className="space-y-3 mb-6">
                    <h3 className="font-bold text-white text-sm mb-2">Événements disponibles:</h3>
                    {webhookEvents.map((event, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <CheckCircle className="w-4 h-4 text-secondary shrink-0 mt-0.5" />
                        <div>
                          <code className="text-secondary text-sm font-mono">{event.event}</code>
                          <div className="text-xs text-gray-400">{event.desc}</div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <button className="bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2">
                    <Webhook className="w-5 h-5" /> Configurer les webhooks
                  </button>
                </div>

                <div className="bg-gray-900 rounded-xl p-6 border border-gray-800">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-gray-400 font-mono">webhook_handler.js</span>
                    <button
                      onClick={() => copyCode(codeExamples.webhook)}
                      className="text-xs text-gray-500 hover:text-white transition-colors flex items-center gap-1"
                    >
                      {copiedCode ? <CheckCircle className="w-4 h-4 text-secondary" /> : <Copy className="w-4 h-4" />}
                      {copiedCode ? 'Copié !' : 'Copier'}
                    </button>
                  </div>
                  <pre className="text-xs text-secondary overflow-x-auto">
                    <code>{codeExamples.webhook}</code>
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Plugins E-commerce */}
      <section className="py-20 bg-gradient-to-b from-primary/5 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-anton uppercase mb-4">PLUGINS E-COMMERCE</h2>
              <p className="text-gray-400 text-lg">Intégration clé en main pour les plateformes populaires</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {plugins.map((plugin, i) => (
                <div key={i} className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-all">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-secondary/20 flex items-center justify-center">
                      <plugin.icon className="w-6 h-6 text-secondary" />
                    </div>
                    <div>
                      <h3 className="font-bold text-white">{plugin.name}</h3>
                      <div className="text-xs text-gray-500">{plugin.downloads} téléchargements</div>
                    </div>
                  </div>
                  <p className="text-sm text-gray-400 mb-4">{plugin.desc}</p>
                  <button className="text-secondary font-bold text-sm flex items-center gap-1 hover:gap-2 transition-all">
                    Télécharger <ExternalLink className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <h2 className="text-4xl font-anton uppercase mb-4">PRÊT À INTÉGRER UFARANGA ?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Créez votre compte développeur et obtenez vos clés API gratuitement
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/developpeurs/inscription"
                className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2"
              >
                <Key className="w-5 h-5" /> Créer un compte développeur
              </a>
              <button className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center justify-center gap-2">
                <Book className="w-5 h-5" /> Lire la documentation
              </button>
            </div>
            <p className="text-sm text-gray-500 mt-6">
              Support technique 24/7 • Documentation en français • Sandbox de test illimité
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Developers;
