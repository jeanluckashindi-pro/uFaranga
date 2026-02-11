import { useState } from 'react';
import {
  BookOpen, Code, Smartphone, Globe, Server, Shield,
  Clock, CheckCircle, ArrowRight, Search, Filter, Star
} from 'lucide-react';

const Tutoriels = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { id: 'all', label: 'Tous', icon: BookOpen },
    { id: 'getting-started', label: 'Démarrage', icon: Star },
    { id: 'integration', label: 'Intégration', icon: Code },
    { id: 'mobile', label: 'Mobile', icon: Smartphone },
    { id: 'web', label: 'Web', icon: Globe },
    { id: 'backend', label: 'Backend', icon: Server },
    { id: 'security', label: 'Sécurité', icon: Shield }
  ];

  const tutorials = [
    {
      id: 1,
      title: 'Créer votre premier paiement',
      description: 'Guide complet pour intégrer votre premier paiement avec l\'API uFaranga en moins de 10 minutes',
      category: 'getting-started',
      duration: '10 min',
      level: 'Débutant',
      steps: 5,
      language: 'JavaScript',
      popular: true
    },
    {
      id: 2,
      title: 'Configurer les webhooks',
      description: 'Recevez des notifications en temps réel pour tous vos paiements et transactions',
      category: 'integration',
      duration: '15 min',
      level: 'Intermédiaire',
      steps: 7,
      language: 'Node.js',
      popular: true
    },
    {
      id: 3,
      title: 'Intégration React Native',
      description: 'Intégrez uFaranga dans votre application mobile React Native',
      category: 'mobile',
      duration: '25 min',
      level: 'Intermédiaire',
      steps: 10,
      language: 'React Native',
      popular: false
    },
    {
      id: 4,
      title: 'Sécuriser vos transactions',
      description: 'Meilleures pratiques de sécurité pour protéger vos paiements',
      category: 'security',
      duration: '20 min',
      level: 'Avancé',
      steps: 8,
      language: 'Tous',
      popular: true
    },
    {
      id: 5,
      title: 'API REST avec Express.js',
      description: 'Créez une API backend complète pour gérer les paiements uFaranga',
      category: 'backend',
      duration: '30 min',
      level: 'Intermédiaire',
      steps: 12,
      language: 'Node.js',
      popular: false
    },
    {
      id: 6,
      title: 'Intégration Flutter',
      description: 'Ajoutez les paiements uFaranga à votre app Flutter',
      category: 'mobile',
      duration: '20 min',
      level: 'Intermédiaire',
      steps: 9,
      language: 'Flutter',
      popular: false
    },
    {
      id: 7,
      title: 'Checkout page avec React',
      description: 'Créez une page de paiement moderne et responsive avec React',
      category: 'web',
      duration: '35 min',
      level: 'Intermédiaire',
      steps: 11,
      language: 'React',
      popular: true
    },
    {
      id: 8,
      title: 'Tests automatisés avec Jest',
      description: 'Testez votre intégration uFaranga avec des tests unitaires et d\'intégration',
      category: 'backend',
      duration: '25 min',
      level: 'Avancé',
      steps: 10,
      language: 'JavaScript',
      popular: false
    },
    {
      id: 9,
      title: 'Gestion des erreurs',
      description: 'Gérez correctement les erreurs et les cas limites dans vos intégrations',
      category: 'integration',
      duration: '15 min',
      level: 'Intermédiaire',
      steps: 6,
      language: 'Tous',
      popular: false
    },
    {
      id: 10,
      title: 'Paiements récurrents',
      description: 'Mettez en place des abonnements et paiements récurrents',
      category: 'integration',
      duration: '30 min',
      level: 'Avancé',
      steps: 13,
      language: 'Python',
      popular: true
    },
    {
      id: 11,
      title: 'Dashboard admin avec Vue.js',
      description: 'Créez un tableau de bord pour suivre vos transactions',
      category: 'web',
      duration: '40 min',
      level: 'Avancé',
      steps: 15,
      language: 'Vue.js',
      popular: false
    },
    {
      id: 12,
      title: 'Authentification 2FA',
      description: 'Ajoutez une couche de sécurité supplémentaire avec la 2FA',
      category: 'security',
      duration: '20 min',
      level: 'Avancé',
      steps: 8,
      language: 'Tous',
      popular: false
    }
  ];

  const filteredTutorials = tutorials.filter(tutorial => {
    const matchesCategory = selectedCategory === 'all' || tutorial.category === selectedCategory;
    const matchesSearch = tutorial.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tutorial.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const popularTutorials = tutorials.filter(t => t.popular);

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-secondary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-secondary/20 text-secondary px-4 py-2 rounded-full mb-6">
              <BookOpen className="w-5 h-5" />
              <span className="font-semibold">Tutoriels & Guides</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              TUTORIELS UFARANGA
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Guides pas à pas pour intégrer uFaranga dans vos applications
            </p>
            
            {/* Search */}
            <div className="max-w-2xl mx-auto relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                placeholder="Rechercher un tutoriel..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-black border border-gray-700 rounded-lg pl-12 pr-4 py-4 focus:border-secondary focus:outline-none"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Popular Tutorials */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">TUTORIELS POPULAIRES</h2>
            <p className="text-gray-400 mb-12">Les guides les plus consultés par la communauté</p>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {popularTutorials.map(tutorial => (
                <div key={tutorial.id} className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors">
                  <div className="flex items-center gap-2 mb-4">
                    <span className="px-3 py-1 bg-secondary/20 text-secondary text-xs font-semibold rounded-full">
                      {tutorial.level}
                    </span>
                    <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-semibold rounded-full">
                      {tutorial.language}
                    </span>
                  </div>

                  <h3 className="text-xl font-bold mb-2">{tutorial.title}</h3>
                  <p className="text-sm text-gray-400 mb-4">{tutorial.description}</p>

                  <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {tutorial.duration}
                    </div>
                    <div className="flex items-center gap-1">
                      <CheckCircle className="w-4 h-4" />
                      {tutorial.steps} étapes
                    </div>
                  </div>

                  <button className="w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2">
                    Commencer
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-12">PARCOURIR PAR CATÉGORIE</h2>

            <div className="flex gap-3 mb-8 overflow-x-auto pb-4">
              {categories.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-6 py-3 rounded-lg font-semibold whitespace-nowrap transition-colors inline-flex items-center gap-2 ${
                    selectedCategory === cat.id
                      ? 'bg-primary text-black'
                      : 'border border-gray-700 hover:border-primary/50'
                  }`}
                >
                  <cat.icon className="w-4 h-4" />
                  {cat.label}
                </button>
              ))}
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {filteredTutorials.map(tutorial => (
                <div key={tutorial.id} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-semibold rounded-full">
                        {tutorial.level}
                      </span>
                      <span className="text-xs text-gray-500">{tutorial.language}</span>
                    </div>
                    {tutorial.popular && (
                      <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                    )}
                  </div>

                  <h3 className="text-xl font-bold mb-2">{tutorial.title}</h3>
                  <p className="text-sm text-gray-400 mb-4">{tutorial.description}</p>

                  <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {tutorial.duration}
                    </div>
                    <div className="flex items-center gap-1">
                      <CheckCircle className="w-4 h-4" />
                      {tutorial.steps} étapes
                    </div>
                  </div>

                  <button className="w-full border border-gray-700 py-3 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center justify-center gap-2">
                    Voir le tutoriel
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>

            {filteredTutorials.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                <p className="text-gray-400">Aucun tutoriel trouvé</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-secondary/30 rounded-xl p-12 text-center bg-gradient-to-r from-secondary/10 to-primary/10">
            <h2 className="text-4xl font-anton uppercase mb-4">BESOIN D'AIDE ?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Notre équipe support est là pour vous accompagner
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/support"
                className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
              >
                Contacter le support
              </a>
              <a
                href="/developpeurs"
                className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-secondary/50 transition-colors"
              >
                Documentation API
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Tutoriels;
