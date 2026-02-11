import React from 'react';
import { BookOpen, Code, Zap, Shield, Search, FileText, Video, MessageCircle } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Docs = () => {
  const sections = [
    {
      title: 'Démarrage rapide',
      icon: Zap,
      color: 'from-blue-500/20 to-cyan-500/20',
      items: [
        'Créer un compte développeur',
        'Obtenir vos clés API',
        'Faire votre premier appel',
        'Tester en sandbox'
      ]
    },
    {
      title: 'API Reference',
      icon: Code,
      color: 'from-purple-500/20 to-pink-500/20',
      items: [
        'Authentification',
        'Paiements',
        'Transferts',
        'Webhooks'
      ]
    },
    {
      title: 'Guides',
      icon: BookOpen,
      color: 'from-green-500/20 to-emerald-500/20',
      items: [
        'Intégration e-commerce',
        'Paiements récurrents',
        'Gestion des erreurs',
        'Bonnes pratiques'
      ]
    },
    {
      title: 'Sécurité',
      icon: Shield,
      color: 'from-orange-500/20 to-red-500/20',
      items: [
        'Authentification OAuth',
        'Signature des webhooks',
        'Gestion des clés',
        'Conformité PCI-DSS'
      ]
    }
  ];

  const resources = [
    { icon: FileText, title: 'Documentation API', desc: 'Référence complète de l\'API' },
    { icon: Code, title: 'Exemples de code', desc: 'Snippets prêts à l\'emploi' },
    { icon: Video, title: 'Tutoriels vidéo', desc: 'Guides pas à pas' },
    { icon: MessageCircle, title: 'Support développeurs', desc: 'Aide en temps réel' }
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
            <BookOpen className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Documentation</h1>
          <p className="text-xl text-gray-300 mb-8">
            Tout ce dont vous avez besoin pour intégrer uFaranga
          </p>

          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher dans la documentation..."
              className="w-full bg-white/5 border border-white/10 rounded-xl pl-12 pr-4 py-4 text-white focus:outline-none focus:border-primary transition-colors"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {sections.map((section, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${section.color} border-white/10 p-8 hover:scale-[1.02] transition-transform cursor-pointer`}>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-lg bg-white/10 flex items-center justify-center">
                  <section.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold">{section.title}</h3>
              </div>
              <ul className="space-y-3">
                {section.items.map((item, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
                    {item}
                  </li>
                ))}
              </ul>
            </GlassCard>
          ))}
        </div>

        <div className="mb-16">
          <h2 className="text-3xl font-anton uppercase text-center mb-8">Ressources</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {resources.map((resource, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 text-center hover:border-primary/30 transition-all cursor-pointer">
                <resource.icon className="w-12 h-12 text-primary mx-auto mb-4" />
                <h4 className="font-bold mb-2">{resource.title}</h4>
                <p className="text-sm text-gray-400">{resource.desc}</p>
              </GlassCard>
            ))}
          </div>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Besoin d'aide ?</h3>
          <p className="text-gray-300 mb-6">Notre équipe de support est disponible 24/7 pour vous aider</p>
          <div className="flex gap-4 justify-center">
            <GradientButton>Contacter le support</GradientButton>
            <button className="px-6 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors">
              Rejoindre Discord
            </button>
          </div>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Docs;
