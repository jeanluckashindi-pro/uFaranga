import React from 'react';
import { Smartphone, Printer, QrCode, Wifi, Battery, Shield, Zap, Download } from 'lucide-react';
import GlassCard from '../../components/ui/GlassCard';
import GradientButton from '../../components/ui/GradientButton';
import Section from '../../components/ui/Section';

const Outils = () => {
  const tools = [
    {
      icon: Smartphone,
      title: 'Application Agent',
      description: 'Interface intuitive pour gérer toutes vos transactions',
      features: ['Dashboard en temps réel', 'Historique complet', 'Rapports quotidiens'],
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      icon: QrCode,
      title: 'QR Code personnalisé',
      description: 'Votre code unique pour recevoir les paiements',
      features: ['Affiche personnalisée', 'Stickers', 'Carte de visite'],
      color: 'from-purple-500/20 to-pink-500/20'
    },
    {
      icon: Printer,
      title: 'Imprimante thermique',
      description: 'Imprimez des reçus professionnels (optionnel)',
      features: ['Reçus instantanés', 'Logo personnalisé', 'Bluetooth'],
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      icon: Wifi,
      title: 'Connexion internet',
      description: 'Forfait data offert pour les agents actifs',
      features: ['5GB/mois gratuit', 'Connexion stable', 'Support technique'],
      color: 'from-orange-500/20 to-red-500/20'
    }
  ];

  const appFeatures = [
    'Tableau de bord en temps réel',
    'Gestion des transactions',
    'Historique complet',
    'Rapports automatiques',
    'Notifications push',
    'Mode hors ligne',
    'Support chat intégré',
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
            <Smartphone className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Outils Agent</h1>
          <p className="text-xl text-gray-300 mb-8">
            Tous les outils dont vous avez besoin pour réussir en tant qu'agent uFaranga
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {tools.map((tool, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${tool.color} border-white/10 p-8`}>
              <tool.icon className="w-12 h-12 text-white mb-4" />
              <h3 className="text-xl font-bold mb-2">{tool.title}</h3>
              <p className="text-gray-300 mb-4">{tool.description}</p>
              <ul className="space-y-2">
                {tool.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-gray-300">
                    <Zap className="w-4 h-4 text-secondary shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-16">
          <h2 className="text-3xl font-anton uppercase mb-6 text-center">FONCTIONNALITÉS DE L'APP</h2>
          <div className="grid md:grid-cols-4 gap-4">
            {appFeatures.map((feature, i) => (
              <div key={i} className="flex items-center gap-2 bg-white/5 rounded-lg p-3">
                <Shield className="w-4 h-4 text-secondary shrink-0" />
                <span className="text-sm text-gray-300">{feature}</span>
              </div>
            ))}
          </div>
        </GlassCard>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Battery className="w-12 h-12 text-green-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Mode économie</h4>
            <p className="text-sm text-gray-400">Optimisé pour économiser la batterie</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Wifi className="w-12 h-12 text-blue-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Mode hors ligne</h4>
            <p className="text-sm text-gray-400">Continuez à travailler sans internet</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Shield className="w-12 h-12 text-purple-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Sécurité maximale</h4>
            <p className="text-sm text-gray-400">Chiffrement de bout en bout</p>
          </GlassCard>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <Download className="w-16 h-16 text-primary mx-auto mb-4" />
          <h3 className="text-2xl font-bold mb-4">Téléchargez l'app agent</h3>
          <p className="text-gray-300 mb-6">Disponible sur Android et iOS</p>
          <div className="flex gap-4 justify-center">
            <GradientButton>Google Play</GradientButton>
            <button className="px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
              App Store
            </button>
          </div>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Outils;
