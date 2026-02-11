import {
  Shield, Lock, Eye, Bell, Building2, CreditCard,
  CheckCircle, AlertTriangle, FileCheck, Users,
  Server, Key, Smartphone, Globe
} from 'lucide-react';

const Security = () => {
  const securityFeatures = [
    {
      icon: Lock,
      title: 'Chiffrement de bout en bout',
      description: 'Toutes vos données sont chiffrées avec les standards les plus élevés (AES-256)'
    },
    {
      icon: Smartphone,
      title: 'Authentification à deux facteurs',
      description: 'Protection supplémentaire avec 2FA pour sécuriser votre compte'
    },
    {
      icon: Eye,
      title: 'Surveillance 24/7',
      description: 'Notre équipe surveille les activités suspectes en temps réel'
    },
    {
      icon: Bell,
      title: 'Alertes instantanées',
      description: 'Notifications immédiates pour chaque transaction'
    },
    {
      icon: Building2,
      title: 'Régulation bancaire',
      description: 'Régulé par la Banque de la République du Burundi (BRB)'
    },
    {
      icon: CreditCard,
      title: 'Protection des paiements',
      description: 'Vos transactions sont protégées contre la fraude'
    }
  ];

  const certifications = [
    { name: 'PCI DSS Level 1', icon: FileCheck },
    { name: 'ISO 27001', icon: Shield },
    { name: 'SOC 2 Type II', icon: Server },
    { name: 'GDPR Compliant', icon: Globe }
  ];

  const dosList = [
    'Utilisez un code PIN fort et unique',
    'Activez l\'authentification à deux facteurs',
    'Vérifiez régulièrement vos transactions',
    'Mettez à jour l\'application régulièrement',
    'Déconnectez-vous après chaque session',
    'Utilisez un mot de passe différent pour chaque service'
  ];

  const dontsList = [
    'Ne partagez jamais votre code PIN',
    'N\'utilisez pas de réseaux WiFi publics non sécurisés',
    'Ne cliquez pas sur des liens suspects',
    'Ne donnez jamais vos identifiants par téléphone',
    'N\'enregistrez pas vos mots de passe dans le navigateur',
    'Ne répondez pas aux emails suspects'
  ];

  const securityStats = [
    { value: '99.99%', label: 'Disponibilité' },
    { value: '256-bit', label: 'Chiffrement' },
    { value: '24/7', label: 'Surveillance' },
    { value: '0', label: 'Failles de sécurité' }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Shield className="w-5 h-5" />
              <span className="font-semibold">Sécurité & Conformité</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              VOTRE SÉCURITÉ, NOTRE PRIORITÉ
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Nous utilisons les technologies les plus avancées pour protéger votre argent et vos données personnelles
            </p>
            
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12">
              {securityStats.map((stat, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="text-3xl font-bold text-primary mb-2">{stat.value}</div>
                  <div className="text-sm text-gray-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Security Features */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-4">
              COMMENT NOUS PROTÉGEONS VOTRE ARGENT
            </h2>
            <p className="text-center text-gray-400 mb-12">Technologies de sécurité de niveau bancaire</p>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {securityFeatures.map((feature, index) => (
                <div key={index} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-4">
                    <feature.icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="py-20 bg-gradient-to-b from-black to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-4">
              CERTIFICATIONS ET CONFORMITÉ
            </h2>
            <p className="text-center text-gray-400 mb-12">Conformes aux normes internationales les plus strictes</p>
            
            <div className="grid md:grid-cols-4 gap-6">
              {certifications.map((cert, index) => (
                <div
                  key={index}
                  className="border border-gray-800 rounded-xl p-6 text-center hover:border-secondary/50 transition-colors"
                >
                  <div className="w-16 h-16 rounded-full bg-secondary/20 flex items-center justify-center mx-auto mb-4">
                    <cert.icon className="w-8 h-8 text-secondary" />
                  </div>
                  <p className="font-bold">{cert.name}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Security Tips */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-4">
              CONSEILS DE SÉCURITÉ
            </h2>
            <p className="text-center text-gray-400 mb-12">Protégez votre compte avec ces bonnes pratiques</p>
            
            <div className="grid md:grid-cols-2 gap-6">
              {/* Do's */}
              <div className="border border-secondary/30 rounded-xl p-8 bg-gradient-to-br from-secondary/5 to-black">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-full bg-secondary/20 flex items-center justify-center">
                    <CheckCircle className="w-6 h-6 text-secondary" />
                  </div>
                  <h3 className="text-2xl font-bold">À FAIRE</h3>
                </div>
                <ul className="space-y-3">
                  {dosList.map((item, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <CheckCircle className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                      <span className="text-gray-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Don'ts */}
              <div className="border border-red-500/30 rounded-xl p-8 bg-gradient-to-br from-red-500/5 to-black">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center">
                    <AlertTriangle className="w-6 h-6 text-red-500" />
                  </div>
                  <h3 className="text-2xl font-bold">À NE PAS FAIRE</h3>
                </div>
                <ul className="space-y-3">
                  {dontsList.map((item, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <AlertTriangle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
                      <span className="text-gray-300">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Security Team */}
      <section className="py-20 bg-gradient-to-b from-secondary/5 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-gray-800 rounded-xl p-10 text-center">
            <Users className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-3xl font-anton uppercase mb-4">ÉQUIPE SÉCURITÉ DÉDIÉE</h2>
            <p className="text-gray-300 mb-6">
              Notre équipe de sécurité travaille 24/7 pour protéger vos fonds et détecter toute activité suspecte. 
              Nous utilisons l'intelligence artificielle et le machine learning pour identifier les menaces en temps réel.
            </p>
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div className="border border-gray-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-primary mb-1">50+</div>
                <div className="text-sm text-gray-400">Experts en sécurité</div>
              </div>
              <div className="border border-gray-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-primary mb-1">&lt;2min</div>
                <div className="text-sm text-gray-400">Temps de réponse</div>
              </div>
              <div className="border border-gray-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-primary mb-1">100%</div>
                <div className="text-sm text-gray-400">Transactions sécurisées</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <h2 className="text-4xl font-anton uppercase mb-4">UNE QUESTION SUR LA SÉCURITÉ ?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Notre équipe de sécurité est là pour vous répondre
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/support"
                className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2"
              >
                <Shield className="w-5 h-5" />
                Contactez-nous
              </a>
              <a
                href="/support"
                className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center justify-center gap-2"
              >
                <FileCheck className="w-5 h-5" />
                Centre d'aide
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Security;
