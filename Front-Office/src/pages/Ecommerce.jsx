import React from 'react';
import { ShoppingCart, CreditCard, Package, TrendingUp } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Ecommerce = () => {
  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
            <ShoppingCart className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Solutions E-commerce</h1>
          <p className="text-xl text-gray-300 mb-8">
            Acceptez les paiements en ligne et développez votre boutique
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <CreditCard className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-bold mb-2">Paiements en ligne</h3>
            <p className="text-gray-400">Cartes, mobile money, virements</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <Package className="w-12 h-12 text-secondary mb-4" />
            <h3 className="text-xl font-bold mb-2">Gestion des commandes</h3>
            <p className="text-gray-400">Suivi complet du panier à la livraison</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <TrendingUp className="w-12 h-12 text-green-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Analytics avancés</h3>
            <p className="text-gray-400">Optimisez vos ventes</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <ShoppingCart className="w-12 h-12 text-purple-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Plugins e-commerce</h3>
            <p className="text-gray-400">WooCommerce, Shopify, PrestaShop</p>
          </GlassCard>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Lancez votre boutique en ligne</h3>
          <GradientButton>Commencer maintenant</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Ecommerce;
