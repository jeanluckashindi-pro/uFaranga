import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  CreditCard, Shield, Zap, Globe, Lock, Eye, EyeOff,
  Copy, Check, ShoppingCart, Wifi, AlertCircle, Plus,
  Trash2, Pause, Play, Settings, DollarSign, Calendar,
  User, Phone, Mail, ArrowRight, Smartphone, X
} from 'lucide-react';

const VirtualCard = () => {
  const [showCardDetails, setShowCardDetails] = useState(false);
  const [copiedField, setCopiedField] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [cards, setCards] = useState([]);
  const [formData, setFormData] = useState({
    cardName: '',
    cardType: 'visa',
    currency: 'BIF',
    monthlyLimit: '500000'
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const copyToClipboard = (text, field) => {
    navigator.clipboard.writeText(text.replace(/\s/g, ''));
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const generateCardNumber = (type) => {
    const prefix = type === 'visa' ? '4' : '5';
    let number = prefix;
    for (let i = 0; i < 15; i++) {
      number += Math.floor(Math.random() * 10);
    }
    return number.match(/.{1,4}/g).join(' ');
  };

  const handleCreateCard = () => {
    if (!formData.cardName.trim()) {
      alert('Veuillez entrer un nom pour votre carte');
      return;
    }

    const newCard = {
      id: Date.now(),
      name: formData.cardName,
      number: generateCardNumber(formData.cardType),
      expiry: `${String(new Date().getMonth() + 1).padStart(2, '0')}/${new Date().getFullYear() + 3}`,
      cvv: Math.floor(100 + Math.random() * 900).toString(),
      balance: 0,
      currency: formData.currency,
      status: 'active',
      type: formData.cardType,
      monthlyLimit: parseInt(formData.monthlyLimit),
      spent: 0,
      createdAt: new Date(),
      color: formData.cardType === 'visa' 
        ? 'from-blue-600 to-blue-800' 
        : 'from-orange-600 to-orange-800'
    };

    setCards([...cards, newCard]);
    setFormData({
      cardName: '',
      cardType: 'visa',
      currency: 'BIF',
      monthlyLimit: '500000'
    });
    setShowCreateModal(false);
  };

  const toggleCardStatus = (cardId) => {
    setCards(cards.map(card =>
      card.id === cardId
        ? { ...card, status: card.status === 'active' ? 'paused' : 'active' }
        : card
    ));
  };

  const deleteCard = (cardId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette carte ?')) {
      setCards(cards.filter(card => card.id !== cardId));
    }
  };

  const features = [
    {
      icon: Zap,
      title: 'Création instantanée',
      description: 'Votre carte est prête en 10 secondes'
    },
    {
      icon: Shield,
      title: '100% sécurisée',
      description: 'Chiffrement bancaire et 3D Secure'
    },
    {
      icon: Globe,
      title: 'Acceptée partout',
      description: 'Utilisable sur tous les sites e-commerce'
    },
    {
      icon: Lock,
      title: 'Contrôle total',
      description: 'Bloquez ou supprimez à tout moment'
    }
  ];

  const useCases = [
    {
      icon: ShoppingCart,
      title: 'Shopping en ligne',
      description: 'Amazon, AliExpress, eBay, Jumia...',
      examples: ['Amazon', 'AliExpress', 'eBay', 'Jumia']
    },
    {
      icon: Smartphone,
      title: 'Abonnements',
      description: 'Netflix, Spotify, YouTube Premium...',
      examples: ['Netflix', 'Spotify', 'YouTube', 'Apple Music']
    },
    {
      icon: Globe,
      title: 'Services internationaux',
      description: 'PayPal, Stripe, Google Play, App Store...',
      examples: ['PayPal', 'Google Play', 'App Store', 'Steam']
    }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left Content */}
              <div>
                <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
                  <CreditCard className="w-5 h-5" />
                  <span className="font-semibold">Carte Virtuelle</span>
                </div>
                <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
                  CARTE VIRTUELLE INSTANTANÉE
                </h1>
                <p className="text-xl text-gray-300 mb-8">
                  Créez une carte Visa/Mastercard virtuelle en 10 secondes. Liée à votre compte uFaranga pour vos achats en ligne.
                </p>

                <div className="grid grid-cols-2 gap-4 mb-8">
                  {features.map((feature, idx) => (
                    <div key={idx} className="flex items-start gap-3">
                      <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center shrink-0">
                        <feature.icon className="w-5 h-5 text-primary" />
                      </div>
                      <div>
                        <div className="font-semibold mb-1">{feature.title}</div>
                        <div className="text-sm text-gray-400">{feature.description}</div>
                      </div>
                    </div>
                  ))}
                </div>

                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
                >
                  <Plus className="w-5 h-5" />
                  Créer ma carte virtuelle
                </button>
              </div>

              {/* Right - Card Preview */}
              <div className="relative">
                {cards.length > 0 ? (
                  <div className={`bg-gradient-to-br ${cards[0].color} rounded-2xl p-8 shadow-2xl transform hover:scale-105 transition-transform`}>
                    <div className="flex justify-between items-start mb-12">
                      <Wifi className="w-12 h-12 text-white/80 rotate-90" />
                      <div className="text-white/80 text-sm font-semibold uppercase">
                        {cards[0].type === 'visa' ? 'VISA' : 'MASTERCARD'}
                      </div>
                    </div>

                    <div className="mb-8">
                      <div className="text-white text-2xl font-mono tracking-wider mb-2">
                        {showCardDetails ? cards[0].number : '•••• •••• •••• ' + cards[0].number.slice(-4)}
                      </div>
                      <div className="text-white/60 text-xs uppercase">{cards[0].name}</div>
                    </div>

                    <div className="flex justify-between items-end">
                      <div>
                        <div className="text-white/60 text-xs mb-1">Expire</div>
                        <div className="text-white font-mono">{cards[0].expiry}</div>
                      </div>
                      <div>
                        <div className="text-white/60 text-xs mb-1">CVV</div>
                        <div className="text-white font-mono">
                          {showCardDetails ? cards[0].cvv : '•••'}
                        </div>
                      </div>
                      <button
                        onClick={() => setShowCardDetails(!showCardDetails)}
                        className="text-white/80 hover:text-white transition-colors"
                      >
                        {showCardDetails ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="border-2 border-dashed border-gray-700 rounded-2xl p-12 text-center">
                    <CreditCard className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                    <p className="text-gray-500 mb-4">Aucune carte créée</p>
                    <button
                      onClick={() => setShowCreateModal(true)}
                      className="text-primary hover:underline"
                    >
                      Créer votre première carte
                    </button>
                  </div>
                )}

                {/* Decorative */}
                <div className="absolute -top-4 -right-4 w-72 h-72 bg-primary/10 rounded-full blur-3xl"></div>
                <div className="absolute -bottom-4 -left-4 w-72 h-72 bg-secondary/10 rounded-full blur-3xl"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* My Cards */}
      {cards.length > 0 && (
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-6xl mx-auto">
              <div className="flex items-center justify-between mb-12">
                <h2 className="text-4xl font-anton uppercase">MES CARTES</h2>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="border border-gray-700 px-6 py-3 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center gap-2"
                >
                  <Plus className="w-5 h-5" />
                  Nouvelle carte
                </button>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {cards.map((card) => (
                  <div key={card.id} className="border border-gray-800 rounded-xl overflow-hidden hover:border-primary/50 transition-colors">
                    {/* Card Visual */}
                    <div className={`bg-gradient-to-br ${card.color} p-6`}>
                      <div className="flex justify-between items-start mb-8">
                        <Wifi className="w-8 h-8 text-white/80 rotate-90" />
                        <div className="text-white/80 text-xs font-semibold uppercase">
                          {card.type === 'visa' ? 'VISA' : 'MASTERCARD'}
                        </div>
                      </div>

                      <div className="mb-6">
                        <div className="text-white text-lg font-mono tracking-wider mb-1">
                          •••• •••• •••• {card.number.slice(-4)}
                        </div>
                        <div className="text-white/60 text-xs uppercase">{card.name}</div>
                      </div>

                      <div className="flex justify-between items-end">
                        <div>
                          <div className="text-white/60 text-xs mb-1">Expire</div>
                          <div className="text-white text-sm font-mono">{card.expiry}</div>
                        </div>
                        <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          card.status === 'active'
                            ? 'bg-secondary/20 text-secondary'
                            : 'bg-gray-700 text-gray-300'
                        }`}>
                          {card.status === 'active' ? 'Active' : 'Pausée'}
                        </div>
                      </div>
                    </div>

                    {/* Card Info */}
                    <div className="p-6 space-y-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-400">Solde disponible</span>
                        <span className="font-bold">{card.balance.toLocaleString()} {card.currency}</span>
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-400">Limite mensuelle</span>
                        <span className="font-bold">{card.monthlyLimit.toLocaleString()} {card.currency}</span>
                      </div>

                      <div className="pt-4 border-t border-gray-800">
                        <div className="text-xs text-gray-500 mb-2">Dépensé ce mois</div>
                        <div className="w-full bg-gray-800 rounded-full h-2 mb-2">
                          <div
                            className="bg-primary h-2 rounded-full"
                            style={{ width: `${(card.spent / card.monthlyLimit) * 100}%` }}
                          ></div>
                        </div>
                        <div className="text-xs text-gray-400">
                          {card.spent.toLocaleString()} / {card.monthlyLimit.toLocaleString()} {card.currency}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-2 pt-4">
                        <button
                          onClick={() => toggleCardStatus(card.id)}
                          className="flex-1 border border-gray-700 px-4 py-2 rounded-lg hover:border-primary/50 transition-colors inline-flex items-center justify-center gap-2 text-sm"
                        >
                          {card.status === 'active' ? (
                            <>
                              <Pause className="w-4 h-4" />
                              Bloquer
                            </>
                          ) : (
                            <>
                              <Play className="w-4 h-4" />
                              Activer
                            </>
                          )}
                        </button>
                        <button
                          onClick={() => deleteCard(card.id)}
                          className="border border-gray-700 px-4 py-2 rounded-lg hover:border-red-500/50 hover:text-red-500 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Use Cases */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">OÙ UTILISER VOTRE CARTE</h2>

            <div className="grid md:grid-cols-3 gap-6">
              {useCases.map((useCase, idx) => (
                <div key={idx} className="border border-gray-800 rounded-xl p-8 hover:border-primary/50 transition-colors">
                  <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-6">
                    <useCase.icon className="w-7 h-7 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold mb-3">{useCase.title}</h3>
                  <p className="text-gray-400 mb-4">{useCase.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {useCase.examples.map((example, i) => (
                      <span key={i} className="px-3 py-1 bg-gray-900 rounded-full text-xs">
                        {example}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">COMMENT ÇA MARCHE</h2>

            <div className="space-y-6">
              <div className="flex gap-6 items-start">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">Créez votre carte</h3>
                  <p className="text-gray-400">
                    Cliquez sur "Créer ma carte virtuelle", choisissez un nom et validez. Votre carte est prête instantanément.
                  </p>
                </div>
              </div>

              <div className="flex gap-6 items-start">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">Rechargez depuis votre compte uFaranga</h3>
                  <p className="text-gray-400">
                    Transférez de l'argent de votre compte uFaranga vers votre carte virtuelle. Le montant est disponible immédiatement.
                  </p>
                </div>
              </div>

              <div className="flex gap-6 items-start">
                <div className="w-12 h-12 rounded-full bg-secondary/20 flex items-center justify-center shrink-0">
                  <span className="text-2xl font-bold text-secondary">3</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">Utilisez-la en ligne</h3>
                  <p className="text-gray-400">
                    Entrez le numéro de carte, la date d'expiration et le CVV sur n'importe quel site e-commerce. C'est tout !
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Security */}
      <section className="py-20 bg-gradient-to-b from-primary/5 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">SÉCURITÉ MAXIMALE</h2>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="border border-gray-800 rounded-xl p-6 text-center">
                <Shield className="w-12 h-12 text-primary mx-auto mb-4" />
                <h3 className="font-bold mb-2">3D Secure</h3>
                <p className="text-sm text-gray-400">Validation par SMS pour chaque paiement</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 text-center">
                <Lock className="w-12 h-12 text-primary mx-auto mb-4" />
                <h3 className="font-bold mb-2">Chiffrement</h3>
                <p className="text-sm text-gray-400">Données protégées par SSL/TLS</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 text-center">
                <Pause className="w-12 h-12 text-primary mx-auto mb-4" />
                <h3 className="font-bold mb-2">Blocage instantané</h3>
                <p className="text-sm text-gray-400">Bloquez votre carte en 1 clic</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 text-center">
                <DollarSign className="w-12 h-12 text-primary mx-auto mb-4" />
                <h3 className="font-bold mb-2">Limites contrôlées</h3>
                <p className="text-sm text-gray-400">Définissez vos propres limites</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <CreditCard className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-4xl font-anton uppercase mb-4">CRÉEZ VOTRE CARTE MAINTENANT</h2>
            <p className="text-xl text-gray-300 mb-8">
              Gratuit, instantané, et lié à votre compte uFaranga
            </p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Créer ma carte virtuelle
            </button>
          </div>
        </div>
      </section>
