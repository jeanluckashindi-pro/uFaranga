import React from 'react';
import { GraduationCap, Video, BookOpen, Users, CheckCircle, Award, Clock, Target } from 'lucide-react';
import GlassCard from '../../components/ui/GlassCard';
import GradientButton from '../../components/ui/GradientButton';
import Section from '../../components/ui/Section';

const Formation = () => {
  const modules = [
    {
      title: 'Module 1: Introduction',
      duration: '30 min',
      topics: ['Présentation uFaranga', 'Rôle de l\'agent', 'Opportunités de revenus'],
      icon: BookOpen
    },
    {
      title: 'Module 2: Application Agent',
      duration: '1h',
      topics: ['Navigation', 'Gestion des transactions', 'Rapports'],
      icon: Video
    },
    {
      title: 'Module 3: Services',
      duration: '1h30',
      topics: ['Dépôts/Retraits', 'Transferts', 'Paiement factures', 'Recharge mobile'],
      icon: Target
    },
    {
      title: 'Module 4: Sécurité',
      duration: '45 min',
      topics: ['Prévention fraude', 'Gestion du cash', 'Procédures d\'urgence'],
      icon: Award
    }
  ];

  const benefits = [
    'Formation 100% gratuite',
    'Certificat officiel',
    'Support continu',
    'Mises à jour régulières',
    'Communauté d\'agents',
    'Webinaires mensuels'
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
            <GraduationCap className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Formation Agent</h1>
          <p className="text-xl text-gray-300 mb-8">
            Programme de formation complet pour devenir un agent uFaranga certifié
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {modules.map((module, i) => (
            <GlassCard key={i} className="bg-black/40 border-white/10 p-8">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
                  <module.icon className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-1">{module.title}</h3>
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <Clock className="w-4 h-4" />
                    {module.duration}
                  </div>
                </div>
              </div>
              <ul className="space-y-2">
                {module.topics.map((topic, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-sm text-gray-300">
                    <CheckCircle className="w-4 h-4 text-secondary shrink-0" />
                    {topic}
                  </li>
                ))}
              </ul>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-16">
          <h2 className="text-2xl font-bold mb-6 text-center">Avantages de la formation</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {benefits.map((benefit, i) => (
              <div key={i} className="flex items-center gap-3 bg-white/5 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-secondary shrink-0" />
                <span className="text-gray-300">{benefit}</span>
              </div>
            ))}
          </div>
        </GlassCard>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <GlassCard className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border-blue-500/30 p-8 text-center">
            <Video className="w-12 h-12 text-blue-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Formation en ligne</h4>
            <p className="text-sm text-gray-300">Vidéos et quiz interactifs</p>
          </GlassCard>
          <GlassCard className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 border-green-500/30 p-8 text-center">
            <Users className="w-12 h-12 text-green-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Sessions de groupe</h4>
            <p className="text-sm text-gray-300">Webinaires et ateliers pratiques</p>
          </GlassCard>
          <GlassCard className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 border-purple-500/30 p-8 text-center">
            <Award className="w-12 h-12 text-purple-400 mx-auto mb-4" />
            <h4 className="font-bold mb-2">Certification</h4>
            <p className="text-sm text-gray-300">Certificat officiel d'agent</p>
          </GlassCard>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Prêt à commencer votre formation ?</h3>
          <p className="text-gray-300 mb-6">Inscrivez-vous maintenant et devenez agent certifié en 2 jours</p>
          <GradientButton>S'inscrire à la formation</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Formation;
