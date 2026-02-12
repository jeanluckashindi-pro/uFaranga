import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Facebook, Twitter, Instagram, Linkedin, Youtube, 
  Mail, Phone, MapPin, Send, ArrowRight 
} from 'lucide-react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerSections = [
    {
      title: 'Produits',
      links: [
        { name: 'Compte Mobile', href: '/compte' },
        { name: 'Cartes', href: '/carte-virtuelle' },
        { name: 'Transferts', href: '/transferts' },
        { name: 'Épargne', href: '/epargne' },
        { name: 'Crédit', href: '/credit' },
      ]
    },
    {
      title: 'Entreprise',
      links: [
        { name: 'Solutions Business', href: '/entreprises' },
        { name: 'API Développeurs', href: '/developpeurs' },
        { name: 'Devenir Agent', href: '/agents' },
        { name: 'Partenaires', href: '/partenaires' },
        { name: 'Tarifs', href: '/tarifs' },
      ]
    },
    {
      title: 'Ressources',
      links: [
        { name: 'Centre d\'aide', href: '/support' },
        { name: 'Blog', href: '/blog' },
        { name: 'Documentation', href: '/docs' },
        { name: 'Tutoriels', href: '/tutoriels' },
        { name: 'Statut', href: '/support#status' },
      ]
    },
    {
      title: 'Société',
      links: [
        { name: 'À propos', href: '/a-propos' },
        { name: 'Carrières', href: '/carrieres' },
        { name: 'Presse', href: '/presse' },
        { name: 'Impact Social', href: '/impact' },
        { name: 'Contact', href: '/contact' },
      ]
    }
  ];

  const socialLinks = [
    { name: 'Facebook', icon: Facebook, href: 'https://facebook.com/ufaranga', color: 'hover:text-blue-500' },
    { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/ufaranga', color: 'hover:text-sky-400' },
    { name: 'Instagram', icon: Instagram, href: 'https://instagram.com/ufaranga', color: 'hover:text-pink-500' },
    { name: 'LinkedIn', icon: Linkedin, href: 'https://linkedin.com/company/ufaranga', color: 'hover:text-blue-600' },
    { name: 'YouTube', icon: Youtube, href: 'https://youtube.com/@ufaranga', color: 'hover:text-red-500' },
  ];

  return (
    <footer className="bg-black border-t border-white/10">
      <div className="container mx-auto px-4 py-16">
        {/* Top Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 mb-12">
          {/* Brand Column */}
          <div className="lg:col-span-4">
            <Link to="/" className="inline-block mb-6">
              <span className="text-4xl font-anton text-white tracking-tight kaushan-">uFaranga</span>
            </Link>
            
            <p className="text-gray-400 mb-6 leading-relaxed">
              La solution de paiement mobile qui transforme la vie financière de millions d'Africains. Simple, rapide et sécurisé.
            </p>


            {/* Social Links */}
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.name}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`w-10 h-10 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 ${social.color} transition-all hover:border-white/20`}
                  aria-label={social.name}
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Links Columns */}
          <div className="lg:col-span-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {footerSections.map((section) => (
                <div key={section.title}>
                  <h3 className="text-white font-bold mb-4 text-sm uppercase tracking-wider">
                    {section.title}
                  </h3>
                  <ul className="space-y-3">
                    {section.links.map((link) => (
                      <li key={link.name}>
                        <Link
                          to={link.href}
                          className="text-gray-400 hover:text-white transition-colors text-sm flex items-center gap-2 group"
                        >
                          <ArrowRight className="w-3 h-3 opacity-0 group-hover:opacity-100 -ml-5 group-hover:ml-0 transition-all" />
                          {link.name}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
