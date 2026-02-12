import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  ChevronDown,
  User,
  Building2,
  Users,
  CreditCard,
  PiggyBank,
  Send,
  Store,
  Code,
  GraduationCap,
  BookOpen,
  HelpCircle,
  FileText,
  Briefcase,
  Shield,
  Newspaper,
  Handshake,
  Smartphone,
  Wallet,
  TrendingUp,
  DollarSign,
  Globe,
  Zap,
  Lock,
  Receipt,
  QrCode,
  Repeat,
  ArrowLeftRight,
  Banknote,
  Calculator,
  BarChart3,
  Truck,
  Heart,
  ShoppingBag,
  Home,
  Landmark,
  Phone,
  Wifi,
  Lightbulb,
  Package
} from 'lucide-react';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [activeDropdown, setActiveDropdown] = useState(null);
  const location = useLocation();

  const megaMenuItems = {
    produits: {
      title: 'Produits',
      sections: [
        {
          title: 'Compte & Carte',
          items: [
            { name: 'Compte personnel', href: '/compte', description: 'Compte mobile gratuit', icon: User },
            { name: 'Carte virtuelle', href: '/carte-virtuelle', description: 'Visa/Mastercard virtuelle', icon: CreditCard },
            { name: 'Carte physique', href: '/carte-physique', description: 'Carte bancaire internationale', icon: CreditCard },
            { name: 'Multi-devises', href: '/multi-devises', description: 'Gérez plusieurs devises', icon: Globe }
          ]
        },
        {
          title: 'Transferts & Paiements',
          items: [
            { name: 'Transferts P2P', href: '/transferts', description: 'Envois gratuits instantanés', icon: Send },
            { name: 'Paiements QR', href: '/paiements-qr', description: 'Payez par QR code', icon: QrCode },
            { name: 'Paiements marchands', href: '/paiements-marchands', description: '10,000+ commerçants', icon: Store },
            { name: 'Factures', href: '/factures', description: 'Payez vos factures', icon: Receipt }
          ]
        },
        {
          title: 'Épargne & Crédit',
          items: [
            { name: 'Épargne automatique', href: '/epargne', description: 'Objectifs d\'épargne', icon: PiggyBank },
            { name: 'Tontines digitales', href: '/tontines', description: 'Épargne en groupe', icon: Users },
            { name: 'Micro-crédit', href: '/credit', description: 'Jusqu\'à 500,000 BIF', icon: DollarSign },
            { name: 'Investissements', href: '/investissements', description: 'Faites fructifier', icon: TrendingUp }
          ]
        },
        {
          title: 'Services',
          items: [
            { name: 'Recharge mobile', href: '/recharge', description: 'Airtime & data', icon: Smartphone },
            { name: 'Paiement factures', href: '/factures', description: 'Eau, électricité, TV', icon: Lightbulb },
            { name: 'Assurance', href: '/assurance', description: 'Protégez-vous', icon: Shield },
            { name: 'Cashback', href: '/cashback', description: 'Gagnez à chaque achat', icon: Repeat }
          ]
        }
      ]
    },
    business: {
      title: 'Business',
      sections: [
        {
          title: 'Solutions Entreprise',
          items: [
            { name: 'uFaranga Business', href: '/entreprises', description: 'Compte professionnel', icon: Building2 },
            { name: 'Point de vente', href: '/pos', description: 'Terminal de paiement', icon: Store },
            { name: 'E-commerce', href: '/ecommerce', description: 'Boutique en ligne', icon: ShoppingBag },
            { name: 'Facturation', href: '/facturation', description: 'Factures automatiques', icon: Receipt }
          ]
        },
        {
          title: 'Gestion',
          items: [
            { name: 'Trésorerie', href: '/tresorerie', description: 'Gérez vos flux', icon: BarChart3 },
            { name: 'Comptabilité', href: '/comptabilite', description: 'Suivi comptable', icon: Calculator },
            { name: 'Paie employés', href: '/paie', description: 'Salaires automatiques', icon: Wallet },
            { name: 'Multi-utilisateurs', href: '/multi-users', description: 'Équipe collaborative', icon: Users }
          ]
        },
        {
          title: 'Intégrations',
          items: [
            { name: 'API Paiements', href: '/api', description: 'Intégrez les paiements', icon: Code },
            { name: 'Plugins', href: '/plugins', description: 'WooCommerce, Shopify', icon: Package },
            { name: 'Webhooks', href: '/webhooks', description: 'Notifications temps réel', icon: Zap },
            { name: 'Documentation', href: '/docs', description: 'Guides développeurs', icon: BookOpen }
          ]
        }
      ]
    },
    solutions: {
      title: 'Solutions',
      sections: [
        {
          title: 'Par secteur',
          items: [
            { name: 'Commerce', href: '/solutions/commerce', description: 'Boutiques & magasins', icon: Store },
            { name: 'Éducation', href: '/solutions/education', description: 'Écoles & universités', icon: GraduationCap },
            { name: 'Santé', href: '/solutions/sante', description: 'Hôpitaux & cliniques', icon: Heart },
            { name: 'Transport', href: '/solutions/transport', description: 'Taxis & bus', icon: Truck },
            { name: 'Immobilier', href: '/solutions/immobilier', description: 'Loyers & ventes', icon: Home },
            { name: 'Hôtellerie', href: '/solutions/hotellerie', description: 'Hôtels & restaurants', icon: Building2 }
          ]
        },
        {
          title: 'Par besoin',
          items: [
            { name: 'Paiements en ligne', href: '/solutions/paiements', description: 'E-commerce', icon: Globe },
            { name: 'Paiements récurrents', href: '/solutions/recurrents', description: 'Abonnements', icon: Repeat },
            { name: 'Envois internationaux', href: '/solutions/international', description: 'Cross-border', icon: ArrowLeftRight },
            { name: 'Paiements de masse', href: '/solutions/masse', description: 'Bulk payments', icon: Users }
          ]
        }
      ]
    },
    agents: {
      title: 'Agents',
      sections: [
        {
          title: 'Devenir Agent',
          items: [
            { name: 'Programme Agent', href: '/agents', description: 'Rejoignez le réseau', icon: Users },
            { name: 'Commissions', href: '/agents/commissions', description: 'Gagnez sur chaque transaction', icon: DollarSign },
            { name: 'Formation', href: '/agents/formation', description: 'Formation gratuite', icon: GraduationCap },
            { name: 'Outils Agent', href: '/agents/outils', description: 'App & dashboard', icon: Smartphone }
          ]
        },
        {
          title: 'Services Agent',
          items: [
            { name: 'Dépôts & Retraits', href: '/agents/depot-retrait', description: 'Cash in/out', icon: Banknote },
            { name: 'Recharge mobile', href: '/agents/recharge', description: 'Airtime & data', icon: Phone },
            { name: 'Paiement factures', href: '/agents/factures', description: 'Services publics', icon: Receipt },
            { name: 'Transferts', href: '/agents/transferts', description: 'Envois d\'argent', icon: Send }
          ]
        },
        {
          title: 'Support Agent',
          items: [
            { name: 'Trouver un agent', href: '/trouver-agent', description: 'Localisez un agent', icon: Landmark },
            { name: 'Assistance', href: '/agents/support', description: 'Support dédié', icon: HelpCircle },
            { name: 'Communauté', href: '/agents/communaute', description: 'Réseau d\'agents', icon: Users }
          ]
        }
      ]
    },
    ressources: {
      title: 'Ressources',
      sections: [
        {
          title: 'Apprendre',
          items: [
            { name: 'Blog', href: '/blog', description: 'Actualités & conseils', icon: BookOpen },
            { name: 'Centre d\'aide', href: '/support', description: 'FAQ & guides', icon: HelpCircle },
            { name: 'Tutoriels', href: '/tutoriels', description: 'Vidéos & guides', icon: FileText },
            { name: 'Webinaires', href: '/webinaires', description: 'Formations en ligne', icon: GraduationCap }
          ]
        },
        {
          title: 'Développeurs',
          items: [
            { name: 'Documentation API', href: '/developpeurs', description: 'Référence complète', icon: Code },
            { name: 'Sandbox', href: '/sandbox', description: 'Environnement de test', icon: Code },
            { name: 'SDKs', href: '/sdks', description: 'Bibliothèques', icon: Package },
            { name: 'Changelog', href: '/changelog', description: 'Nouveautés API', icon: FileText }
          ]
        },
        {
          title: 'Légal & Sécurité',
          items: [
            { name: 'Sécurité', href: '/securite', description: 'Notre engagement', icon: Shield },
            { name: 'Confidentialité', href: '/legal#privacy', description: 'Politique de confidentialité', icon: Lock },
            { name: 'Conditions', href: '/legal#terms', description: 'CGU', icon: FileText },
            { name: 'Conformité', href: '/conformite', description: 'Régulations', icon: Landmark }
          ]
        }
      ]
    },
    entreprise: {
      title: 'Entreprise',
      sections: [
        {
          title: 'À propos',
          items: [
            { name: 'Notre mission', href: '/a-propos', description: 'Qui nous sommes', icon: Briefcase },
            { name: 'Équipe', href: '/equipe', description: 'Rencontrez l\'équipe', icon: Users },
            { name: 'Carrières', href: '/carrieres', description: 'Rejoignez-nous', icon: Briefcase },
            { name: 'Impact social', href: '/impact', description: 'Notre contribution', icon: Heart }
          ]
        },
        {
          title: 'Partenaires',
          items: [
            { name: 'Devenir partenaire', href: '/partenaires', description: 'Collaborons', icon: Handshake },
            { name: 'Nos partenaires', href: '/partenaires/liste', description: 'Réseau de partenaires', icon: Building2 },
            { name: 'Programme affiliation', href: '/affiliation', description: 'Gagnez des commissions', icon: DollarSign }
          ]
        },
        {
          title: 'Communication',
          items: [
            { name: 'Presse', href: '/presse', description: 'Kit média', icon: Newspaper },
            { name: 'Actualités', href: '/actualites', description: 'Communiqués', icon: Newspaper },
            { name: 'Contact', href: '/contact', description: 'Contactez-nous', icon: Phone }
          ]
        }
      ]
    }
  };

  const simpleLinks = [
    { name: 'Tarifs', href: '/tarifs' },
    { name: 'Télécharger', href: '/telecharger' }
  ];

  const isActive = (path) => location.pathname === path;

  const handleMouseEnter = (dropdown) => {
    setActiveDropdown(dropdown);
  };

  const handleMouseLeave = () => {
    setActiveDropdown(null);
  };

  return (
    <header className="sticky top-0 z-50 glass">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Brand */}
          <Link to="/" className="flex items-center">
            <span className="text-3xl font-kaushan text-white">
              uFaranga
            </span>
          </Link>

          {/* Navigation Desktop - Mega Menu */}
          <div className="hidden lg:flex items-center space-x-8">
            {/* Mega Menu Items */}
            {Object.entries(megaMenuItems).map(([key, menu]) => (
              <div
                key={key}
                className="relative group"
                onMouseEnter={() => handleMouseEnter(key)}
                onMouseLeave={handleMouseLeave}
              >
                <button className="flex items-center gap-1.5 px-1 py-2 text-sm font-medium text-white hover:text-primary transition-colors">
                  {menu.title}
                  <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${activeDropdown === key ? 'rotate-180' : ''}`} />
                </button>

                {/* Dropdown with animation */}
                <div className={`absolute left-1/2 -translate-x-1/2 top-full pt-4 transition-all duration-300 ${activeDropdown === key
                    ? 'opacity-100 visible translate-y-0'
                    : 'opacity-0 invisible -translate-y-2 pointer-events-none'
                  }`}>
                  <div className={`bg-black rounded-2xl shadow-2xl border border-gray-800 p-6 ${menu.sections.length === 4 ? 'w-[960px]' :
                      menu.sections.length === 3 ? 'w-[720px]' :
                        'w-[520px]'
                    }`}>
                    <div className={`grid gap-6 ${menu.sections.length === 4 ? 'grid-cols-4' :
                        menu.sections.length === 3 ? 'grid-cols-3' :
                          'grid-cols-2'
                      }`}>
                      {menu.sections.map((section, idx) => (
                        <div key={idx}>
                          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4 px-3">
                            {section.title}
                          </h3>
                          <ul className="space-y-1">
                            {section.items.map((item, itemIdx) => {
                              const Icon = item.icon;
                              return (
                                <li key={itemIdx}>
                                  <Link
                                    to={item.href}
                                    className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-900 transition-colors group/item"
                                    onClick={() => setActiveDropdown(null)}
                                  >
                                    <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover/item:bg-primary transition-colors">
                                      <Icon className="w-5 h-5 text-primary group-hover/item:text-white" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                      <div className="text-sm font-semibold text-white group-hover/item:text-primary transition-colors">
                                        {item.name}
                                      </div>
                                      <div className="text-xs text-gray-400 mt-0.5 line-clamp-1">
                                        {item.description}
                                      </div>
                                    </div>
                                  </Link>
                                </li>
                              );
                            })}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Simple Links */}
            {simpleLinks.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`px-1 py-2 text-sm font-medium transition-colors ${isActive(item.href)
                    ? 'text-primary'
                    : 'text-white hover:text-primary'
                  }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <div className="flex lg:hidden items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-white hover:bg-gray-900 transition-colors"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {mobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-800 max-h-[calc(100vh-5rem)] overflow-y-auto">
            <div className="flex flex-col space-y-4">
              {/* Mobile Mega Menu */}
              {Object.entries(megaMenuItems).map(([key, menu]) => (
                <div key={key}>
                  <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    {menu.title}
                  </div>
                  {menu.sections.map((section, idx) => (
                    <div key={idx} className="ml-2 mt-2">
                      <div className="text-xs font-medium text-gray-500 mb-2 px-3">
                        {section.title}
                      </div>
                      {section.items.map((item, itemIdx) => {
                        const Icon = item.icon;
                        return (
                          <Link
                            key={itemIdx}
                            to={item.href}
                            onClick={() => setMobileMenuOpen(false)}
                            className="flex items-center gap-3 px-3 py-2 text-sm text-white hover:bg-gray-900 rounded-lg transition-colors"
                          >
                            <Icon className="w-4 h-4 text-primary" />
                            {item.name}
                          </Link>
                        );
                      })}
                    </div>
                  ))}
                </div>
              ))}

              {/* Simple Links Mobile */}
              {simpleLinks.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="px-3 py-2 text-base font-medium text-white hover:bg-gray-900 rounded-lg transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        )}
      </nav>
    </header>
  );
};

export default Header;
