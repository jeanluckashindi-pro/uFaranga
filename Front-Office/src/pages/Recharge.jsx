import React from 'react';
import { Smartphone, Zap, Clock, CheckCircle, Wifi } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Recharge = () => {
  const operators = [
    { name: 'Econet Leo', logo: '🦁', color: 'from-orange-500/20 to-red-500/20' },
    { name: 'Lumitel', logo: '📱', color: 'from-blue-500/20 to-cyan-500/20' },
    { name: 'Smart', logo: '⚡', color: 'from-green-500/20 to-emerald-500/20' },
  ];

  const quickAmounts = [1000, 2000, 5000, 10000, 20000, 50000];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
            <Smartphone className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Recharge Mobile</h1>
          <p className="text-xl text-gray-300 mb-8">
            Rechargez votre crédit mobile en quelques secondes, tous opérateurs
          </p>
        </div>

        <div className="max-w-2xl mx-auto mb-16">
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <h3 className="text-xl font-bold mb-6">Recharger maintenant</h3>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Opérateur</label>
                <div className="grid grid-cols-3 gap-4">
                  {operators.map((op, i) => (
                    <button key={i} className={`p-4 rounded-xl bg-gradient-to-br ${op.color} border border-white/10 hover:border-primary/30 transition-all text-center`}>
                      <div className="text-3xl mb-2">{op.logo}</div>
                      <div className="text-sm font-bold">{op.name}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Numéro de téléphone</label>
                <input
                  type="tel"
                  placeholder="+257 79 123 456"
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-400 mb-2">Montant (FBU)</label>
                <input
                  type="number"
                  placeholder="0"
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white text-2xl font-mono focus:outline-none focus:border-primary transition-colors"
                />
                <div className="grid grid-cols-3 gap-2 mt-3">
                  {quickAmounts.map(amount => (
                    <button key={amount} className="px-3 py-2 rounded-lg bg-white/5 text-sm text-gray-400 hover:bg-primary/20 hover:text-primary border border-white/10 transition-all">
                      {amount.toLocaleString()}
                    </button>
                  ))}
                </div>
              </div>

              <GradientButton className="w-full py-4 text-lg">
                Recharger maintenant
              </GradientButton>
            </div>
          </GlassCard>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Zap className="w-12 h-12 text-primary mx-auto mb-4" />
            <h4 className="font-bold mb-2">Instantané</h4>
            <p className="text-gray-400 text-sm">Crédit disponible en moins de 5 secondes</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <CheckCircle className="w-12 h-12 text-secondary mx-auto mb-4" />
            <h4 className="font-bold mb-2">Tous opérateurs</h4>
            <p className="text-gray-400 text-sm">Econet, Lumitel, Smart et plus</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Clock className="w-12 h-12 text-purple-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">24/7</h4>
            <p className="text-gray-400 text-sm">Disponible à tout moment</p>
          </GlassCard>
        </div>
      </Section>
    </div>
  );
};

export default Recharge;
