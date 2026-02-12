import React, { useState } from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  LayoutDashboard, Users, Wallet, Settings, LogOut, Menu, X,
  Bell, Search, User, ChevronDown, TrendingUp, Receipt,
  CreditCard, FileText, BarChart3, Shield, Headphones
} from 'lucide-react';

const AdminLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [profileOpen, setProfileOpen] = useState(false);
  const location = useLocation();

  const menuItems = [
    { path: '/admin', icon: LayoutDashboard, label: 'Tableau de bord', exact: true },
    { path: '/admin/transactions', icon: Receipt, label: 'Transactions' },
    { path: '/admin/utilisateurs', icon: Users, label: 'Utilisateurs' },
    { path: '/admin/comptes', icon: Wallet, label: 'Comptes' },
    { path: '/admin/cartes', icon: CreditCard, label: 'Cartes' },
    { path: '/admin/rapports', icon: BarChart3, label: 'Rapports' },
    { path: '/admin/factures', icon: FileText, label: 'Factures' },
    { path: '/admin/securite', icon: Shield, label: 'Sécurité' },
    { path: '/admin/support', icon: Headphones, label: 'Support' },
    { path: '/admin/parametres', icon: Settings, label: 'Paramètres' },
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <aside className={`fixed top-0 left-0 h-full bg-gray-900 border-r border-gray-800 transition-all duration-300 z-50 ${
        sidebarOpen ? 'w-64' : 'w-20'
      }`}>
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-800">
          {sidebarOpen ? (
            <>
              <Link to="/" className="text-xl font-anton text-primary">uFaranga Admin</Link>
              <button onClick={() => setSidebarOpen(false)} className="p-2 hover:bg-gray-800 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </>
          ) : (
            <button onClick={() => setSidebarOpen(true)} className="p-2 hover:bg-gray-800 rounded-lg mx-auto">
              <Menu className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Menu Items */}
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive(item.path, item.exact)
                  ? 'bg-primary text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {sidebarOpen && <span>{item.label}</span>}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
        {/* Top Bar */}
        <header className="h-16 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-6 sticky top-0 z-40">
          <div className="flex items-center gap-4 flex-1">
            <div className="relative max-w-md w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
              <input
                type="text"
                placeholder="Rechercher..."
                className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-primary"
              />
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Notifications */}
            <button className="relative p-2 hover:bg-gray-800 rounded-lg">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-3 p-2 hover:bg-gray-800 rounded-lg"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-blue-600 flex items-center justify-center">
                  <User className="w-5 h-5" />
                </div>
                <div className="text-left hidden md:block">
                  <div className="text-sm font-semibold">Admin User</div>
                  <div className="text-xs text-gray-400">admin@ufaranga.com</div>
                </div>
                <ChevronDown className="w-4 h-4 text-gray-400" />
              </button>

              {profileOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl py-2">
                  <Link to="/admin/profil" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-700">
                    <User className="w-4 h-4" />
                    Mon profil
                  </Link>
                  <Link to="/admin/parametres" className="flex items-center gap-2 px-4 py-2 hover:bg-gray-700">
                    <Settings className="w-4 h-4" />
                    Paramètres
                  </Link>
                  <hr className="my-2 border-gray-700" />
                  <button className="flex items-center gap-2 px-4 py-2 hover:bg-gray-700 w-full text-left text-red-400">
                    <LogOut className="w-4 h-4" />
                    Déconnexion
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
