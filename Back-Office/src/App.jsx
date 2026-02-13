import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import AllModulesLayout from './components/AllModulesLayout';

// Agent Pages
import AgentDashboard from './pages/agent/AgentDashboard';
import AgentTransactions from './pages/agent/Transactions';
import AgentFloat from './pages/agent/Float';
import AgentRapports from './pages/agent/Rapports';
import AgentCommissions from './pages/agent/Commissions';
import AgentNotifications from './pages/agent/Notifications';
import AgentParametres from './pages/agent/Parametres';

// Admin System Pages
import AdminDashboard from './pages/admin/DashboardPro';
import CartographieReseau from './pages/admin/CartographieReseau';
import GestionAgents from './pages/admin/GestionAgents';
import GestionClients from './pages/admin/GestionClients';
import ToutesTransactions from './pages/admin/ToutesTransactions';
import FloatGlobal from './pages/admin/FloatGlobal';
import Securite from './pages/admin/Securite';
import Fraude from './pages/admin/Fraude';
import Reporting from './pages/admin/Reporting';
import GestionCommissions from './pages/admin/GestionCommissions';

// Tech Pages
import CartographieAgents from './pages/tech/CartographieAgents';
import TechMonitoring from './pages/tech/Monitoring';
import TechPerformance from './pages/tech/Performance';
import TechAPI from './pages/tech/API';
import TechWebhooks from './pages/tech/Webhooks';
import TechSMS from './pages/tech/SMS';
import TechEmail from './pages/tech/Email';
import TechLogs from './pages/tech/Logs';
import TechMaintenance from './pages/tech/Maintenance';
import TechFirewall from './pages/tech/Firewall';

function App() {
  return (
    <ThemeProvider>
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AllModulesLayout userName="Super Admin">
          <Routes>
            {/* Agent Routes */}
            <Route path="/agent/dashboard" element={<AgentDashboard />} />
            <Route path="/agent/transactions" element={<AgentTransactions />} />
            <Route path="/agent/float" element={<AgentFloat />} />
            <Route path="/agent/rapports" element={<AgentRapports />} />
            <Route path="/agent/commissions" element={<AgentCommissions />} />
            <Route path="/agent/notifications" element={<AgentNotifications />} />
            <Route path="/agent/parametres" element={<AgentParametres />} />

            {/* Admin System Routes */}
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/cartographie" element={<CartographieReseau />} />
            <Route path="/admin/agents" element={<GestionAgents />} />
            <Route path="/admin/clients" element={<GestionClients />} />
            <Route path="/admin/transactions" element={<ToutesTransactions />} />
            <Route path="/admin/commissions" element={<GestionCommissions />} />
            <Route path="/admin/float-global" element={<FloatGlobal />} />
            <Route path="/admin/reporting" element={<Reporting />} />
            <Route path="/admin/fraude" element={<Fraude />} />
            <Route path="/admin/securite" element={<Securite />} />
            <Route path="/admin/parametres" element={<AdminDashboard />} />

            {/* Admin Tech Routes */}
            <Route path="/tech/monitoring" element={<TechMonitoring />} />
            <Route path="/tech/cartographie-agents" element={<CartographieAgents />} />
            <Route path="/tech/performance" element={<TechPerformance />} />
            <Route path="/tech/api" element={<TechAPI />} />
            <Route path="/tech/webhooks" element={<TechWebhooks />} />
            <Route path="/tech/sms" element={<TechSMS />} />
            <Route path="/tech/email" element={<TechEmail />} />
            <Route path="/tech/logs" element={<TechLogs />} />
            <Route path="/tech/maintenance" element={<TechMaintenance />} />
            <Route path="/tech/firewall" element={<TechFirewall />} />
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
