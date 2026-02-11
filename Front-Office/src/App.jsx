import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Layout from './components/layout/Layout';

// Pages principales
import Home from './pages/Home';
import Features from './pages/Features';
import Pricing from './pages/Pricing';
import Business from './pages/Business';
import Agents from './pages/Agents';
import About from './pages/About';
import Blog from './pages/Blog';
import BlogPost from './pages/BlogPost';
import Support from './pages/Support';
import Developers from './pages/Developers';
import Careers from './pages/Careers';
import Security from './pages/Security';
import Legal from './pages/Legal';
import Press from './pages/Press';
import Partners from './pages/Partners';
import PartnersList from './pages/PartnersList';
import SDKs from './pages/SDKs';
import Impact from './pages/Impact';
import Affiliation from './pages/Affiliation';
import Contact from './pages/Contact';
import Actualites from './pages/Actualites';
import Team from './pages/Team';
import Sandbox from './pages/Sandbox';
import DeveloperSignup from './pages/DeveloperSignup';
import DeveloperDashboard from './pages/DeveloperDashboard';
import Webinaires from './pages/Webinaires';
import Tutoriels from './pages/Tutoriels';
import Changelog from './pages/Changelog';
import Conformite from './pages/Conformite';
import NotFound from './pages/NotFound';

// Produits - Compte & Carte
import Account from './pages/Account';
import VirtualCard from './pages/VirtualCard';
import PhysicalCard from './pages/PhysicalCard';
import MultiCurrency from './pages/MultiCurrency';

// Produits - Transferts & Paiements
import Transfers from './pages/Transfers';
import QRPayments from './pages/QRPayments';
import MerchantPayments from './pages/MerchantPayments';
import Bills from './pages/Bills';

// Produits - Épargne & Crédit
import Savings from './pages/Savings';
import Tontines from './pages/Tontines';
import MicroCredit from './pages/MicroCredit';

// Business
import POS from './pages/POS';
import API from './pages/API';

// Autres
import Download from './pages/Download';

// Solutions
import Commerce from './pages/solutions/Commerce';
import Education from './pages/solutions/Education';
import Health from './pages/solutions/Health';
import Transport from './pages/solutions/Transport';
import RealEstate from './pages/solutions/RealEstate';
import Hospitality from './pages/solutions/Hospitality';
import OnlinePayments from './pages/solutions/OnlinePayments';
import RecurringPayments from './pages/solutions/RecurringPayments';
import International from './pages/solutions/International';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
          <Routes>
            {/* Pages principales */}
            <Route path="/" element={<Home />} />
            <Route path="/fonctionnalites" element={<Features />} />
            <Route path="/tarifs" element={<Pricing />} />
            <Route path="/telecharger" element={<Download />} />
            
            {/* Produits - Compte & Carte */}
            <Route path="/compte" element={<Account />} />
            <Route path="/carte-virtuelle" element={<VirtualCard />} />
            <Route path="/carte-physique" element={<PhysicalCard />} />
            <Route path="/multi-devises" element={<MultiCurrency />} />
            
            {/* Produits - Transferts & Paiements */}
            <Route path="/transferts" element={<Transfers />} />
            <Route path="/paiements-qr" element={<QRPayments />} />
            <Route path="/paiements-marchands" element={<MerchantPayments />} />
            <Route path="/factures" element={<Bills />} />
            
            {/* Produits - Épargne & Crédit */}
            <Route path="/epargne" element={<Savings />} />
            <Route path="/tontines" element={<Tontines />} />
            <Route path="/credit" element={<MicroCredit />} />
            
            {/* Business */}
            <Route path="/entreprises" element={<Business />} />
            <Route path="/pos" element={<POS />} />
            <Route path="/api" element={<API />} />
            
            {/* Agents */}
            <Route path="/agents" element={<Agents />} />
            
            {/* Solutions */}
            <Route path="/solutions/commerce" element={<Commerce />} />
            <Route path="/solutions/education" element={<Education />} />
            <Route path="/solutions/sante" element={<Health />} />
            <Route path="/solutions/transport" element={<Transport />} />
            <Route path="/solutions/immobilier" element={<RealEstate />} />
            <Route path="/solutions/hotellerie" element={<Hospitality />} />
            <Route path="/solutions/paiements" element={<OnlinePayments />} />
            <Route path="/solutions/recurrents" element={<RecurringPayments />} />
            <Route path="/solutions/international" element={<International />} />
            
            {/* Blog */}
            <Route path="/blog" element={<Blog />} />
            <Route path="/blog/:slug" element={<BlogPost />} />
            <Route path="/actualites" element={<Actualites />} />
            <Route path="/actualites/:slug" element={<BlogPost />} />
            
            {/* Support & Ressources */}
            <Route path="/support" element={<Support />} />
            <Route path="/developpeurs" element={<Developers />} />
            <Route path="/developpeurs/inscription" element={<DeveloperSignup />} />
            <Route path="/developpeurs/dashboard" element={<DeveloperDashboard />} />
            <Route path="/sandbox" element={<Sandbox />} />
            <Route path="/sdks" element={<SDKs />} />
            <Route path="/webinaires" element={<Webinaires />} />
            <Route path="/tutoriels" element={<Tutoriels />} />
            <Route path="/changelog" element={<Changelog />} />
            <Route path="/conformite" element={<Conformite />} />
            
            {/* Entreprise */}
            <Route path="/a-propos" element={<About />} />
            <Route path="/equipe" element={<Team />} />
            <Route path="/carrieres" element={<Careers />} />
            <Route path="/securite" element={<Security />} />
            <Route path="/legal" element={<Legal />} />
            <Route path="/presse" element={<Press />} />
            <Route path="/partenaires" element={<Partners />} />
            <Route path="/partenaires/liste" element={<PartnersList />} />
            <Route path="/impact" element={<Impact />} />
            <Route path="/affiliation" element={<Affiliation />} />
            <Route path="/contact" element={<Contact />} />
            
            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
