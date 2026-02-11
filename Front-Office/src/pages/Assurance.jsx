import React from 'react';
import { Shield, Heart, Car, Home, Users, CheckCircle, Phone } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Assurance = () => {
  const insuranceTypes = [
    {
      title: 'Assurance Santé',
      icon: Heart,
      price: '5,000 FBU/mois',
      features: ['Consultations médicales', 'Médicaments essentiels', 'Hospitalisation d\'urgence'],
      color: 'from-red-500/20 to-pink-500/20'
    },
    {
      title: 'Assurance Mobile',
      icon: Phone,
      price: '2,000 FBU/mois',
      features: ['Vol et perte', 'Casse accidentelle', 'Remplacement rapide'],
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      title: 'Assurance Vie',
      icon: Users,
      price: '10,000 FBU/mois',
      features: ['Protection familiale', 'Capital décès', 'Assistance funéraire'],
      color: 'from-purple-500/20 to-indigo-500/20'
    },
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
            <Shield className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Assurance</h1>
          <p className="text-xl text-gray-300 mb-8">
            Protégez ce qui compte le plus pour vous avec nos assurances accessibles
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {insuranceTypes.map((insurance, i) => (
            <GlassCard key={i} className={`bg-gradient-to-br ${insurance.color} border-white/10 p-8 hover:scale-[1.02] transition-transform`}>
              <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center mb-6">
                <insurance.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold mb-2">{insurance.title}</h3>
              <div className="text-3xl font-anton text-primary mb-6">{insurance.price}</div>
              <ul className="space-y-3 mb-8">
                {insurance.features.map((feature, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-gray-300">
                    <CheckCircle className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <GradientButton className="w-full">Souscrire</GradientButton>
            </GlassCard>
          ))}
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8">
          <h2 className="text-3xl font-anton uppercase mb-6 text-center">Pourquoi choisir nos assurances ?</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="flex gap-4">
              <CheckCircle className="w-6 h-6 text-secondary shrink-0" />
              <div>
                <h4 className="font-bold mb-2">Souscription instantanée</h4>
                <p className="text-gray-400">Activez votre assurance en quelques clics depuis l'app</p>
              </div>
            </div>
            <div className="flex gap-4">
              <CheckCircle className="w-6 h-6 text-secondary shrink-0" />
              <div>
                <h4 className="font-bold mb-2">Paiement flexible</h4>
                <p className="text-gray-400">Payez mensuellement directement depuis votre solde</p>
              </div>
            </div>
            <div className="flex gap-4">
              <CheckCircle className="w-6 h-6 text-secondary shrink-0" />
              <div>
                <h4 className="font-bold mb-2">Déclaration simplifiée</h4>
                <p className="text-gray-400">Déclarez un sinistre en 2 minutes via l'application</p>
              </div>
            </div>
            <div className="flex gap-4">
              <CheckCircle className="w-6 h-6 text-secondary shrink-0" />
              <div>
                <h4 className="font-bold mb-2">Remboursement rapide</h4>
                <p className="text-gray-400">Recevez vos indemnités directement sur votre compte</p>
              </div>
            </div>
          </div>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Assurance;
