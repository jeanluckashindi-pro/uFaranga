import React from 'react';
import { Percent, Gift, TrendingUp, ShoppingBag, Zap, CheckCircle, Star, ArrowRight } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Cashback = () => {
  const cashbackPartners = [
    { name: 'Supermarchés', cashback: '2%', icon: ShoppingBag, color: 'text-green-400' },
    { name: 'Restaurants', cashback: '5%', icon: Gift, color: 'text-orange-400' },
    { name: 'Carburant', cashback: '1.5%', icon: Zap, color: 'text-blue-400' },
    { name: 'E-commerce', cashback: '3%', icon: TrendingUp, color: 'text-purple-400' },
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
            <Percent className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Cashback</h1>
          <p className="text-xl text-gray-300 mb-8">
            Gagnez de l'argent à chaque achat avec votre carte uFaranga
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <GlassCard className="bg-gradient-to-br from-primary/20 to-blue-900/20 border-primary/30 p-8">
            <Gift className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-2xl font-bold mb-4">Jusqu'à 5% de cashback</h3>
            <p className="text-gray-300">
              Recevez automatiquement un pourcentage de vos achats directement sur votre compte uFaranga.
            </p>
          </GlassCard>

          <GlassCard className="bg-black/40 border-white/10 p-8">
            <TrendingUp className="w-12 h-12 text-secondary mb-4" />
            <h3 className="text-2xl font-bold mb-4">Cumulez vos gains</h3>
            <p className="text-gray-300">
              Plus vous utilisez votre carte, plus vous gagnez. Aucune limite de gains mensuelle.
            </p>
          </GlassCard>
        </div>

        <div className="mb-16">
          <h2 className="text-3xl font-anton uppercase text-center mb-8">Nos partenaires cashback</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {cashbackPartners.map((partner, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 text-center hover:border-primary/30 transition-all">
                <div className={`w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4 ${partner.color}`}>
                  <partner.icon className="w-8 h-8" />
                </div>
                <h4 className="font-bold mb-2">{partner.name}</h4>
                <div className="text-2xl font-anton text-primary">{partner.cashback}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Comment ça marche ?</h3>
          <div className="grid md:grid-cols-3 gap-6 mt-8">
            <div>
              <div className="w-12 h-12 rounded-full bg-primary/20 text-primary flex items-center justify-center mx-auto mb-3 font-bold text-xl">1</div>
              <p className="text-gray-300">Payez avec votre carte uFaranga</p>
            </div>
            <div>
              <div className="w-12 h-12 rounded-full bg-primary/20 text-primary flex items-center justify-center mx-auto mb-3 font-bold text-xl">2</div>
              <p className="text-gray-300">Recevez votre cashback automatiquement</p>
            </div>
            <div>
              <div className="w-12 h-12 rounded-full bg-primary/20 text-primary flex items-center justify-center mx-auto mb-3 font-bold text-xl">3</div>
              <p className="text-gray-300">Utilisez vos gains comme vous voulez</p>
            </div>
          </div>
          <GradientButton className="mt-8">Activer le cashback</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Cashback;
