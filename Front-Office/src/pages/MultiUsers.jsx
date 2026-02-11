import React from 'react';
import { Users, Shield, CheckCircle, UserPlus, Settings } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const MultiUsers = () => {
  const roles = [
    { name: 'Administrateur', permissions: 'Accès complet', color: 'from-red-500/20 to-orange-500/20' },
    { name: 'Gestionnaire', permissions: 'Paiements et rapports', color: 'from-blue-500/20 to-cyan-500/20' },
    { name: 'Comptable', permissions: 'Lecture seule', color: 'from-green-500/20 to-emerald-500/20' },
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
            <Users className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Gestion Multi-utilisateurs</h1>
          <p className="text-xl text-gray-300 mb-8">
            Gérez votre équipe avec des rôles et permissions personnalisés
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {roles.map((role, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${role.color} border-white/10 p-8 text-center`}>
              <Shield className="w-12 h-12 text-white mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">{role.name}</h3>
              <p className="text-gray-300">{role.permissions}</p>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Fonctionnalités</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {['Rôles personnalisables', 'Permissions granulaires', 'Audit trail complet', 'Authentification 2FA'].map((feature, i) => (
              <div key={i} className="flex items-center gap-3 bg-white/5 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-secondary shrink-0" />
                <span className="text-gray-300">{feature}</span>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <UserPlus className="w-16 h-16 text-primary mx-auto mb-4" />
          <h3 className="text-2xl font-bold mb-4">Invitez votre équipe</h3>
          <p className="text-gray-300 mb-6">Ajoutez des membres et gérez leurs accès facilement</p>
          <GradientButton>Ajouter un utilisateur</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default MultiUsers;
