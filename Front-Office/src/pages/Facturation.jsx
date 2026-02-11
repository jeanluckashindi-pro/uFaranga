import React from 'react';
import { FileText, Send, CheckCircle, Clock } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Facturation = () => {
  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
            <FileText className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Facturation</h1>
          <p className="text-xl text-gray-300 mb-8">
            Créez et envoyez des factures professionnelles en quelques clics
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <FileText className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-bold mb-2">Factures personnalisées</h3>
            <p className="text-gray-400">Modèles professionnels avec votre logo</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <Send className="w-12 h-12 text-secondary mb-4" />
            <h3 className="text-xl font-bold mb-2">Envoi automatique</h3>
            <p className="text-gray-400">Par email ou SMS directement</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <CheckCircle className="w-12 h-12 text-green-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Suivi des paiements</h3>
            <p className="text-gray-400">Statut en temps réel</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-8">
            <Clock className="w-12 h-12 text-orange-400 mb-4" />
            <h3 className="text-xl font-bold mb-2">Rappels automatiques</h3>
            <p className="text-gray-400">Pour les factures impayées</p>
          </GlassCard>
        </div>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Commencez à facturer</h3>
          <GradientButton>Créer ma première facture</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Facturation;
