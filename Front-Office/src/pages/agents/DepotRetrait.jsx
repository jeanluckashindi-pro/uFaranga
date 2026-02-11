import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Banknote, ArrowDownToLine, ArrowUpFromLine, DollarSign, 
  Shield, Clock, MapPin, CheckCircle, TrendingUp, Users,
  Smartphone, Award, Star, Zap
} from 'lucide-react';
import GlassCard from '../../components/ui/GlassCard';
import GradientButton from '../../components/ui/GradientButton';
import Section from '../../components/ui/Section';

const DepotRetrait = () => {
  const features = [
    {
      icon: ArrowDownToLine,
      title: 'Dépôts instantanés',
      description: 'Vos clients déposent du cash et reçoivent l\'argent sur leur compte en temps réel',
      commission: '1% par dépôt'
    },
    {
      icon: ArrowUpFromLine,
      title: 'Retraits rapides',
      description: 'Permettez à vos clients de retirer leur argent en quelques secondes',
      commission: '1% par retrait'
    },
    {
      icon: Shield,
      title: 'Sécurisé à 100%',
      description: 'Toutes les transactions sont protégées et traçables',
      commission: 'Assurance incluse'
    },
    {
      icon: Clock,
      title: 'Service 24/7',
      description: 'Vos clients peuvent effectuer des opérations à tout moment',
      commission: 'Pas de limite horaire'
    }
  ];

  const benefits = [
    {
      title: 'Revenus garantis',
      value: '300K - 500K BIF/mois',
      icon: DollarSign,
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      title: 'Transactions quotidiennes',
      value: '50 - 100 clients/jour',
      icon: Users,
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      title: 'Commission moyenne',
      value: '1% par transaction',
      icon: TrendingUp,
      color: 'from-purple-500/20 to-pink-500/20'
    }
  ];

  const requirements = [
    'Capital de départ: 500,000 BIF minimum',
    'Local commercial ou kiosque visible',
    'Smartphone Android/iOS récent',
    'Connexion internet stable',
    'Pièce d\'identité valide',
    'Casier judiciaire vierge'
  ];

  const steps = [
    {
      number: '1',
      title: 'Inscription',
      description: 'Remplissez le formulaire en ligne avec vos informations',
      duration: '5 min'
    },
    {
      number: '2',
      title: 'Vérification',
      description: 'Notre équipe vérifie votre dossier et votre local',
      duration: '24-48h'
    },
    {
      number: '3',
      title: 'Formation',
      description: 'Formation gratuite sur l\'app agent et les procédures',
      duration: '1 jour'
    },
    {
      number: '4',
      title: 'Activation',
      description: 'Recevez votre kit agent et commencez à gagner',
      duration: 'Immédiat'
    }
  ];

  const testimonials = [
    {
      name: 'Jean-Claude N.',
      location: 'Bujumbura, Buyenzi',
      avatar: 'JC',
      transactions: '80-100/jour',
      revenue: '450,000 BIF/mois',
      quote: 'Les dépôts-retraits représentent 70% de mon activité. C\'est très rentable!'
    },
    {
      name: 'Marie U.',
      location: 'Gitega Centre',
      avatar: 'MU',
      transactions: '60-80/jour',
      revenue: '380,000 BIF/mois',
      quote: 'Mes clients apprécient la rapidité. Je n\'ai jamais eu de problème.'
    }
  ];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        {/* Hero */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-2 bg-secondary/20 text-secondary px-4 py-2 rounded-full mb-6">
                <Award className="w-5 h-5" />
                <span className="font-semibold">Service le plus demandé</span>
              </div>
              <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                AGENT DÉPÔT & RETRAIT
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Devenez point de service cash pour votre communauté et gagnez jusqu'à 500,000 BIF par mois
              </p>
              
              <div className="flex flex-wrap gap-4 mb-8">
                <div className="bg-white/5 border border-white/10 rounded-xl p-4 flex-1 min-w-[150px]">
                  <div className="text-3xl font-anton text-secondary mb-1">1%</div>
                  <div className="text-sm text-gray-400">Commission/transaction</div>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-4 flex-1 min-w-[150px]">
                  <div className="text-3xl font-anton text-secondary mb-1">24/7</div>
                  <div className="text-sm text-gray-400">Service disponible</div>
                </div>
              </div>

              <GradientButton className="mb-4">Devenir agent maintenant</GradientButton>
              <p className="text-sm text-gray-400">
                Ou appelez-nous au <span className="text-white font-semibold">+257 79 000 000</span>
              </p>
            </div>

            <GlassCard className="bg-black/40 border-white/10 p-8">
              <h3 className="text-2xl font-bold mb-6 flex items-center gap-3">
                <Banknote className="w-8 h-8 text-primary" />
                Comment ça marche ?
              </h3>
              <div className="space-y-6">
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center shrink-0">
                    <ArrowDownToLine className="w-6 h-6 text-green-400" />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1">Dépôt</h4>
                    <p className="text-sm text-gray-400">
                      Client vous donne du cash → Vous créditez son compte via l'app → Vous gagnez 1%
                    </p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center shrink-0">
                    <ArrowUpFromLine className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1">Retrait</h4>
                    <p className="text-sm text-gray-400">
                      Client demande un retrait → Vous débitez son compte → Vous lui donnez le cash → Vous gagnez 1%
                    </p>
                  </div>
                </div>
                <div className="p-4 bg-secondary/10 border border-secondary/20 rounded-xl">
                  <div className="flex items-center gap-2 text-secondary font-bold mb-1">
                    <Zap className="w-5 h-5" />
                    Exemple de revenus
                  </div>
                  <p className="text-sm text-gray-300">
                    100 transactions/jour × 10,000 BIF moyen × 1% = <span className="text-white font-bold">10,000 BIF/jour</span>
                  </p>
                  <p className="text-xs text-gray-400 mt-2">
                    Soit environ <span className="text-secondary font-bold">300,000 BIF/mois</span>
                  </p>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>

        {/* Features */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">AVANTAGES DU SERVICE</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 hover:border-primary/30 transition-all">
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <feature.icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-400 mb-3">{feature.description}</p>
                <div className="text-xs text-secondary font-semibold">{feature.commission}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Benefits Stats */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">POTENTIEL DE REVENUS</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {benefits.map((benefit, i) => (
              <GlassCard key={i} className={`bg-gradient-to-br ${benefit.color} border-white/10 p-8 text-center`}>
                <benefit.icon className="w-16 h-16 text-white mx-auto mb-4" />
                <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                <div className="text-3xl font-anton text-white mb-2">{benefit.value}</div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Steps */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">COMMENT DEVENIR AGENT</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {steps.map((step, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6 text-center relative">
                <div className="w-16 h-16 rounded-full bg-secondary/20 flex items-center justify-center text-3xl font-anton text-secondary mx-auto mb-4">
                  {step.number}
                </div>
                <h3 className="text-lg font-bold mb-2">{step.title}</h3>
                <p className="text-sm text-gray-400 mb-3">{step.description}</p>
                <div className="inline-block bg-white/5 border border-white/10 px-3 py-1 rounded-full text-xs text-secondary">
                  {step.duration}
                </div>
                {i < steps.length - 1 && (
                  <div className="hidden md:block absolute top-8 -right-3 w-6 h-0.5 bg-secondary/30"></div>
                )}
              </GlassCard>
            ))}
          </div>
        </div>

        {/* Requirements */}
        <GlassCard className="bg-black/40 border-white/10 p-8 mb-20">
          <h2 className="text-3xl font-anton uppercase mb-6 flex items-center gap-3">
            <CheckCircle className="w-8 h-8 text-secondary" />
            CONDITIONS REQUISES
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {requirements.map((req, i) => (
              <div key={i} className="flex items-start gap-3 bg-white/5 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                <span className="text-gray-300">{req}</span>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Testimonials */}
        <div className="mb-20">
          <h2 className="text-4xl font-anton uppercase text-center mb-12">TÉMOIGNAGES D'AGENTS</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {testimonials.map((testimonial, i) => (
              <GlassCard key={i} className="bg-black/40 border-white/10 p-6">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-full bg-gradient-to-br from-secondary to-green-800 flex items-center justify-center text-white font-bold text-lg">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <h3 className="font-bold">{testimonial.name}</h3>
                    <div className="text-sm text-gray-400 flex items-center gap-1">
                      <MapPin className="w-3 h-3" />
                      {testimonial.location}
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-1 mb-3">
                  {[...Array(5)].map((_, idx) => (
                    <Star key={idx} className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  ))}
                </div>
                
                <p className="text-gray-300 text-sm mb-4 italic">"{testimonial.quote}"</p>
                
                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
                  <div>
                    <div className="text-secondary font-bold">{testimonial.transactions}</div>
                    <div className="text-xs text-gray-400">Transactions/jour</div>
                  </div>
                  <div>
                    <div className="text-secondary font-bold">{testimonial.revenue}</div>
                    <div className="text-xs text-gray-400">Revenus mensuels</div>
                  </div>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>

        {/* CTA */}
        <GlassCard className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20 p-12 text-center">
          <Smartphone className="w-20 h-20 text-primary mx-auto mb-6" />
          <h2 className="text-4xl font-anton uppercase mb-4">PRÊT À COMMENCER ?</h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Rejoignez les 2,000+ agents qui font confiance à uFaranga et transformez votre local en point de service financier
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <GradientButton className="text-lg px-8 py-4">
              Postuler maintenant
            </GradientButton>
            <Link to="/agents" className="px-8 py-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors font-bold">
              En savoir plus
            </Link>
          </div>
        </GlassCard>
      </Section>
    </div>
  );
};

export default DepotRetrait;
