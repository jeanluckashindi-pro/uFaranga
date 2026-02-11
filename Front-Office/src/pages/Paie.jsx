import React, { useState } from 'react';
import { 
  Wallet, Users, Calendar, FileText, CheckCircle, Zap,
  DollarSign, Clock, Download, Send, Shield, Calculator,
  TrendingUp, AlertCircle, Settings, Eye, EyeOff, Percent,
  Building, Phone, Mail, MapPin, Award, Target
} from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Paie = () => {
  const [showSalaries, setShowSalaries] = useState(false);

  const features = [
    {
      icon: Calendar,
      title: 'Paiements programmés',
      description: 'Configurez vos cycles de paie (mensuel, bimensuel) et laissez le système gérer automatiquement',
      benefits: ['Calendrier personnalisable', 'Rappels automatiques', 'Validation en 1 clic']
    },
    {
      icon: FileText,
      title: 'Bulletins de paie',
      description: 'Génération automatique des bulletins conformes à la législation burundaise',
      benefits: ['Modèles personnalisables', 'Envoi par email/SMS', 'Archivage sécurisé']
    },
    {
      icon: Users,
      title: 'Gestion employés',
      description: 'Base de données centralisée avec toutes les informations de vos employés',
      benefits: ['Fiches complètes', 'Historique des paies', 'Documents RH']
    },
    {
      icon: Zap,
      title: 'Virements instantanés',
      description: 'Payez tous vos employés en un seul clic via leurs comptes uFaranga',
      benefits: ['Paiement groupé', 'Confirmation temps réel', 'Zéro frais bancaires']
    }
  ];

  const payrollStats = [
    {
      label: 'Masse salariale',
      value: showSalaries ? '8,500,000 FBU' : '•••••••',
      icon: DollarSign,
      color: 'text-blue-400',
      change: '+5.2%'
    },
    {
      label: 'Employés actifs',
      value: '24',
      icon: Users,
      color: 'text-green-400',
      change: '+2'
    },
    {
      label: 'Charges sociales',
      value: showSalaries ? '1,700,000 FBU' : '•••••••',
      icon: Calculator,
      color: 'text-orange-400',
      change: '+5.2%'
    },
    {
      label: 'Coût total',
      value: showSalaries ? '10,200,000 FBU' : '•••••••',
      icon: Wallet,
      color: 'text-purple-400',
      change: '+5.2%'
    }
  ];

  const employees = [
    { name: 'Jean Dupont', role: 'Directeur', salary: showSalaries ? 850000 : null, status: 'paid' },
    { name: 'Marie Uwimana', role: 'Comptable', salary: showSalaries ? 450000 : null, status: 'paid' },
    { name: 'David Nkurunziza', role: 'Commercial', salary: showSalaries ? 380000 : null, status: 'paid' },
    { name: 'Sophie Ndayisenga', role: 'Assistante', salary: showSalaries ? 320000 : null, status: 'pending' },
  ];

  const payrollComponents = [
    { name: 'Salaire de base', type: 'Fixe', taxable: true },
    { name: 'Primes', type: 'Variable', taxable: true },
    { name: 'Heures supplémentaires', type: 'Variable', taxable: true },
    { name: 'Allocations familiales', type: 'Fixe', taxable: false },
    { name: 'Transport', type: 'Fixe', taxable: false },
  ];

  const deductions = [
    { name: 'INSS (employé)', rate: '3.5%', description: 'Cotisation sociale obligatoire' },
    { name: 'INSS (employeur)', rate: '8.5%', description: 'Part patronale' },
    { name: 'IPR', rate: 'Progressif', description: 'Impôt sur le revenu' },
    { name: 'Avances', rate: 'Variable', description: 'Avances sur salaire' },
  ];

  const complianceItems = [
    'Conforme Code du Travail burundais',
    'Calcul automatique INSS',
    'Calcul automatique IPR',
    'Déclarations mensuelles',
    'Archivage légal 10 ans',
    'Piste d\'audit complète'
  ];

  const useCases = [
    {
      company: 'Restaurant "Le Gourmet"',
      employees: 15,
      challenge: 'Calculs manuels chronophages et erreurs fréquentes',
      solution: 'Automatisation complète de la paie',
      result: '20h/mois économisées, 0 erreur',
      savings: '500,000 FBU/an'
    },
    {
      company: 'Boutique "Fashion Style"',
      employees: 8,
      challenge: 'Retards de paiement et mécontentement',
      solution: 'Virements instantanés programmés',
      result: '100% de paiements à l\'heure',
      savings: 'Satisfaction employés +95%'
    },
    {
      company: 'Cabinet "Conseil Plus"',
      employees: 12,
      challenge: 'Gestion complexe des primes variables',
      solution: 'Système flexible de rémunération',
      result: 'Calculs automatiques précis',
      savings: '15h/mois économisées'
    }
  ];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        {/* Hero */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
                <Shield className="w-5 h-5" />
                <span className="font-semibold">Conforme INSS & IPR</span>
              </div>
              <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                GESTION DE LA PAIE
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Automatisez votre paie de A à Z. Calculs, bulletins, virements et déclarations sociales en quelques clics.
              </p>
              
              <div className="flex flex-wrap gap-4 mb-8">
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Calculs automatiques</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Virements groupés</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Bulletins auto</span>
                </div>
              </div>

              <div className="flex gap-4">
                <GradientButton>Essai gratuit 30 jours</GradientButton>
                <button className="px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
                  Voir la démo
                </button>
              </div>
            </div>

            {/* Mock Payroll Interface */}
            <GlassCard className="bg-black/60 border-white/10 p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-lg">Paie de Février 2024</h3>
                <button 
                  onClick={() => setShowSalaries(!showSalaries)}
                  className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                >
                  {showSalaries ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>

              {/* Mini Stats */}
              <div className="grid grid-cols-2 gap-3 mb-6">
                <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Employés</div>
                  <div className="font-bold text-blue-400">24</div>
                </div>
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Total</div>
                  <div className="font-bold text-green-400">
                    {showSalaries ? '10.2M FBU' : '•••••••'}
                  </div>
                </div>
              </div>

              {/* Mini Employee List */}
              <div className="space-y-2 mb-6">
                <div className="text-xs text-gray-400 mb-2">Employés</div>
                {employees.slice(0, 3).map((emp, i) => (
                  <div key={i} className="flex justify-between items-center bg-white/5 rounded-lg p-2">
                    <div>
                      <div className="text-xs font-semibold">{emp.name}</div>
                      <div className="text-xs text-gray-500">{emp.role}</div>
                    </div>
                    <div className="text-xs font-mono font-bold text-green-400">
                      {emp.salary ? `${emp.salary.toLocaleString()} FBU` : '•••••••'}
                    </div>
                  </div>
                ))}
              </div>

              <GradientButton className="w-full">
                <Send className="w-4 h-4 mr-2" />
                Payer tous les employés
              </GradientButton>
            </GlassCard>
          </div>
        </div>

        {/* Payroll Stats */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">VUE D'ENSEMBLE</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {payrollStats.map((stat, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className={`w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center ${stat.color}`}>
                    <stat.icon className="w-6 h-6" />
                  </div>
                  {stat.change && (
                    <div className="text-sm text-green-400">
                      {stat.change}
                    </div>
                  )}
                </div>
                <div className="text-sm text-gray-400 mb-1">{stat.label}</div>
                <div className="text-2xl font-bold">{stat.value}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-4">FONCTIONNALITÉS COMPLÈTES</h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Tout ce dont vous avez besoin pour gérer la paie de votre entreprise
          </p>
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-8 hover:border-primary/30 transition-all">
                <div className="flex gap-4 mb-6">
                  <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                    <feature.icon className="w-7 h-7 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                    <p className="text-gray-400">{feature.description}</p>
                  </div>
                </div>
                <div className="space-y-2">
                  {feature.benefits.map((benefit, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="w-4 h-4 text-secondary shrink-0" />
                      {benefit}
                    </div>
                  ))}
                </div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Payroll Components */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">ÉLÉMENTS DE RÉMUNÉRATION</h2>
          <div className="max-w-4xl mx-auto">
            <GlassCard className="bg-black/40 border-white/10 p-8">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-bold mb-4 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                    Éléments de paie
                  </h3>
                  <div className="space-y-3">
                    {payrollComponents.map((component, i) => (
                      <div key={i} className="flex items-center justify-between bg-white/5 rounded-lg p-3">
                        <div>
                          <div className="text-sm font-semibold">{component.name}</div>
                          <div className="text-xs text-gray-500">{component.type}</div>
                        </div>
                        <div className={`text-xs px-2 py-1 rounded ${
                          component.taxable ? 'bg-orange-500/20 text-orange-400' : 'bg-green-500/20 text-green-400'
                        }`}>
                          {component.taxable ? 'Imposable' : 'Non imposable'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-bold mb-4 flex items-center gap-2">
                    <Calculator className="w-5 h-5 text-red-400" />
                    Retenues & Charges
                  </h3>
                  <div className="space-y-3">
                    {deductions.map((deduction, i) => (
                      <div key={i} className="bg-white/5 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1">
                          <div className="text-sm font-semibold">{deduction.name}</div>
                          <div className="text-sm font-mono text-primary">{deduction.rate}</div>
                        </div>
                        <div className="text-xs text-gray-500">{deduction.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Compliance */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">CONFORMITÉ LÉGALE</h2>
          <GlassCard className="bg-black/40 border-white/10 p-8 max-w-4xl mx-auto">
            <div className="flex items-center gap-3 mb-6">
              <Shield className="w-8 h-8 text-secondary" />
              <div>
                <h3 className="font-bold text-xl">100% Conforme</h3>
                <p className="text-sm text-gray-400">Respect de toutes les obligations légales</p>
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {complianceItems.map((item, i) => (
                <div key={i} className="flex items-center gap-3 bg-white/5 rounded-lg p-4">
                  <CheckCircle className="w-5 h-5 text-secondary shrink-0" />
                  <span className="text-gray-300">{item}</span>
                </div>
              ))}
            </div>
          </GlassCard>
        </div>

        {/* Use Cases */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-4">ILS NOUS FONT CONFIANCE</h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Découvrez comment nos clients ont transformé leur gestion de la paie
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {useCases.map((useCase, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-8">
                <div className="flex items-center gap-3 mb-4">
                  <Building className="w-8 h-8 text-primary" />
                  <div>
                    <h4 className="font-bold">{useCase.company}</h4>
                    <div className="text-xs text-gray-400">{useCase.employees} employés</div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <h5 className="text-sm font-bold text-red-400 mb-1">Problème</h5>
                    <p className="text-sm text-gray-400">{useCase.challenge}</p>
                  </div>
                  <div>
                    <h5 className="text-sm font-bold text-blue-400 mb-1">Solution</h5>
                    <p className="text-sm text-gray-400">{useCase.solution}</p>
                  </div>
                  <div>
                    <h5 className="text-sm font-bold text-green-400 mb-1">Résultat</h5>
                    <p className="text-sm text-white font-semibold">{useCase.result}</p>
                  </div>
                  <div className="pt-3 border-t border-white/5">
                    <div className="text-xs text-gray-400">Économies</div>
                    <div className="text-secondary font-bold">{useCase.savings}</div>
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* How it Works */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">COMMENT ÇA MARCHE ?</h2>
          <div className="grid md:grid-cols-4 gap-6 max-w-5xl mx-auto">
            {[
              { step: '1', title: 'Ajoutez vos employés', desc: 'Importez ou saisissez les infos', icon: Users },
              { step: '2', title: 'Configurez la paie', desc: 'Salaires, primes, retenues', icon: Settings },
              { step: '3', title: 'Validez & Payez', desc: 'Un clic pour tout payer', icon: Send },
              { step: '4', title: 'Bulletins envoyés', desc: 'Automatiquement par email', icon: Mail }
            ].map((item, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 text-center">
                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center text-3xl font-anton text-primary mx-auto mb-4">
                  {item.step}
                </div>
                <item.icon className="w-8 h-8 text-primary mx-auto mb-3" />
                <h4 className="font-bold mb-2">{item.title}</h4>
                <p className="text-sm text-gray-400">{item.desc}</p>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Pricing */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">TARIFICATION SIMPLE</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <GlassCard className="bg-black/40 border-white/10 p-8">
              <h3 className="text-xl font-bold mb-2">Starter</h3>
              <div className="text-4xl font-anton text-primary mb-4">2K FBU<span className="text-lg text-gray-400">/employé/mois</span></div>
              <p className="text-gray-400 mb-6">Jusqu'à 10 employés</p>
              <ul className="space-y-3 mb-8">
                {['Calculs automatiques', 'Bulletins de paie', 'Virements groupés', 'Support email'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-secondary shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="w-full py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
                Commencer
              </button>
            </GlassCard>

            <GlassCard className="bg-gradient-to-br from-primary/20 to-blue-900/20 border-primary/30 p-8 relative">
              <div className="absolute top-4 right-4 bg-secondary text-black text-xs font-bold px-3 py-1 rounded-full">
                POPULAIRE
              </div>
              <h3 className="text-xl font-bold mb-2">Business</h3>
              <div className="text-4xl font-anton text-primary mb-4">1.5K FBU<span className="text-lg text-gray-400">/employé/mois</span></div>
              <p className="text-gray-400 mb-6">11 à 50 employés</p>
              <ul className="space-y-3 mb-8">
                {['Tout du plan Starter', 'Déclarations INSS', 'Multi-utilisateurs', 'API', 'Support prioritaire'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-secondary shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <GradientButton className="w-full">Essai gratuit 30 jours</GradientButton>
            </GlassCard>

            <GlassCard className="bg-black/40 border-white/10 p-8">
              <h3 className="text-xl font-bold mb-2">Enterprise</h3>
              <div className="text-4xl font-anton text-primary mb-4">Sur mesure</div>
              <p className="text-gray-400 mb-6">50+ employés</p>
              <ul className="space-y-3 mb-8">
                {['Tout du plan Business', 'Intégration ERP', 'Account manager', 'SLA garanti', 'Formation sur site'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-secondary shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="w-full py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
                Nous contacter
              </button>
            </GlassCard>
          </div>
        </div>

        {/* CTA */}
        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-12 text-center">
          <Wallet className="w-20 h-20 text-primary mx-auto mb-6" />
          <h2 className="text-4xl font-anton uppercase mb-4">PRÊT À SIMPLIFIER VOTRE PAIE ?</h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Rejoignez les centaines d'entreprises qui gèrent leur paie avec uFaranga
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
            <GradientButton className="text-lg px-8 py-4">
              Essai gratuit 30 jours
            </GradientButton>
            <button className="px-8 py-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
              Planifier une démo
            </button>
          </div>
          <p className="text-sm text-gray-400">
            Aucune carte bancaire requise • Configuration en 10 minutes • Support 24/7
          </p>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Paie;
