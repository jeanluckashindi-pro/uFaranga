import React from 'react';
import { Puzzle, ShoppingCart, Code, Download, CheckCircle, Zap } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Plugins = () => {
  const plugins = [
    {
      name: 'WooCommerce',
      logo: '🛒',
      description: 'Plugin officiel pour WordPress/WooCommerce',
      downloads: '5,000+',
      rating: 4.8,
      integration: '5 minutes',
      color: 'from-purple-500/20 to-pink-500/20'
    },
    {
      name: 'Shopify',
      logo: '🛍️',
      description: 'Application Shopify certifiée',
      downloads: '3,000+',
      rating: 4.9,
      integration: '3 minutes',
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      name: 'PrestaShop',
      logo: '🏪',
      description: 'Module PrestaShop compatible toutes versions',
      downloads: '2,000+',
      rating: 4.7,
      integration: '5 minutes',
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      name: 'Magento',
      logo: '🎯',
      description: 'Extension Magento 2.x',
      downloads: '1,000+',
      rating: 4.6,
      integration: '10 minutes',
      color: 'from-orange-500/20 to-red-500/20'
    },
  ];

  const features = [
    'Installation en un clic',
    'Configuration simplifiée',
    'Support multi-devises',
    'Webhooks automatiques',
    'Rapports intégrés',
    'Mises à jour automatiques'
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
            <Puzzle className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Plugins E-commerce</h1>
          <p className="text-xl text-gray-300 mb-8">
            Intégrez uFaranga à votre boutique en ligne en quelques clics
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {plugins.map((plugin, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${plugin.color} border-white/10 p-8 hover:scale-[1.02] transition-transform`}>
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="text-5xl">{plugin.logo}</div>
                  <div>
                    <h3 className="text-2xl font-bold">{plugin.name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-yellow-400">★</span>
                      <span className="text-sm text-gray-400">{plugin.rating} • {plugin.downloads} téléchargements</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <p className="text-gray-300 mb-6">{plugin.description}</p>
              
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <Zap className="w-4 h-4 text-secondary" />
                  <span>Installation: {plugin.integration}</span>
                </div>
              </div>

              <GradientButton className="w-full">
                <Download className="w-4 h-4 mr-2" />
                Télécharger
              </GradientButton>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-3xl font-anton uppercase mb-6 text-center">Fonctionnalités incluses</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {features.map((feature, i) => (
              <div key={i} className="flex items-center gap-3 bg-white/5 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-secondary shrink-0" />
                <span className="text-gray-300">{feature}</span>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <Code className="w-16 h-16 text-primary mx-auto mb-4" />
          <h3 className="text-2xl font-bold mb-4">Besoin d'une intégration personnalisée ?</h3>
          <p className="text-gray-300 mb-6">Notre équipe peut créer un plugin sur mesure pour votre plateforme</p>
          <GradientButton>Contacter l'équipe technique</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Plugins;
