import { useState } from 'react';
import {
  Video, Calendar, Clock, Users, Play, CheckCircle,
  Download, ExternalLink, Filter, Search, Tag
} from 'lucide-react';

const Webinaires = () => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { id: 'all', label: 'Tous les webinaires' },
    { id: 'integration', label: 'Intégration API' },
    { id: 'security', label: 'Sécurité' },
    { id: 'business', label: 'Business' },
    { id: 'mobile', label: 'Mobile Money' }
  ];

  const upcomingWebinars = [
    {
      id: 1,
      title: 'Intégration API uFaranga en 30 minutes',
      description: 'Apprenez à intégrer l\'API uFaranga dans votre application web en moins de 30 minutes',
      date: '2026-02-20',
      time: '14:00 - 15:00',
      speaker: 'Jean-Claude Niyonzima',
      role: 'Lead Developer',
      category: 'integration',
      attendees: 45,
      maxAttendees: 100,
      level: 'Débutant',
      language: 'Français'
    },
    {
      id: 2,
      title: 'Sécuriser vos transactions avec uFaranga',
      description: 'Meilleures pratiques de sécurité pour protéger vos transactions et vos utilisateurs',
      date: '2026-02-25',
      time: '10:00 - 11:30',
      speaker: 'Marie Uwimana',
      role: 'Security Expert',
      category: 'security',
      attendees: 32,
      maxAttendees: 80,
      level: 'Intermédiaire',
      language: 'Français'
    },
    {
      id: 3,
      title: 'Développer une app Mobile Money complète',
      description: 'De zéro à la production : créez votre application de paiement mobile',
      date: '2026-03-05',
      time: '15:00 - 17:00',
      speaker: 'Patrick Ndayisenga',
      role: 'Mobile Architect',
      category: 'mobile',
      attendees: 28,
      maxAttendees: 60,
      level: 'Avancé',
      language: 'Français'
    }
  ];

  const pastWebinars = [
    {
      id: 4,
      title: 'Introduction à l\'API uFaranga',
      description: 'Découvrez les bases de l\'API et créez votre premier paiement',
      date: '2026-01-15',
      duration: '45 min',
      views: 1234,
      category: 'integration',
      videoUrl: '#',
      slidesUrl: '#',
      level: 'Débutant'
    },
    {
      id: 5,
      title: 'Webhooks et notifications en temps réel',
      description: 'Configurez et gérez les webhooks pour recevoir des notifications instantanées',
      date: '2026-01-22',
      duration: '60 min',
      views: 892,
      category: 'integration',
      videoUrl: '#',
      slidesUrl: '#',
      level: 'Intermédiaire'
    },
    {
      id: 6,
      title: 'Monétiser votre app avec uFaranga',
      description: 'Stratégies de monétisation et modèles économiques pour votre application',
      date: '2026-01-28',
      duration: '90 min',
      views: 756,
      category: 'business',
      videoUrl: '#',
      slidesUrl: '#',
      level: 'Tous niveaux'
    },
    {
      id: 7,
      title: 'Tests et débogage avec le Sandbox',
      description: 'Utilisez efficacement l\'environnement de test pour développer sans risque',
      date: '2026-02-05',
      duration: '50 min',
      views: 645,
      category: 'integration',
      videoUrl: '#',
      slidesUrl: '#',
      level: 'Débutant'
    }
  ];

  const filteredPastWebinars = pastWebinars.filter(webinar => {
    const matchesFilter = filter === 'all' || webinar.category === filter;
    const matchesSearch = webinar.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         webinar.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Video className="w-5 h-5" />
              <span className="font-semibold">Webinaires & Formations</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              WEBINAIRES UFARANGA
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Formations en direct et replays pour maîtriser l'API uFaranga et développer vos applications de paiement
            </p>
          </div>
        </div>
      </section>

      {/* Upcoming Webinars */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">WEBINAIRES À VENIR</h2>
            <p className="text-gray-400 mb-12">Inscrivez-vous gratuitement aux prochaines sessions</p>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {upcomingWebinars.map(webinar => (
                <div key={webinar.id} className="border border-gray-800 rounded-xl overflow-hidden hover:border-primary/50 transition-colors">
                  <div className="bg-gradient-to-br from-primary/20 to-secondary/20 p-6">
                    <div className="flex items-center gap-2 mb-4">
                      <span className="px-3 py-1 bg-primary/30 text-primary text-xs font-semibold rounded-full">
                        {webinar.level}
                      </span>
                      <span className="px-3 py-1 bg-black/30 text-white text-xs font-semibold rounded-full">
                        {webinar.language}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold mb-2">{webinar.title}</h3>
                    <p className="text-sm text-gray-300 mb-4">{webinar.description}</p>
                  </div>

                  <div className="p-6 space-y-3">
                    <div className="flex items-center gap-2 text-sm">
                      <Calendar className="w-4 h-4 text-primary" />
                      <span>{new Date(webinar.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Clock className="w-4 h-4 text-primary" />
                      <span>{webinar.time}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Users className="w-4 h-4 text-primary" />
                      <span>{webinar.attendees}/{webinar.maxAttendees} inscrits</span>
                    </div>

                    <div className="pt-4 border-t border-gray-800">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
                          <Users className="w-5 h-5 text-primary" />
                        </div>
                        <div>
                          <div className="font-semibold text-sm">{webinar.speaker}</div>
                          <div className="text-xs text-gray-400">{webinar.role}</div>
                        </div>
                      </div>

                      <button className="w-full bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
                        S'inscrire gratuitement
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Past Webinars */}
      <section className="py-20 bg-gradient-to-b from-black to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase mb-4">REPLAYS DISPONIBLES</h2>
            <p className="text-gray-400 mb-8">Regardez les enregistrements des webinaires passés</p>

            {/* Filters */}
            <div className="flex flex-col md:flex-row gap-4 mb-8">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type="text"
                  placeholder="Rechercher un webinaire..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                />
              </div>
              <div className="flex gap-2 overflow-x-auto">
                {categories.map(cat => (
                  <button
                    key={cat.id}
                    onClick={() => setFilter(cat.id)}
                    className={`px-4 py-3 rounded-lg font-semibold whitespace-nowrap transition-colors ${
                      filter === cat.id
                        ? 'bg-primary text-black'
                        : 'border border-gray-700 hover:border-primary/50'
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Webinar Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {filteredPastWebinars.map(webinar => (
                <div key={webinar.id} className="border border-gray-800 rounded-xl overflow-hidden hover:border-secondary/50 transition-colors">
                  <div className="relative bg-gradient-to-br from-gray-900 to-black p-8 flex items-center justify-center">
                    <div className="absolute inset-0 bg-secondary/10"></div>
                    <Play className="w-16 h-16 text-secondary relative z-10" />
                  </div>

                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="px-3 py-1 bg-secondary/20 text-secondary text-xs font-semibold rounded-full">
                        {webinar.level}
                      </span>
                      <span className="text-xs text-gray-500">{webinar.duration}</span>
                    </div>

                    <h3 className="text-xl font-bold mb-2">{webinar.title}</h3>
                    <p className="text-sm text-gray-400 mb-4">{webinar.description}</p>

                    <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {new Date(webinar.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="w-4 h-4" />
                        {webinar.views} vues
                      </div>
                    </div>

                    <div className="flex gap-3">
                      <a
                        href={webinar.videoUrl}
                        className="flex-1 bg-white text-black py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2"
                      >
                        <Play className="w-4 h-4" />
                        Regarder
                      </a>
                      <a
                        href={webinar.slidesUrl}
                        className="border border-gray-700 px-4 py-3 rounded-lg hover:border-secondary/50 transition-colors inline-flex items-center gap-2"
                      >
                        <Download className="w-4 h-4" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {filteredPastWebinars.length === 0 && (
              <div className="text-center py-12">
                <Video className="w-16 h-16 text-gray-700 mx-auto mb-4" />
                <p className="text-gray-400">Aucun webinaire trouvé</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <h2 className="text-4xl font-anton uppercase mb-4">PROPOSEZ UN SUJET</h2>
            <p className="text-xl text-gray-300 mb-8">
              Vous avez une idée de webinaire ? Partagez-la avec nous !
            </p>
            <a
              href="/contact"
              className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
            >
              <ExternalLink className="w-5 h-5" />
              Nous contacter
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Webinaires;
