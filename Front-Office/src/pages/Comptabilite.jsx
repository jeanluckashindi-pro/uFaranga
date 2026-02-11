import React, { useState } from 'react';
import { 
  Calculator, PieChart, FileText, TrendingUp, Download, 
  BookOpen, Receipt, CreditCard, Wallet, BarChart3,
  CheckCircle, Clock, Users, Building, Zap, Shield,
  ArrowUpRight, ArrowDownRight, DollarSign, Calendar,
  FileSpreadsheet, Printer, Mail, Settings, Eye, Filter
} from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Comptabilite = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('month');

  const features = [
    {
      icon: BookOpen,
      title: 'Plan comptable personnalisé',
      description: 'Adaptez votre plan comptable selon les normes burundaises (SYSCOHADA) ou créez le vôtre',
      benefits: ['Comptes pré-configurés', 'Personnalisation complète', 'Import/Export']
    },
    {
      icon: Receipt,
      title: 'Saisie automatique',
      description: 'Toutes vos transactions uFaranga sont automatiquement enregistrées en comptabilité',
      benefits: ['Zéro saisie manuelle', 'Synchronisation temps réel', 'Catégorisation IA']
    },
    {
      icon: FileText,
      title: 'Rapports réglementaires',
      description: 'Générez tous vos états financiers conformes aux normes en un clic',
      benefits: ['Bilan comptable', 'Compte de résultat', 'Grand livre', 'Balance générale']
    },
    {
      icon: Download,
      title: 'Export multi-formats',
      description: 'Exportez vos données vers Excel, PDF ou votre logiciel comptable préféré',
      benefits: ['Format FEC', 'Excel/CSV', 'PDF imprimable', 'API comptable']
    }
  ];

  const financialMetrics = [
    {
      label: 'Chiffre d\'affaires',
      value: '45,800,000 FBU',
      change: '+15.3%',
      trend: 'up',
      icon: TrendingUp,
      color: 'text-green-400',
      period: 'Ce mois'
    },
    {
      label: 'Charges',
      value: '28,500,000 FBU',
      change: '+5.2%',
      trend: 'up',
      icon: ArrowUpRight,
      color: 'text-orange-400',
      period: 'Ce mois'
    },
    {
      label: 'Résultat net',
      value: '17,300,000 FBU',
      change: '+32.8%',
      trend: 'up',
      icon: DollarSign,
      color: 'text-blue-400',
      period: 'Ce mois'
    },
    {
      label: 'Marge nette',
      value: '37.8%',
      change: '+2.1 pts',
      trend: 'up',
      icon: BarChart3,
      color: 'text-purple-400',
      period: 'Ce mois'
    }
  ];

  const recentTransactions = [
    { date: '11 Fév', description: 'Vente client ABC', account: '701000', debit: 0, credit: 2500000, balance: 2500000 },
    { date: '11 Fév', description: 'Achat fournitures', account: '601000', debit: 450000, credit: 0, balance: 2050000 },
    { date: '10 Fév', description: 'Salaires janvier', account: '661000', debit: 1800000, credit: 0, balance: 250000 },
    { date: '10 Fév', description: 'Loyer bureau', account: '613000', debit: 500000, credit: 0, balance: -250000 },
  ];

  const reports = [
    {
      name: 'Bilan comptable',
      description: 'Situation patrimoniale à une date donnée',
      icon: FileText,
      frequency: 'Mensuel',
      lastGenerated: 'Il y a 2 jours'
    },
    {
      name: 'Compte de résultat',
      description: 'Performance financière sur une période',
      icon: TrendingUp,
      frequency: 'Mensuel',
      lastGenerated: 'Il y a 2 jours'
    },
    {
      name: 'Grand livre',
      description: 'Détail de tous les comptes',
      icon: BookOpen,
      frequency: 'À la demande',
      lastGenerated: 'Il y a 5 jours'
    },
    {
      name: 'Balance générale',
      description: 'Soldes de tous les comptes',
      icon: Calculator,
      frequency: 'Mensuel',
      lastGenerated: 'Il y a 2 jours'
    },
    {
      name: 'Journal des ventes',
      description: 'Toutes les opérations de vente',
      icon: Receipt,
      frequency: 'Quotidien',
      lastGenerated: 'Aujourd\'hui'
    },
    {
      name: 'Journal des achats',
      description: 'Toutes les opérations d\'achat',
      icon: CreditCard,
      frequency: 'Quotidien',
      lastGenerated: 'Aujourd\'hui'
    }
  ];

  const integrations = [
    { name: 'Sage', logo: '📊', status: 'Disponible' },
    { name: 'QuickBooks', logo: '💼', status: 'Disponible' },
    { name: 'Excel', logo: '📈', status: 'Disponible' },
    { name: 'EBP', logo: '🏢', status: 'Disponible' },
  ];

  const complianceFeatures = [
    'Conforme SYSCOHADA',
    'Normes IFRS',
    'Déclarations fiscales',
    'TVA automatique',
    'Archivage légal 10 ans',
    'Piste d\'audit complète'
  ];

  const useCases = [
    {
      company: 'Restaurant "Le Gourmet"',
      sector: 'Restauration',
      challenge: 'Comptabilité manuelle chronophage',
      solution: 'Automatisation complète avec uFaranga',
      result: '15h/mois économisées',
      testimonial: 'Je me concentre enfin sur mon restaurant au lieu de passer mes soirées sur Excel'
    },
    {
      company: 'Boutique "Fashion Style"',
      sector: 'Commerce',
      challenge: 'Erreurs fréquentes dans les écritures',
      solution: 'Saisie automatique et contrôles',
      result: '99.9% de précision',
      testimonial: 'Plus aucune erreur depuis qu\'on utilise uFaranga. Mon comptable est ravi!'
    },
    {
      company: 'Cabinet "Conseil Plus"',
      sector: 'Services',
      challenge: 'Rapports mensuels difficiles à produire',
      solution: 'Génération automatique des états',
      result: 'Rapports en 2 clics',
      testimonial: 'Je génère tous mes rapports en quelques secondes. C\'est magique!'
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
                <span className="font-semibold">Conforme SYSCOHADA</span>
              </div>
              <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                COMPTABILITÉ AUTOMATISÉE
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Oubliez les saisies manuelles. Votre comptabilité se fait toute seule pendant que vous développez votre business.
              </p>
              
              <div className="flex flex-wrap gap-4 mb-8">
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Saisie automatique</span>
                </div>
                <div className="flex items-center gap-2 text-gray-300">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Rapports en 1 clic</span>
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

            {/* Mock Accounting Interface */}
            <GlassCard className="bg-black/60 border-white/10 p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-lg">Tableau de bord comptable</h3>
                <div className="flex gap-2">
                  <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Calendar className="w-4 h-4" />
                  </button>
                  <button className="p-2 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Mini Financial Summary */}
              <div className="grid grid-cols-2 gap-3 mb-6">
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Produits</div>
                  <div className="font-bold text-green-400">45.8M FBU</div>
                </div>
                <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Charges</div>
                  <div className="font-bold text-red-400">28.5M FBU</div>
                </div>
              </div>

              {/* Mini Transactions */}
              <div className="space-y-2">
                <div className="text-xs text-gray-400 mb-2">Dernières écritures</div>
                {[
                  { label: 'Vente client', amount: '+2.5M', color: 'text-green-400' },
                  { label: 'Achat fournitures', amount: '-450K', color: 'text-red-400' },
                  { label: 'Salaires', amount: '-1.8M', color: 'text-red-400' }
                ].map((tx, i) => (
                  <div key={i} className="flex justify-between items-center bg-white/5 rounded-lg p-2">
                    <span className="text-xs text-gray-300">{tx.label}</span>
                    <span className={`text-xs font-mono font-bold ${tx.color}`}>{tx.amount}</span>
                  </div>
                ))}
              </div>

              <div className="mt-4 pt-4 border-t border-white/5">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-400">Résultat net</span>
                  <span className="text-lg font-bold text-blue-400">17.3M FBU</span>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Financial Metrics */}
        <div className="mb-20">
          <h2 className="text-3xl font-anton uppercase text-center mb-12">INDICATEURS FINANCIERS</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {financialMetrics.map((metric, i) => (
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
                <div className="text-2xl font-bold mb-1">{metric.value}</div>
                <div className="text-xs text-gray-500">{metric.period}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-4">FONCTIONNALITÉS PRINCIPALES</h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Une solution comptable complète qui s'adapte à votre entreprise
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
      </Section>
    </div>
  );
};

export default Comptabilite;