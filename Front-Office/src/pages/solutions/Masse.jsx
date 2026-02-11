import React from 'react';
import { Link } from 'react-router-dom';
import { Users, Send, Clock, CheckCircle, FileSpreadsheet, Zap, Shield, BarChart3 } from 'lucide-react';
import GlassCard from '../../components/ui/GlassCard';
import GradientButton from '../../components/ui/GradientButton';
import Section from '../../components/ui/Section';

const Masse = () => {
  const features = [
    {
      icon: FileSpreadsheet,
      title: 'Import Excel/CSV',
      description: 'Importez vos listes de bénéficiaires facilement'
    },
    {
      icon: Zap,
      title: 'Traitement instantané',
      description: 'Jusqu\'à 10,000 paiements en quelques secondes'
    },
    {
      icon: Shield,
      title: 'Validation automatique',
      description: 'Vérification des numéros et montants'
    },
    {
      icon: BarChart3,
      title: 'Rapports détaillés',
      description: 'Suivi en temps réel de chaque transaction'
    }
  ];

  const useCases = [
    {
      type: 'Paie des employés',
      volume: '500+ employés',
      frequency: 'Mensuel',
      savings: 'Économie de 95% du temps'
    },
    {
      type: 'Commissions agents',
      volume: '1,000+ agents',
      frequency: 'Hebdomadaire',
      savings: 'Zéro erreur de paiement'
    },
    {
      type: 'Remboursements clients',
      volume: '5,000+ clients',
      frequency: 'À la demande',
      savings: 'Traitement en 2 minutes'
    }
  ];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center mb-20">
            <div>
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-6">
                <Users className="w-8 h-8 text-primary" />
              </div>
              <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                PAIEMENTS EN MASSE
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Payez des milliers de personnes en un seul clic. Idéal pour la paie, les commissions et les remboursements.
              </p>
              
              <div className="space-y-3 mb-8">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span className="text-gray-300">Jusqu'à 10,000 paiements simultanés</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span className="text-gray-300">Traitement en moins de 5 minutes</span>
                </div>
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span className="text-gray-300">Tarif dégressif selon le volume</span>
                </div>
              </div>

              <GradientButton>Demander une démo</GradientButton>
            </div>

            <GlassCard className="bg-black/40 border-white/10 p-8">
              <h3 className="text-2xl font-semibold mb-6">Fonctionnalités clés</h3>
              <div className="space-y-4">
                {features.map((feature, idx) => (
                  <div key={idx} className="flex items-start gap-4 bg-white/5 rounded-xl p-4 hover:bg-white/10 transition-colors">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <feature.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold mb-1">{feature.title}</h4>
                      <p className="text-sm text-gray-400">{feature.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </GlassCard>
          </div>

          <div className="mb-20">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">CAS D'UTILISATION</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {useCases.map((useCase, idx) => (
                <GlassCard key={idx} className="bg-black/40 border-white/10 p-6">
                  <Send className="w-12 h-12 text-primary mb-4" />
                  <h3 className="text-xl font-semibold mb-4">{useCase.type}</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Volume</span>
                      <span className="text-white font-semibold">{useCase.volume}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Fréquence</span>
                      <span className="text-white font-semibold">{useCase.frequency}</span>
                    </div>
                    <div className="pt-3 border-t border-white/5">
                      <div className="text-secondary text-sm font-semibold">{useCase.savings}</div>
                    </div>
                  </div>
                </GlassCard>
              ))}
            </div>
          </div>

          <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
            <h3 className="text-3xl font-anton uppercase mb-4">TARIFICATION DÉGRESSIVE</h3>
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div>
                <div className="text-4xl font-anton text-primary mb-2">1.5%</div>
                <p className="text-gray-400">0 - 1,000 paiements/mois</p>
              </div>
              <div>
                <div className="text-4xl font-anton text-primary mb-2">1%</div>
                <p className="text-gray-400">1,000 - 10,000 paiements/mois</p>
              </div>
              <div>
                <div className="text-4xl font-anton text-primary mb-2">0.5%</div>
                <p className="text-gray-400">10,000+ paiements/mois</p>
              </div>
            </div>
            <GradientButton className="mt-8">Commencer maintenant</GradientButton>
          </GlassCard>
        </div>
      </Section>
    </div>
  );
};

export default Masse;
