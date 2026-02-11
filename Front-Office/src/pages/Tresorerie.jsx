import React, { useState } from 'react';
import { 
  TrendingUp, DollarSign, BarChart3, Calendar, AlertTriangle,
  ArrowUpRight, ArrowDownRight, PieChart, LineChart, Bell,
  CheckCircle, Clock, Target, Wallet, CreditCard, Receipt,
  Download, Filter, Search, Eye, EyeOff, Zap, Shield
} from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Tresorerie = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  const features = [
    {
      icon: BarChart3,
      title: 'Tableau de bord en temps réel',
      description: 'Visualisez instantanément votre position de trésorerie avec des graphiques interactifs et des KPIs clés',
      benefits: ['Solde actuel', 'Flux entrants/sortants', 'Tendances mensuelles']
    },
    {
      icon: TrendingUp,
      title: 'Prévisions intelligentes',
      description: 'Algorithmes d\'IA qui analysent vos historiques pour prédire vos besoins futurs de trésorerie',
      benefits: ['Prévisions à 30/60/90 jours', 'Scénarios multiples', 'Alertes préventives']
    },
    {
      icon: Calendar,
      title: 'Planification budgétaire',
      description: 'Créez et suivez vos budgets par catégorie avec des alertes de dépassement automatiques',
      benefits: ['Budgets personnalisés', 'Suivi des écarts', 'Rapports mensuels']
    },
    {
      icon: Bell,
      title: 'Alertes intelligentes',
      description: 'Recevez des notifications proactives pour éviter les découverts et optimiser votre cash',
      benefits: ['Seuils personnalisables', 'Notifications SMS/Email', 'Recommandations']
    }
  ];

  const metrics = [
    {
      label: 'Solde actuel',
      value: '12,450,000 FBU',
      change: '+12.5%',
      trend: 'up',
      icon: Wallet,
      color: 'text-green-400'
    },
    {
      label: 'Entrées ce mois',
      value: '8,200,000 FBU',
      change: '+8.3%',
      trend: 'up',
      icon: ArrowUpRight,
      color: 'text-blue-400'
    },
    {
      label: 'Sorties ce mois',
      value: '5,750,000 FBU',
      change: '-3.2%',
      trend: 'down',
      icon: ArrowDownRight,
      color: 'text-orange-400'
    },
    {
      label: 'Prévision 30j',
      value: '14,800,000 FBU',
      change: '+18.9%',
      trend: 'up',
      icon: TrendingUp,
      color: 'text-purple-400'
    }
  ];

  const cashFlowData = [
    { month: 'Jan', entrees: 7500000, sorties: 5200000 },
    { month: 'Fév', entrees: 8100000, sorties: 5800000 },
    { month: 'Mar', entrees: 8200000, sorties: 5750000 },
  ];

  const categories = [
    { name: 'Ventes', amount: 8200000, percentage: 65, color: 'bg-green-500' },
    { name: 'Services', amount: 2800000, percentage: 22, color: 'bg-blue-500' },
    { name: 'Autres', amount: 1600000, percentage: 13, color: 'bg-purple-500' },
  ];

  const upcomingPayments = [
    { name: 'Salaires', amount: 2500000, date: '28 Fév', status: 'pending', priority: 'high' },
    { name: 'Loyer', amount: 500000, date: '01 Mar', status: 'pending', priority: 'high' },
    { name: 'Fournisseur A', amount: 1200000, date: '05 Mar', status: 'scheduled', priority: 'medium' },
    { name: 'Électricité', amount: 150000, date: '10 Mar', status: 'scheduled', priority: 'low' },
  ];

  const alerts = [
    {
      type: 'warning',
      title: 'Paiement important à venir',
      message: 'Salaires de 2,500,000 FBU prévus dans 3 jours',
      action: 'Voir détails'
    },
    {
      type: 'info',
      title: 'Opportunité d\'optimisation',
      message: 'Vous pourriez placer 3M FBU en épargne court terme',
      action: 'En savoir plus'
    }
  ];

  const tools = [
    {
      icon: PieChart,
      title: 'Analyse par catégorie',
      description: 'Comprenez où va votre argent avec des rapports détaillés par catégorie de dépenses'
    },
    {
      icon: LineChart,
      title: 'Graphiques de tendances',
      description: 'Visualisez l\'évolution de votre trésorerie sur différentes périodes'
    },
    {
      icon: Target,
      title: 'Objectifs financiers',
      description: 'Définissez des objectifs de trésorerie et suivez votre progression'
    },
    {
      icon: Download,
      title: 'Export comptable',
      description: 'Exportez vos données au format Excel, PDF ou vers votre logiciel comptable'
    }
  ];

  const useCases = [
    {
      type: 'PME',
      challenge: 'Difficulté à prévoir les besoins de trésorerie',
      solution: 'Prévisions automatiques basées sur l\'historique',
      result: '95% de précision sur les prévisions à 30 jours'
    },
    {
      type: 'Commerce',
      challenge: 'Gestion manuelle chronophage',
      solution: 'Automatisation complète du suivi',
      result: '10h/semaine économisées'
    },
    {
      type: 'Startup',
      challenge: 'Manque de visibilité sur le cash',
      solution: 'Dashboard temps réel avec alertes',
      result: 'Zéro découvert depuis 6 mois'
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
                <Zap className="w-5 h-5" />
                <span className="font-semibold">Pilotage financier intelligent</span>
              </div>
              <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                GESTION DE TRÉSORERIE
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Ne laissez plus jamais votre trésorerie vous surprendre. Anticipez, optimisez et prenez les bonnes décisions au bon moment.
              </p>
              
              <div className="flex flex-wrap gap-4 mb-8">
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Prévisions IA</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Alertes temps réel</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Export comptable</span>
                </div>
              </div>

              <div className="flex gap-4">
                <GradientButton>Essai gratuit 30 jours</GradientButton>
                <button className="px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
                  Voir la démo
                </button>
              </div>
            </div>

            {/* Mock Dashboard Preview */}
            <GlassCard className="bg-black/60 border-white/10 p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-lg">Tableau de bord</h3>
                <div className="flex gap-2">
                  <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Filter className="w-4 h-4" />
                  </button>
                  <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Mini Chart */}
              <div className="mb-6">
                <div className="flex justify-between items-end h-32 gap-2">
                  {cashFlowData.map((data, i) => (
                    <div key={i} className="flex-1 flex flex-col gap-1">
                      <div 
                        className="bg-green-500/30 rounded-t"
                        style={{ height: `${(data.entrees / 10000000) * 100}%` }}
                      ></div>
                      <div 
                        className="bg-red-500/30 rounded-t"
                        style={{ height: `${(data.sorties / 10000000) * 100}%` }}
                      ></div>
                      <div className="text-xs text-gray-500 text-center mt-1">{data.month}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white/5 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Solde</div>
                  <div className="font-bold text-green-400">12.4M FBU</div>
                </div>
                <div className="bg-white/5 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Prévision</div>
                  <div className="font-bold text-blue-400">+18.9%</div>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Metrics */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">VUE D'ENSEMBLE</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {metrics.map((metric, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className={`w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center ${metric.color}`}>
                    <metric.icon className="w-6 h-6" />
                  </div>
                  <div className={`flex items-center gap-1 text-sm ${metric.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                    {metric.trend === 'up' ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
                    {metric.change}
                  </div>
                </div>
                <div className="text-sm text-gray-400 mb-1">{metric.label}</div>
                <div className="text-2xl font-bold">{metric.value}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-4">FONCTIONNALITÉS CLÉS</h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Tous les outils dont vous avez besoin pour une gestion de trésorerie professionnelle
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

        {/* Alerts Section */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">ALERTES INTELLIGENTES</h2>
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {alerts.map((alert, i) => (
              <GlassCard key={i} className={`border-white/10 p-6 ${
                alert.type === 'warning' ? 'bg-orange-500/10 border-orange-500/30' : 'bg-blue-500/10 border-blue-500/30'
              }`}>
                <div className="flex gap-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center shrink-0 ${
                    alert.type === 'warning' ? 'bg-orange-500/20' : 'bg-blue-500/20'
                  }`}>
                    {alert.type === 'warning' ? (
                      <AlertTriangle className="w-6 h-6 text-orange-400" />
                    ) : (
                      <Bell className="w-6 h-6 text-blue-400" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-bold mb-1">{alert.title}</h4>
                    <p className="text-sm text-gray-300 mb-3">{alert.message}</p>
                    <button className="text-sm text-primary hover:text-primary/80 font-semibold">
                      {alert.action} →
                    </button>
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Upcoming Payments */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">PAIEMENTS À VENIR</h2>
          <GlassCard className="bg-black/40 border-white/10 p-0 overflow-hidden max-w-4xl mx-auto">
            <div className="p-6 border-b border-white/5 flex justify-between items-center">
              <h3 className="font-bold">Prochains 30 jours</h3>
              <div className="flex gap-2">
                <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                  <Search className="w-4 h-4" />
                </button>
                <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                  <Filter className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="divide-y divide-white/5">
              {upcomingPayments.map((payment, i) => (
                <div key={i} className="p-4 hover:bg-white/5 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        payment.priority === 'high' ? 'bg-red-500/20' :
                        payment.priority === 'medium' ? 'bg-orange-500/20' : 'bg-blue-500/20'
                      }`}>
                        <Receipt className={`w-5 h-5 ${
                          payment.priority === 'high' ? 'text-red-400' :
                          payment.priority === 'medium' ? 'text-orange-400' : 'text-blue-400'
                        }`} />
                      </div>
                      <div>
                        <div className="font-bold">{payment.name}</div>
                        <div className="text-sm text-gray-400 flex items-center gap-2">
                          <Calendar className="w-3 h-3" />
                          {payment.date}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-mono font-bold">{payment.amount.toLocaleString()} FBU</div>
                      <div className={`text-xs ${
                        payment.status === 'pending' ? 'text-orange-400' : 'text-blue-400'
                      }`}>
                        {payment.status === 'pending' ? 'En attente' : 'Programmé'}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 bg-white/5 text-center">
              <button className="text-sm text-gray-400 hover:text-white transition-colors">
                Voir tous les paiements →
              </button>
            </div>
          </GlassCard>
        </div>

        {/* Categories Breakdown */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">RÉPARTITION PAR CATÉGORIE</h2>
          <div className="max-w-4xl mx-auto">
            <GlassCard className="bg-black/40 border-white/10 p-8">
              <div className="space-y-6">
                {categories.map((category, i) => (
                  <div key={i}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold">{category.name}</span>
                      <span className="font-mono font-bold">{category.amount.toLocaleString()} FBU</span>
                    </div>
                    <div className="relative h-3 bg-white/5 rounded-full overflow-hidden">
                      <div 
                        className={`absolute inset-y-0 left-0 ${category.color} rounded-full transition-all duration-500`}
                        style={{ width: `${category.percentage}%` }}
                      ></div>
                    </div>
                    <div className="text-sm text-gray-400 mt-1">{category.percentage}% du total</div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Tools */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">OUTILS AVANCÉS</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {tools.map((tool, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 text-center hover:border-primary/30 transition-all cursor-pointer">
                <tool.icon className="w-12 h-12 text-primary mx-auto mb-4" />
                <h4 className="font-bold mb-2">{tool.title}</h4>
                <p className="text-sm text-gray-400">{tool.description}</p>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Use Cases */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-4">CAS D'UTILISATION</h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Découvrez comment nos clients optimisent leur trésorerie
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {useCases.map((useCase, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-8">
                <div className="inline-block px-3 py-1 bg-primary/20 text-primary rounded-full text-sm font-semibold mb-4">
                  {useCase.type}
                </div>
                <h4 className="font-bold mb-3 text-red-400">Problème</h4>
                <p className="text-sm text-gray-400 mb-4">{useCase.challenge}</p>
                <h4 className="font-bold mb-3 text-blue-400">Solution</h4>
                <p className="text-sm text-gray-400 mb-4">{useCase.solution}</p>
                <h4 className="font-bold mb-3 text-green-400">Résultat</h4>
                <p className="text-sm text-white font-semibold">{useCase.result}</p>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Pricing */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">TARIFICATION</h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <GlassCard className="bg-black/40 border-white/10 p-8">
              <h3 className="text-xl font-bold mb-2">Starter</h3>
              <div className="text-4xl font-anton text-primary mb-4">Gratuit</div>
              <p className="text-gray-400 mb-6">Pour les petites entreprises</p>
              <ul className="space-y-3 mb-8">
                {['Tableau de bord basique', 'Jusqu\'à 100 transactions/mois', 'Alertes email', 'Support email'].map((feature, i) => (
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
              <div className="text-4xl font-anton text-primary mb-4">50K FBU<span className="text-lg text-gray-400">/mois</span></div>
              <p className="text-gray-400 mb-6">Pour les PME en croissance</p>
              <ul className="space-y-3 mb-8">
                {['Tout du plan Starter', 'Transactions illimitées', 'Prévisions IA', 'Alertes SMS', 'Multi-utilisateurs', 'Support prioritaire'].map((feature, i) => (
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
              <p className="text-gray-400 mb-6">Pour les grandes entreprises</p>
              <ul className="space-y-3 mb-8">
                {['Tout du plan Business', 'API personnalisée', 'Intégration ERP', 'Account manager dédié', 'SLA garanti', 'Formation sur site'].map((feature, i) => (
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
          <Shield className="w-20 h-20 text-primary mx-auto mb-6" />
          <h2 className="text-4xl font-anton uppercase mb-4">PRÊT À OPTIMISER VOTRE TRÉSORERIE ?</h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Rejoignez les centaines d'entreprises qui pilotent leur trésorerie avec uFaranga
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
            Aucune carte bancaire requise • Configuration en 5 minutes • Support 24/7
          </p>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Tresorerie;
