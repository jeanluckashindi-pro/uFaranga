import React from 'react';
import { Send, DollarSign, Users, TrendingUp, CheckCircle, Zap, Globe, Clock } from 'lucide-react';
import GlassCard from '../../components/ui/GlassCard';
import GradientButton from '../../components/ui/GradientButton';
import Section from '../../components/ui/Section';

const Transferts = () => {
  const features = [
    {
      icon: Send,
      title: 'Transferts nationaux',
      description: 'Envoyez de l\'argent partout au Burundi instantanément',
      commission: '1.5% par transfert'
    },
    {
      icon: Globe,
      title: 'Transferts internationaux',
      description: 'Vers l\'Afrique de l\'Est et au-delà',
      commission: '2% par transfert'
    },
    {
      icon: Zap,
      title: 'Instantané',
      description: 'Argent disponible en moins de 5 secondes',
      commission: 'Temps réel'
    },
    {
      icon: Clock,
      title: 'Service 24/7',
      description: 'Disponible à tout moment pour vos clients',
      commission: 'Sans limite'
    }
  ];

  const benefits = [
    { value: '1.5%', label: 'Commission moyenne', icon: DollarSign },
    { value: '50-80', label: 'Transferts/jour', icon: Users },
    { value: '200K-350K', label: 'Revenus/mois', icon: TrendingUp }
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
            <Send className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Agent Transferts</h1>
          <p className="text-xl text-gray-300 mb-8">
            Facilitez les envois d'argent pour votre communauté et gagnez sur chaque transaction
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {benefits.map((benefit, i) => (
            <GlassCard key={i} className="bg-gradient-to-br from-primary/20 to-blue-900/20 border-primary/30 p-8 text-center">
              <benefit.icon className="w-12 h-12 text-primary mx-auto mb-4" />
              <div className="text-4xl font-anton text-white mb-2">{benefit.value}</div>
              <div className="text-gray-300">{benefit.label}</div>
            </GlassCard>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {features.map((feature, i) => (
            <GlassCard key={i} className="bg-black/40 border-white/10 p-8">
              <feature.icon className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-400 mb-4">{feature.description}</p>
              <div className="text-secondary font-semibold">{feature.commission}</div>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Comment ça marche ?</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { step: '1', text: 'Client vous donne les infos du bénéficiaire' },
              { step: '2', text: 'Vous saisissez le montant dans l\'app' },
              { step: '3', text: 'Bénéficiaire reçoit l\'argent instantanément' }
            ].map((item, i) => (
              <div key={i} className="text-center">
                <div className="w-12 h-12 rounded-full bg-primary/20 text-primary flex items-center justify-center mx-auto mb-3 font-bold text-xl">
                  {item.step}
                </div>
                <p className="text-gray-300">{item.text}</p>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-8 text-center">
          <h3 className="text-2xl font-bold mb-4">Devenez agent transferts</h3>
          <p className="text-gray-300 mb-6">Rejoignez notre réseau et commencez à gagner dès aujourd'hui</p>
          <GradientButton>Postuler maintenant</GradientButton>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Transferts;
