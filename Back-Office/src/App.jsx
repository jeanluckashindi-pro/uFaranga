import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import AllModulesLayout from './components/AllModulesLayout';

// Agent Pages
import AgentDashboard from './pages/agent/AgentDashboard';
import AgentTransactions from './pages/agent/Transactions';

// Admin System Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import CartographieReseau from './pages/admin/CartographieReseau';
import GestionAgents from './pages/admin/GestionAgents';
import GestionClients from './pages/admin/GestionClients';
import ToutesTransactions from './pages/admin/ToutesTransactions';

// Tech Pages
import CartographieAgents from './pages/tech/CartographieAgents';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AllModulesLayout userName="Super Admin">
          <Routes>
            {/* Agent Routes */}
            <Route path="/agent/dashboard" element={<AgentDashboard />} />
            <Route path="/agent/transactions" element={<AgentTransactions />} />
            <Route path="/agent/float" element={<AgentDashboard />} />
            <Route path="/agent/rapports" element={<AgentDashboard />} />
            <Route path="/agent/commissions" element={<AgentDashboard />} />
            <Route path="/agent/notifications" element={<AgentDashboard />} />
            <Route path="/agent/parametres" element={<AgentDashboard />} />

            {/* Admin System Routes */}
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/cartographie" element={<CartographieReseau />} />
            <Route path="/admin/agents" element={<GestionAgents />} />
            <Route path="/admin/clients" element={<GestionClients />} />
            <Route path="/admin/transactions" element={<ToutesTransactions />} />
            <Route path="/admin/commissions" element={<AdminDashboard />} />
            <Route path="/admin/float-global" element={<AdminDashboard />} />
            <Route path="/admin/reporting" element={<AdminDashboard />} />
            <Route path="/admin/fraude" element={<AdminDashboard />} />
            <Route path="/admin/securite" element={<AdminDashboard />} />
            <Route path="/admin/parametres" element={<AdminDashboard />} />

            {/* Client Routes */}
            <Route path="/client/dashboard" element={<AgentDashboard />} />
            <Route path="/client/transfert" element={<AgentDashboard />} />
            <Route path="/client/paiement" element={<AgentDashboard />} />
            <Route path="/client/depot" element={<AgentDashboard />} />
            <Route path="/client/retrait" element={<AgentDashboard />} />
            <Route path="/client/historique" element={<AgentDashboard />} />
            <Route path="/client/releves" element={<AgentDashboard />} />
            <Route path="/client/profil" element={<AgentDashboard />} />
            <Route path="/client/securite" element={<AgentDashboard />} />

            {/* Admin Tech Routes */}
            <Route path="/tech/monitoring" element={<AdminDashboard />} />
            <Route path="/tech/cartographie-agents" element={<CartographieAgents />} />
            <Route path="/tech/performance" element={<AdminDashboard />} />
            <Route path="/tech/api" element={<AdminDashboard />} />
            <Route path="/tech/webhooks" element={<AdminDashboard />} />
            <Route path="/tech/sms" element={<AdminDashboard />} />
            <Route path="/tech/email" element={<AdminDashboard />} />
            <Route path="/tech/logs" element={<AdminDashboard />} />
            <Route path="/tech/maintenance" element={<AdminDashboard />} />
            <Route path="/tech/firewall" element={<AdminDashboard />} />
            <Route path="/tech/detection" element={<AdminDashboard />} />
            <Route path="/tech/database" element={<AdminDashboard />} />

            {/* Default redirect */}
            <Route path="/" element={<Navigate to="/agent/dashboard" replace />} />
          </Routes>
        </AllModulesLayout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
