import {
  Sparkles, Bug, Zap, Shield, Code, Plus, Minus,
  AlertCircle, CheckCircle, ArrowRight, Calendar
} from 'lucide-react';

const Changelog = () => {
  const releases = [
    {
      version: '2.5.0',
      date: '2026-02-10',
      type: 'major',
      title: 'Paiements internationaux et multi-devises',
      changes: [
        { type: 'feature', text: 'Support des paiements en USD, EUR et RWF' },
        { type: 'feature', text: 'Conversion automatique de devises en temps réel' },
        { type: 'feature', text: 'Nouveau endpoint /api/v1/exchange-rates' },
        { type: 'improvement', text: 'Performance améliorée de 40% sur les webhooks' },
        { type: 'improvement', text: 'Interface dashboard redesignée' },
        { type: 'fix', text: 'Correction du timeout sur les transactions volumineuses' }
      ]
    },
    {
      version: '2.4.2',
      date: '2026-01-28',
      type: 'patch',
      title: 'Corrections et améliorations',
      changes: [
        { type: 'fix', text: 'Résolution du bug d\'affichage des montants avec décimales' },
        { type: 'fix', text: 'Correction de la validation des numéros de téléphone internationaux' },
        { type: 'improvement', text: 'Messages d\'erreur plus explicites' },
        { type: 'security', text: 'Mise à jour des dépendances de sécurité' }
      ]
    },
    {
      version: '2.4.0',
      date: '2026-01-15',
      type: 'minor',
      title: 'Webhooks v2 et nouveaux SDKs',
      changes: [
        { type: 'feature', text: 'Webhooks v2 avec retry automatique' },
        { type: 'feature', text: 'SDK Python officiel' },
        { type: 'feature', text: 'SDK PHP avec support Laravel' },
        { type: 'improvement', text: 'Documentation interactive avec exemples' },
        { type: 'improvement', text: 'Logs détaillés dans le dashboard' }
      ]
    },
    {
      version: '2.3.1',
      date: '2025-12-20',
      type: 'patch',
      title: 'Optimisations de performance',
      changes: [
        { type: 'improvement', text: 'Temps de réponse API réduit de 25%' },
        { type: 'improvement', text: 'Cache optimisé pour les requêtes fréquentes' },
        { type: 'fix', text: 'Correction des erreurs 500 intermittentes' },
        { type: 'fix', text: 'Résolution du problème de synchronisation des soldes' }
      ]
    },
    {
      version: '2.3.0',
      date: '2025-12-05',
      type: 'minor',
      title: 'Cartes virtuelles et QR codes',
      changes: [
        { type: 'feature', text: 'Génération de cartes virtuelles Visa/Mastercard' },
        { type: 'feature', text: 'Paiements par QR code dynamiques' },
        { type: 'feature', text: 'API de gestion des cartes' },
        { type: 'improvement', text: 'Interface mobile optimisée' },
        { type: 'security', text: 'Chiffrement renforcé des données sensibles' }
      ]
    },
    {
      version: '2.2.0',
      date: '2025-11-18',
      type: 'minor',
      title: 'Tontines et épargne collective',
      changes: [
        { type: 'feature', text: 'Module de gestion des tontines' },
        { type: 'feature', text: 'Épargne programmée automatique' },
        { type: 'feature', text: 'Notifications push pour les échéances' },
        { type: 'improvement', text: 'Dashboard avec graphiques de suivi' }
      ]
    }
  ];

  const getTypeIcon = (type) => {
    switch (type) {
      case 'feature':
        return <Plus className="w-4 h-4 text-secondary" />;
      case 'improvement':
        return <Zap className="w-4 h-4 text-primary" />;
      case 'fix':
        return <Bug className="w-4 h-4 text-yellow-500" />;
      case 'security':
        return <Shield className="w-4 h-4 text-red-500" />;
      case 'breaking':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
      default:
        return <CheckCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getTypeLabel = (type) => {
    switch (type) {
      case 'feature':
        return 'Nouvelle fonctionnalité';
      case 'improvement':
        return 'Amélioration';
      case 'fix':
        return 'Correction';
      case 'security':
        return 'Sécurité';
      case 'breaking':
        return 'Breaking change';
      default:
        return 'Changement';
    }
  };

  const getVersionBadge = (type) => {
    switch (type) {
      case 'major':
        return 'bg-secondary/20 text-secondary';
      case 'minor':
        return 'bg-primary/20 text-primary';
      case 'patch':
        return 'bg-gray-700 text-gray-300';
      default:
        return 'bg-gray-700 text-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Sparkles className="w-5 h-5" />
              <span className="font-semibold">Mises à jour</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              CHANGELOG
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Suivez l'évolution de la plateforme uFaranga et découvrez les nouvelles fonctionnalités
            </p>
            <div className="flex items-center justify-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-secondary"></div>
                <span className="text-gray-400">Version majeure</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary"></div>
                <span className="text-gray-400">Version mineure</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-gray-700"></div>
                <span className="text-gray-400">Patch</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              {/* Vertical line */}
              <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-800"></div>

              {/* Releases */}
              <div className="space-y-12">
                {releases.map((release, index) => (
                  <div key={release.version} className="relative pl-20">
                    {/* Timeline dot */}
                    <div className={`absolute left-0 w-16 h-16 rounded-full border-4 border-black flex items-center justify-center ${
                      release.type === 'major' ? 'bg-secondary' :
                      release.type === 'minor' ? 'bg-primary' :
                      'bg-gray-700'
                    }`}>
                      <Sparkles className="w-6 h-6 text-black" />
                    </div>

                    {/* Content */}
                    <div className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <div className="flex items-center gap-3 mb-2">
                            <span className={`px-4 py-1 rounded-full text-sm font-bold ${getVersionBadge(release.type)}`}>
                              v{release.version}
                            </span>
                            <span className="text-sm text-gray-500 flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              {new Date(release.date).toLocaleDateString('fr-FR', { 
                                day: 'numeric', 
                                month: 'long', 
                                year: 'numeric' 
                              })}
                            </span>
                          </div>
                          <h2 className="text-2xl font-bold">{release.title}</h2>
                        </div>
                      </div>

                      <div className="space-y-3">
                        {release.changes.map((change, idx) => (
                          <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-gray-900/50">
                            {getTypeIcon(change.type)}
                            <div className="flex-1">
                              <div className="text-xs text-gray-500 mb-1">{getTypeLabel(change.type)}</div>
                              <div className="text-sm">{change.text}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Load more */}
            <div className="text-center mt-12">
              <button className="border border-gray-700 px-8 py-3 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center gap-2">
                Voir les versions précédentes
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Subscribe */}
      <section className="py-20 bg-gradient-to-b from-black to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-secondary/30 rounded-xl p-12 text-center bg-gradient-to-r from-secondary/10 to-primary/10">
            <Sparkles className="w-16 h-16 text-secondary mx-auto mb-6" />
            <h2 className="text-4xl font-anton uppercase mb-4">RESTEZ INFORMÉ</h2>
            <p className="text-xl text-gray-300 mb-8">
              Recevez les notifications des nouvelles versions par email
            </p>
            <div className="max-w-md mx-auto flex gap-3">
              <input
                type="email"
                placeholder="votre@email.com"
                className="flex-1 bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-secondary focus:outline-none"
              />
              <button className="bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
                S'abonner
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Links */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6">
            <a
              href="/developpeurs"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <Code className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Documentation API</h3>
              <p className="text-sm text-gray-400">Guides et références complètes</p>
            </a>

            <a
              href="/tutoriels"
              className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors"
            >
              <Code className="w-8 h-8 text-secondary mb-3" />
              <h3 className="font-bold mb-2">Tutoriels</h3>
              <p className="text-sm text-gray-400">Guides pas à pas</p>
            </a>

            <a
              href="/support"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <Shield className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Support</h3>
              <p className="text-sm text-gray-400">Aide et assistance</p>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Changelog;
