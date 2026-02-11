import React from 'react';
import { TrendingUp, PieChart, BarChart3, DollarSign, Shield, Target } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Investissements = () => {
  const investmentOptions = [
    {
      title: 'Obligations d\'État',
      return: '8-12%',
      risk: 'Faible',
      minAmount: '100,000 FBU',
      icon: Shield,
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      title: 'Fonds Communs',
      return: '12-18%',
      risk: 'Moyen',
      minAmount: '50,000 FBU',
      icon: PieChart,
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      title: 'Actions',
      return: '15-25%',
      risk: 'Élevé',
      minAmount: '200,000 FBU',
      icon: BarChart3,
      color: 'from-purple-500/20 to-pink-500/20'
    },
  ];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
            <TrendingUp className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Investissements</h1>
          <p className="text-xl text-gray-300 mb-8">
            Faites fructifier votre argent avec des investissements sécurisés et accessibles
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {investmentOptions.map((option, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${option.color} border-white/10 p-8 hover:scale-[1.02] transition-transform`}>
              <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center mb-6">
                <option.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-4">{option.title}</h3>
              <div className="space-y-3 mb-6">
                <div className="flex justify-between">
                  <span className="text-gray-400">Rendement annuel</span>
                  <span className="font-bold text-secondary">{option.return}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Risque</span>
                  <span className="font-bold">{option.risk}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Minimum</span>
                  <span className="font-bold text-primary">{option.minAmount}</span>
                </div>
              </div>
              <GradientButton className="w-full">Investir</GradientButton>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-3xl font-anton uppercase mb-6 text-center">Pourquoi investir avec uFaranga ?</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                <Target className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h4 className="font-bold mb-2">Accessible à tous</h4>
                <p className="text-gray-400">Commencez à investir avec aussi peu que 50,000 FBU</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-full bg-secondary/20 flex items-center justify-center shrink-0">
                <Shield className="w-6 h-6 text-secondary" />
              </div>
              <div>
                <h4 className="font-bold mb-2">Sécurisé et régulé</h4>
                <p className="text-gray-400">Tous nos produits sont approuvés par la BRB</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center shrink-0">
                <PieChart className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <h4 className="font-bold mb-2">Diversification facile</h4>
                <p className="text-gray-400">Répartissez vos investissements en un clic</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center shrink-0">
                <DollarSign className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <h4 className="font-bold mb-2">Retraits flexibles</h4>
                <p className="text-gray-400">Accédez à votre argent quand vous en avez besoin</p>
              </div>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Prêt à commencer ?</h3>
          <p className="text-gray-300 mb-6">Ouvrez votre compte d'investissement en moins de 5 minutes</p>
          <GradientButton className="mx-auto">Créer mon portefeuille</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Investissements;
