import {
  Shield, FileCheck, Lock, Eye, Globe, Building2,
  CheckCircle, AlertTriangle, Scale, Users, Server, Key, CreditCard
} from 'lucide-react';

const Conformite = () => {
  const certifications = [
    {
      name: 'PCI DSS Level 1',
      icon: CreditCard,
      description: 'Norme de sécurité des données de l\'industrie des cartes de paiement',
      status: 'Certifié',
      date: '2025',
      details: 'Conformité totale aux 12 exigences PCI DSS pour la protection des données de cartes'
    },
    {
      name: 'ISO 27001',
      icon: Shield,
      description: 'Système de management de la sécurité de l\'information',
      status: 'Certifié',
      date: '2024',
      details: 'Certification internationale pour la gestion de la sécurité des informations'
    },
    {
      name: 'SOC 2 Type II',
      icon: Server,
      description: 'Contrôles de sécurité, disponibilité et confidentialité',
      status: 'Certifié',
      date: '2025',
      details: 'Audit indépendant des contrôles de sécurité sur une période de 12 mois'
    },
    {
      name: 'RGPD',
      icon: Globe,
      description: 'Règlement Général sur la Protection des Données',
      status: 'Conforme',
      date: '2024',
      details: 'Conformité totale aux exigences européennes de protection des données'
    }
  ];

  const regulations = [
    {
      title: 'Banque de la République du Burundi (BRB)',
      icon: Building2,
      description: 'Régulé et supervisé par la banque centrale du Burundi',
      points: [
        'Licence d\'établissement de paiement',
        'Audits réguliers de conformité',
        'Rapports trimestriels obligatoires',
        'Réserves de capital réglementaires'
      ]
    },
    {
      title: 'Lutte contre le blanchiment (AML)',
      icon: Shield,
      description: 'Conformité aux normes internationales anti-blanchiment',
      points: [
        'Vérification d\'identité (KYC) obligatoire',
        'Surveillance des transactions suspectes',
        'Déclaration des opérations douteuses',
        'Formation continue des équipes'
      ]
    },
    {
      title: 'Protection des consommateurs',
      icon: Users,
      description: 'Respect des droits et protection des utilisateurs',
      points: [
        'Transparence des frais et conditions',
        'Service client accessible 24/7',
        'Processus de réclamation clair',
        'Assurance des dépôts'
      ]
    }
  ];

  const dataProtection = [
    {
      title: 'Chiffrement des données',
      icon: Lock,
      description: 'AES-256 pour les données au repos, TLS 1.3 pour les données en transit'
    },
    {
      title: 'Contrôle d\'accès',
      icon: Key,
      description: 'Authentification multi-facteurs et principe du moindre privilège'
    },
    {
      title: 'Audit et logs',
      icon: Eye,
      description: 'Traçabilité complète de toutes les opérations sensibles'
    },
    {
      title: 'Sauvegarde',
      icon: Server,
      description: 'Sauvegardes chiffrées quotidiennes avec rétention de 90 jours'
    }
  ];

  const compliance = [
    {
      category: 'Données personnelles',
      items: [
        'Collecte minimale des données',
        'Consentement explicite des utilisateurs',
        'Droit à l\'oubli et portabilité',
        'Notification des violations sous 72h'
      ]
    },
    {
      category: 'Transactions financières',
      items: [
        'Vérification d\'identité (KYC)',
        'Surveillance anti-fraude en temps réel',
        'Limites de transaction configurables',
        'Historique complet des opérations'
      ]
    },
    {
      category: 'Sécurité technique',
      items: [
        'Tests de pénétration trimestriels',
        'Mises à jour de sécurité automatiques',
        'Plan de continuité d\'activité',
        'Équipe de réponse aux incidents 24/7'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Shield className="w-5 h-5" />
              <span className="font-semibold">Conformité & Régulation</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              CONFORMITÉ RÉGLEMENTAIRE
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              uFaranga respecte les normes internationales les plus strictes en matière de sécurité, confidentialité et conformité financière
            </p>
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">CERTIFICATIONS</h2>
            <p className="text-gray-400 mb-12">Nos certifications et conformités internationales</p>

            <div className="grid md:grid-cols-2 gap-6">
              {certifications.map((cert, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center shrink-0">
                      <cert.icon className="w-7 h-7 text-primary" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="text-xl font-bold">{cert.name}</h3>
                        <span className="px-3 py-1 bg-secondary/20 text-secondary text-xs font-semibold rounded-full">
                          {cert.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400 mb-2">{cert.description}</p>
                      <p className="text-xs text-gray-500">Certifié depuis {cert.date}</p>
                    </div>
                  </div>
                  <div className="pt-4 border-t border-gray-800">
                    <p className="text-sm text-gray-300">{cert.details}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Regulations */}
      <section className="py-20 bg-gradient-to-b from-black to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">RÉGULATIONS</h2>
            <p className="text-gray-400 mb-12">Conformité aux autorités de régulation</p>

            <div className="space-y-6">
              {regulations.map((reg, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-12 h-12 rounded-lg bg-secondary/20 flex items-center justify-center shrink-0">
                      <reg.icon className="w-6 h-6 text-secondary" />
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold mb-2">{reg.title}</h3>
                      <p className="text-gray-400">{reg.description}</p>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    {reg.points.map((point, idx) => (
                      <div key={idx} className="flex items-start gap-3 p-4 rounded-lg bg-gray-900/50">
                        <CheckCircle className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                        <span className="text-sm">{point}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Data Protection */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">PROTECTION DES DONNÉES</h2>
            <p className="text-gray-400 mb-12">Mesures techniques de sécurité</p>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {dataProtection.map((item, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center mb-4">
                    <item.icon className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="font-bold mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-400">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Compliance Details */}
      <section className="py-20 bg-gradient-to-b from-secondary/5 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">PRATIQUES DE CONFORMITÉ</h2>
            <p className="text-gray-400 mb-12">Nos engagements au quotidien</p>

            <div className="grid md:grid-cols-3 gap-6">
              {compliance.map((cat, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6">
                  <h3 className="text-xl font-bold mb-4">{cat.category}</h3>
                  <ul className="space-y-3">
                    {cat.items.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <CheckCircle className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                        <span className="text-gray-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Reports */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <FileCheck className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-4xl font-anton uppercase mb-4">RAPPORTS DE CONFORMITÉ</h2>
            <p className="text-xl text-gray-300 mb-8">
              Téléchargez nos rapports d'audit et certificats de conformité
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2">
                <FileCheck className="w-5 h-5" />
                Rapports d'audit
              </button>
              <button className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center gap-2">
                <Scale className="w-5 h-5" />
                Documents légaux
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Contact */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6">
            <a
              href="/legal"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <Scale className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Mentions légales</h3>
              <p className="text-sm text-gray-400">CGU, politique de confidentialité</p>
            </a>

            <a
              href="/securite"
              className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors"
            >
              <Shield className="w-8 h-8 text-secondary mb-3" />
              <h3 className="font-bold mb-2">Sécurité</h3>
              <p className="text-sm text-gray-400">Mesures de protection</p>
            </a>

            <a
              href="/contact"
              className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors"
            >
              <Users className="w-8 h-8 text-primary mb-3" />
              <h3 className="font-bold mb-2">Contact</h3>
              <p className="text-sm text-gray-400">Questions sur la conformité</p>
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Conformite;
