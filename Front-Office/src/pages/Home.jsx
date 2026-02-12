import React from 'react';
import { Link } from 'react-router-dom';
import {
  Users, Building, Shield, Star, Smartphone, Send, Zap, Globe, Download,
  Wallet, Sparkles, CreditCard, TrendingUp, DollarSign, HandshakeIcon,
  Apple, PlayCircle, Lock, Clock, Award, CheckCircle, ArrowRight, Percent,
  Headphones, MapPin, ChevronRight, Bell, History, User, LayoutGrid,
  Quote
} from 'lucide-react';
import Section from '../components/ui/Section';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';

const Home = () => {

  const features = [
    {
      title: "Envoyer de l'argent 💰",
      desc: "À n'importe qui, instantanément. Plus besoin de vous déplacer, tout se fait depuis votre téléphone.",
      icon: Send,
      color: "bg-primary",
      highlight: (
        <div className="flex items-center gap-3 bg-white/5 p-3 rounded-lg">
          <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-xs">JD</div>
          <div className="text-sm">
            <p className="font-semibold text-white">À Maman</p>
            <p className="text-xs text-green-400">Envoyé</p>
          </div>
          <span className="ml-auto font-mono text-sm">- 50k</span>
        </div>
      )
    },
    {
      title: "Payer vos Factures 🧾",
      desc: "Eau, électricité, TV, internet... Fini les files d'attente interminables. Payez tout depuis votre salon.",
      icon: Zap,
      color: "bg-secondary",
      highlight: (
        <div className="flex gap-2">
          <span className="text-xs bg-white/5 px-2 py-1 rounded text-yellow-400 border border-white/5">Regideso</span>
          <span className="text-xs bg-white/5 px-2 py-1 rounded text-blue-400 border border-white/5">Canal+</span>
        </div>
      )
    },
    {
      title: "Dépôt & Retrait 🏧",
      desc: "Retirez ou déposez du cash facilement chez nos milliers d'agents agréés partout dans le pays.",
      icon: MapPin,
      color: "bg-purple-500",
    },
    {
      title: "Crédit Mobile 📲",
      desc: "Rechargez votre mobile ou celui d'un proche en quelques secondes, quelque soit l'opérateur.",
      icon: Smartphone,
      color: "bg-orange-500",
    },
    {
      title: "Épargne & Projets 🏦",
      desc: "Mettez de l'argent de côté automatiquement et réalisez vos rêves plus rapidement.",
      icon: TrendingUp,
      color: "bg-pink-500",
    },
    {
      title: "Paiement Marchand",
      desc: "Scannez et payez chez vos commerçants préférés sans toucher à du cash.",
      icon: CheckCircle,
      color: "bg-teal-500",
    }
  ];

  return (
    <div className="bg-black min-h-screen text-white overflow-x-hidden">

      {/* --- HERO SECTION --- */}
      <section className="relative min-h-screen flex items-center overflow-hidden py-20">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 z-0">
          <div className="absolute top-[-10%] right-[-5%] w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] animate-blob mix-blend-screen opacity-50"></div>
          <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-secondary/10 rounded-full blur-[100px] animate-blob delay-200 mix-blend-screen opacity-40"></div>
        </div>

        <div className="container mx-auto px-4 z-10 relative">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">

            {/* Left Content */}
            <div className="text-left space-y-8 animate-fade-in-up">
              <div className="space-y-4">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-md">
                  <span className="flex h-2 w-2 rounded-full bg-green-400 animate-pulse"></span>
                  <span className="text-sm font-medium tracking-wide text-gray-300">uFaranga, your money. Your bank.</span>
                </div>
                <h1 className="text-5xl md:text-7xl font-anton leading-[1.1] tracking-tight text-white uppercase">
                  Un seul système,une banque
                  <span className="text-white bg-clip-text bg-gradient-to-r from-primary via-blue-400 to-secondary bg-[length:300%_300%] animate-gradient" style={{ marginTop: '10px', display: 'block' }}>entièrement intégrée</span>
                </h1>
              </div>

              <p className="text-lg md:text-xl text-gray-400 font-light max-w-xl leading-relaxed">
                Envoyez et recevez de l'argent avec votre téléphone, <span className="text-white font-medium">sans compte bancaire</span>.
                Juste avec votre compte Uhuru. <br />
                <span className="italic text-gray-500 mt-2 block">Rapide, simple et entièrement sécurisé.</span>
              </p>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <button className="px-8 py-3.5 rounded-full bg-white text-black font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg shadow-white/10 flex items-center justify-center gap-2">
                  <User className="w-5 h-5" />
                  Se connecter
                </button>
                <button className="px-8 py-3.5 rounded-full bg-transparent border border-white/20 text-white font-bold text-lg hover:bg-white/10 transition-colors flex items-center justify-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Créer un compte
                </button>
              </div>

              <div className="pt-8 flex items-center gap-8 text-sm text-gray-500 font-medium">
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>Licence BRB</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-secondary" />
                  <span>500k+ Utilisateurs</span>
                </div>
              </div>
            </div>

            {/* Right Visual (Abstract Interface - Integrated System) */}
            <div className="relative hidden lg:block animate-fade-in-up delay-200 perspective-1000">
              <div className="relative z-10 transform rotate-y-12 rotate-x-6 transition-transform duration-500 hover:rotate-0">
                {/* Main Hub Card */}
                <GlassCard className="w-[380px] h-[550px] border-white/20 shadow-2xl bg-black/60 backdrop-blur-2xl rounded-[3rem] p-6 flex flex-col mx-auto relative z-20 overflow-hidden">

                  {/* Header */}
                  <div className="flex justify-between items-center mb-8">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary p-0.5">
                        <div className="w-full h-full bg-black rounded-full flex items-center justify-center text-xs font-bold">JD</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-400">Total Balance</div>
                        <div className="font-bold text-xl">2,450,000 <span className="text-xs text-secondary">BIF</span></div>
                      </div>
                    </div>
                    <div className="p-2 rounded-full bg-white/5 border border-white/10">
                      <Bell className="w-5 h-5 text-gray-400" />
                    </div>
                  </div>

                  {/* Central Pulse */}
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-primary/20 rounded-full blur-3xl animate-pulse-slow pointer-events-none"></div>

                  {/* Grid of Services (Integrated) */}
                  <div className="grid grid-cols-2 gap-4 flex-grow content-start relative z-10">
                    <div className="bg-white/5 hover:bg-white/10 p-4 rounded-2xl border border-white/5 transition-colors group cursor-pointer">
                      <div className="w-10 h-10 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                        <Send size={20} />
                      </div>
                      <div className="font-semibold text-sm">Envoyer</div>
                      <div className="text-[10px] text-gray-500">P2P Gratuit</div>
                    </div>
                    <div className="bg-white/5 hover:bg-white/10 p-4 rounded-2xl border border-white/5 transition-colors group cursor-pointer">
                      <div className="w-10 h-10 rounded-full bg-green-500/20 text-green-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                        <Zap size={20} />
                      </div>
                      <div className="font-semibold text-sm">Factures</div>
                      <div className="text-[10px] text-gray-500">Eau, Élec...</div>
                    </div>
                    <div className="bg-white/5 hover:bg-white/10 p-4 rounded-2xl border border-white/5 transition-colors group cursor-pointer">
                      <div className="w-10 h-10 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                        <TrendingUp size={20} />
                      </div>
                      <div className="font-semibold text-sm">Épargne</div>
                      <div className="text-[10px] text-gray-500">+5.0% / an</div>
                    </div>
                    <div className="bg-white/5 hover:bg-white/10 p-4 rounded-2xl border border-white/5 transition-colors group cursor-pointer">
                      <div className="w-10 h-10 rounded-full bg-orange-500/20 text-orange-400 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                        <CreditCard size={20} />
                      </div>
                      <div className="font-semibold text-sm">Cartes</div>
                      <div className="text-[10px] text-gray-500">Virtuelle</div>
                    </div>
                  </div>

                  {/* Bottom Tab */}
                  <div className="mt-auto h-16 bg-white/5 rounded-2xl border border-white/5 flex items-center justify-around text-gray-400">
                    <div className="p-2 text-white"><LayoutGrid size={24} /></div>
                    <div className="p-2 hover:text-white"><History size={24} /></div>
                    <div className="p-2 hover:text-white"><User size={24} /></div>
                  </div>
                </GlassCard>

                {/* Connecting Satellites */}
                <GlassCard className="absolute top-1/4 -left-12 p-3 flex items-center gap-3 animate-bounce shadow-xl border-secondary/30 bg-black/80 z-30">
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center text-black font-bold text-xs"><CheckCircle size={16} /></div>
                  <div className="text-xs font-bold whitespace-nowrap">Salaire Reçu <br /><span className="text-secondary font-normal">+ 500k</span></div>
                </GlassCard>

                <GlassCard className="absolute bottom-1/4 -right-12 p-3 flex items-center gap-3 animate-pulse-slow shadow-xl border-primary/30 bg-black/80 z-30">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white"><Globe size={16} /></div>
                  <div className="text-xs font-bold whitespace-nowrap">Paiement Online <br /><span className="text-gray-400 font-normal">Netflix, Amazon...</span></div>
                </GlassCard>

                {/* Connection Lines (Simulated with absolute divs) */}
                <div className="absolute top-1/4 left-0 w-12 h-[1px] bg-gradient-to-r from-secondary to-transparent -z-10"></div>
                <div className="absolute bottom-1/4 right-0 w-12 h-[1px] bg-gradient-to-l from-primary to-transparent -z-10"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- FEATURES SECTION (Instagram Story Style) --- */}
      <Section id="features" className="bg-black/50 overflow-hidden relative">
        <div className="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-black to-transparent z-10 pointer-events-none md:hidden"></div>
        <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-black to-transparent z-10 pointer-events-none md:hidden"></div>

        <div className="text-center mb-16 relative z-10 px-4">
          <h2 className="text-4xl md:text-5xl font-anton uppercase mb-4">Tout ce que vous pouvez faire</h2>
          <p className="text-gray-400 text-lg">Swipez pour découvrir vos super-pouvoirs.</p>
        </div>

        {/* Story Container */}
        <div className="flex overflow-x-auto snap-x snap-mandatory gap-6 pb-12 px-4 md:px-0 hide-scrollbar items-center justify-start md:justify-center">
          {[
            {
              title: "Envoyer de l'argent instantanément",
              img: "https://images.unsplash.com/photo-1556742049-0cfed4f7a07d?auto=format&fit=crop&w=800&q=80",
              desc: "Transférez des fonds à vos amis, votre famille ou vos partenaires en quelques secondes, où qu'ils soient.",
              highlight: "Gratuit entre amis"
            },
            {
              title: "Payer toutes vos factures",
              img: "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
              desc: "Électricité, eau, internet, abonnements TV... Réglez tout depuis votre canapé en un clic.",
              highlight: "Cashback 1%"
            },
            {
              title: "Épargner pour vos rêves",
              img: "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=800&q=80",
              desc: "Créez des cagnottes automatiques et regardez votre argent grandir jour après jour.",
              highlight: "Jusqu'à 5% d'intérêts"
            },
            {
              title: "Cartes Virtuelles & Physiques",
              img: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=800&q=80",
              desc: "Payez en ligne avec nos cartes virtuelles sécurisées ou commandez votre carte physique.",
              highlight: "Contrôle total"
            },
            {
              title: "Crédit & Avance sur salaire",
              img: "https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=800&q=80",
              desc: "Besoin d'un coup de pouce ? Obtenez une avance instantanée directement dans l'app.",
              highlight: "Approbation instantanée"
            }
          ].map((feature, idx) => (
            <div key={idx} className="snap-center shrink-0 relative group cursor-pointer transition-transform duration-300 hover:scale-[1.02]">
              {/* Story Card */}
              <GlassCard className="w-[300px] h-[520px] md:w-[360px] md:h-[600px] p-0 overflow-hidden flex flex-col justify-between border-white/10 bg-black relative">
                {/* Background Image */}
                <div className="absolute inset-0">
                  <img src={feature.img} alt={feature.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-90"></div>
                </div>

                {/* Story Progress Bars (Visual) */}
                <div className="absolute top-4 left-4 right-4 flex gap-1 z-20">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className={`h-1 flex-1 rounded-full bg-white/20 overflow-hidden`}>
                      <div className={`h-full bg-white ${i === 0 ? 'w-full' : 'w-0'}`}></div>
                    </div>
                  ))}
                </div>

                {/* Content Top */}
                <div className="p-8 pt-16 relative z-10">
                  <h3 className="text-3xl font-anton uppercase mb-2 leading-none drop-shadow-lg">{feature.title}</h3>
                </div>

                {/* Content Bottom */}
                <div className="p-8 relative z-10 mt-auto pt-12">
                  <p className="text-gray-300 text-lg leading-relaxed mb-6 font-medium drop-shadow-md">{feature.desc}</p>
                  {feature.highlight && (
                    <div className="inline-block py-2 px-4 rounded-xl bg-primary/80 border border-primary/50 backdrop-blur-md text-sm font-bold text-white mb-4">
                      {feature.highlight}
                    </div>
                  )}
                  <button className="w-full mt-4 py-3 rounded-xl bg-white text-black font-bold text-sm uppercase tracking-wider hover:bg-gray-200 transition-colors shadow-lg">
                    En savoir plus
                  </button>
                </div>
              </GlassCard>
            </div>
          ))}
        </div>
      </Section>

      {/* --- MISSION SECTION (Premium Bento Grid) --- */}
      <section className="py-24 bg-black relative">
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center mb-20">
            <h2 className="text-4xl md:text-6xl font-anton uppercase leading-tight mb-6">
              Pourquoi nous existons
            </h2>
            <p className="text-xl text-gray-400 font-light max-w-2xl mx-auto">
              Nous bâtissons l'infrastructure financière de demain pour l'Afrique d'aujourd'hui.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {/* Main Feature - Inclusion (Span 2 cols on Large) */}
            <GlassCard className="lg:col-span-2 p-8 md:p-12 relative overflow-hidden group bg-surface-50 border-white/10 hover:border-primary/30 transition-all duration-500">
              <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-primary/20 transition-all duration-500"></div>
              <div className="relative z-10">
                <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-300">
                  <Globe className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-3xl font-bold text-white mb-4">Inclusion Financière</h3>
                <p className="text-gray-400 text-lg leading-relaxed max-w-md">
                  En Afrique, le téléphone est plus répandu que le compte bancaire.
                  <span className="text-white block mt-2">Nous transformons chaque mobile en une agence bancaire complète.</span>
                </p>
              </div>
            </GlassCard>

            {/* Feature 2 - Rapidité */}
            <GlassCard className="p-8 relative overflow-hidden group bg-surface-50 border-white/10 hover:border-secondary/30 transition-all duration-500">
              <div className="absolute bottom-0 left-0 w-48 h-48 bg-secondary/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2 group-hover:bg-secondary/20 transition-all duration-500"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6">
                  <Zap className="w-7 h-7 text-secondary" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">Instantaneité</h3>
                <p className="text-gray-400">
                  L'argent voyage à la vitesse d'un SMS. Fini les délais de 3 jours.
                </p>
              </div>
            </GlassCard>

            {/* Feature 3 - Sécurité */}
            <GlassCard className="p-8 relative overflow-hidden group bg-surface-50 border-white/10 hover:border-blue-400/30 transition-all duration-500">
              <div className="absolute top-0 left-0 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl -translate-y-1/2 -translate-x-1/2 group-hover:bg-blue-500/20 transition-all duration-500"></div>
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6">
                  <Shield className="w-7 h-7 text-blue-400" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">Sécurité Bancaire</h3>
                <p className="text-gray-400">
                  Chiffrement de bout en bout et conformité aux standards internationaux.
                </p>
              </div>
            </GlassCard>

            {/* Feature 4 - Coûts (Span 2 cols on Large) */}
            <GlassCard className="lg:col-span-2 p-8 md:p-12 relative overflow-hidden group bg-surface-50 border-white/10 hover:border-green-400/30 transition-all duration-500">
              <div className="absolute bottom-0 right-0 w-64 h-64 bg-green-500/10 rounded-full blur-3xl translate-y-1/2 translate-x-1/2 group-hover:bg-green-500/20 transition-all duration-500"></div>
              <div className="relative z-10 flex flex-col md:flex-row gap-8 items-start md:items-center">
                <div className="flex-1">
                  <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                    <Percent className="w-8 h-8 text-green-400" />
                  </div>
                  <h3 className="text-3xl font-bold text-white mb-4">Zéro Frais Cachés</h3>
                  <p className="text-gray-400 text-lg leading-relaxed">
                    Nous croyons que vos services financiers doivent être transparents.
                    <span className="text-white"> Payez pour ce que vous utilisez, rien de plus.</span>
                  </p>
                </div>
                {/* Visual Element for Cost/Savings */}
                <div className="hidden md:flex flex-col gap-3 min-w-[200px]">
                  <div className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5">
                    <span className="text-sm text-gray-400">Banque Classique</span>
                    <span className="text-sm text-red-400 font-mono">- 3,500 BIF</span>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                    <span className="text-sm text-white font-bold">uFaranga</span>
                    <span className="text-sm text-green-400 font-mono font-bold">- 500 BIF</span>
                  </div>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* --- STATS SECTION --- */}
      <section className="py-20 border-y border-white/5 bg-black">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x divide-white/10">
            {[
              { value: '500K+', label: 'Utilisateurs' },
              { value: '50M+', label: 'Transactions' },
              { value: '<2s', label: 'Vitesse' },
              { value: '5', label: 'Pays' },
            ].map((stat, i) => (
              <div key={i} className="p-4">
                <div className="text-4xl md:text-5xl font-anton text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-600 mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-primary font-medium tracking-wider uppercase">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* --- SOCIAL PROOF (Testimonial Comments) --- */}
      <Section background="default" className="relative overflow-hidden">
        <div className="container mx-auto px-4 mb-16 text-center">
          <h2 className="text-4xl font-anton uppercase mb-4">Ils nous font confiance</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Rejoignez la communauté grandissante qui a choisi uFaranga pour sa simplicité et sa fiabilité.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 relative px-4">
          {/* Background decoration */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-primary/5 blur-3xl rounded-full pointer-events-none"></div>

          {[
            {
              name: "Marie K.",
              role: "Commerçante",
              comment: "Depuis que j'utilise uFaranga, mes clients me paient instantanément. Plus de problèmes de monnaie ou de retards. C'est un vrai soulagement pour mon commerce.",
              location: "Bujumbura",
              color: "text-primary"
            },
            {
              name: "Jean-Paul M.",
              role: "Étudiant",
              comment: "L'application est super fluide. Je reçois mon argent de poche de mes parents directement sur mon téléphone, sans frais cachés. Top !",
              location: "Gitega",
              color: "text-secondary"
            },
            {
              name: "Aisha N.",
              role: "Entrepreneur",
              comment: "La gestion de ma trésorerie est devenue un jeu d'enfant. J'ai une vue claire sur toutes mes dépenses et mes revenus en temps réel.",
              location: "Ngozi",
              color: "text-primary"
            },
            {
              name: "David B.",
              role: "Chauffeur",
              comment: "Payer l'essence est devenu si simple. Je n'ai plus besoin de transporter du liquide sur moi, ce qui est beaucoup plus sûr.",
              location: "Muyinga",
              color: "text-secondary"
            },
            {
              name: "Sophie T.",
              role: "Freelance",
              comment: "Recevoir des paiements internationaux était un cauchemar avant. Avec uFaranga, c'est rapide et sécurisé. Je recommande à 100%.",
              location: "Bujumbura",
              color: "text-primary"
            },
            {
              name: "Eric N.",
              role: "Agriculteur",
              comment: "Je peux payer mes fournisseurs et recevoir l'argent de mes récoltes sans me déplacer en ville. Un gain de temps précieux.",
              location: "Bubanza",
              color: "text-secondary"
            }
          ].map((t, i) => (
            <GlassCard key={i} className="flex flex-col h-full bg-black/40 hover:bg-black/60 border-white/5 hover:border-white/20 transition-all group">
              <div className="flex justify-between items-start mb-6">
                <div className="flex gap-1">
                  {[...Array(5)].map((_, idx) => (
                    <Star key={idx} className="w-4 h-4 fill-yellow-500 text-yellow-500" />
                  ))}
                </div>
                <Quote className={`w-8 h-8 ${t.color} opacity-20 group-hover:opacity-50 transition-opacity`} />
              </div>

              <p className="text-gray-300 text-lg leading-relaxed mb-6 flex-grow italic">"{t.comment}"</p>

              <div className="flex items-center gap-4 mt-auto border-t border-white/5 pt-4">
                <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${t.color === 'text-primary' ? 'from-primary to-blue-900' : 'from-secondary to-green-900'} flex items-center justify-center text-white font-bold shadow-lg`}>
                  {t.name.charAt(0)}
                </div>
                <div>
                  <div className="font-bold text-white">{t.name}</div>
                  <div className="text-xs text-gray-500">{t.role} • {t.location}</div>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>
      </Section>

      {/* --- APP SHOWCASE SECTION (Modern Content Approach) --- */}
      <section className="py-24 relative overflow-hidden bg-gradient-to-b from-black to-surface-100">
        <div className="container mx-auto px-4 relative z-10">
          <GlassCard className="rounded-[3rem] p-0 overflow-hidden border-white/10 bg-black/40">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              {/* Fake App Visual */}
              <div className="relative h-[500px] md:h-[600px] bg-gradient-to-b from-surface-100 to-black flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>
                {/* Abstract Phone */}
                <div className="relative w-[280px] h-[550px] bg-black border-8 border-gray-800 rounded-[3rem] shadow-2xl rotate-[-5deg] translate-y-12">
                  <div className="absolute top-0 left-0 right-0 h-full w-full bg-surface-100 rounded-[2.5rem] overflow-hidden flex flex-col">
                    {/* Screen Content Mockup */}
                    <div className="h-40 bg-primary p-6 flex flex-col justify-end">
                      <div className="text-white font-bold text-2xl">Bonjour, Jean</div>
                      <div className="text-white/80 text-sm">Bon retour parmi nous</div>
                    </div>
                    <div className="flex-1 bg-white p-4">
                      <div className="h-32 bg-gray-100 rounded-xl mb-4 animate-pulse"></div>
                      <div className="h-16 bg-gray-100 rounded-xl mb-2 animate-pulse delay-100"></div>
                      <div className="h-16 bg-gray-100 rounded-xl mb-2 animate-pulse delay-200"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-8 md:p-12 md:pr-20 space-y-8 text-center md:text-left">
                <div className="inline-block p-3 rounded-2xl bg-white/5 border border-white/10 mb-2">
                  <Smartphone className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-4xl md:text-6xl font-anton uppercase leading-tight">
                  Votre banque,<br /> <span className="text-primary">partout avec vous.</span>
                </h2>
                <p className="text-xl text-gray-400 font-light leading-relaxed">
                  Téléchargez uFaranga dès aujourd'hui et rejoignez la révolution financière.
                  Gérez votre argent, payez vos factures et épargnez pour l'avenir, le tout depuis votre poche.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start pt-4">
                  <button className="flex items-center justify-center gap-3 px-8 py-4 bg-white text-black rounded-xl font-bold text-lg hover:bg-gray-100 transition-colors shadow-lg shadow-white/10">
                    <Apple className="w-6 h-6" />
                    <div className="text-left">
                      <div className="text-[10px] uppercase font-bold text-gray-500 leading-none">Download on the</div>
                      <div className="leading-none">App Store</div>
                    </div>
                  </button>
                  <button className="flex items-center justify-center gap-3 px-8 py-4 bg-transparent border border-white/20 text-white hover:bg-white/5 rounded-xl font-bold text-lg transition-colors">
                    <PlayCircle className="w-6 h-6 text-white" />
                    <div className="text-left">
                      <div className="text-[10px] uppercase font-bold text-gray-400 leading-none">Get it on</div>
                      <div className="leading-none">Google Play</div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </section>

    </div>
  );
};

export default Home;
