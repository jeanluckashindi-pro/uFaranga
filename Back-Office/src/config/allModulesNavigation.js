import {
  LayoutDashboard, Activity, Wallet, FileText, TrendingUp,
  Bell, Settings, Users, Shield, UserCheck, DollarSign,
  BarChart3, Lock, Database, Server, Zap, AlertTriangle,
  CreditCard, RefreshCw, Download, Upload, Eye, Ban,
  CheckCircle, XCircle, Clock, Globe, Smartphone, Mail,
  ArrowDownToLine, ArrowUpFromLine, ArrowLeftRight
} from 'lucide-react';

// Navigation complète avec TOUS les modules
export const allModulesNavigation = [
  // ==================== MODULE AGENT ====================
  {
    section: 'MODULE AGENT',
    module: 'agent',
    color: 'primary',
    items: [
      { 
        path: '/agent/dashboard', 
        icon: LayoutDashboard, 
        label: 'Dashboard Agent', 
        description: 'Vue d\'ensemble activité agent'
      },
      { 
        path: '/agent/transactions', 
        icon: Activity, 
        label: 'Transactions', 
        description: 'Dépôts, retraits, transferts'
      },
      { 
        path: '/agent/float', 
        icon: Wallet, 
        label: 'Gestion Float', 
        description: 'Réapprovisionnement float'
      },
      { 
        path: '/agent/rapports', 
        icon: FileText, 
        label: 'Rapports Agent', 
        description: 'Rapports journaliers/mensuels'
      },
      { 
        path: '/agent/commissions', 
        icon: TrendingUp, 
        label: 'Mes Commissions', 
        description: 'Suivi des gains'
      },
      { 
        path: '/agent/notifications', 
        icon: Bell, 
        label: 'Notifications Agent', 
        badge: 'notifications'
      },
      { 
        path: '/agent/parametres', 
        icon: Settings, 
        label: 'Paramètres Agent'
      },
    ]
  },

  // ==================== MODULE ADMIN SYSTÈME ====================
  {
    section: 'MODULE ADMIN SYSTÈME',
    module: 'admin',
    color: 'danger',
    items: [
      { 
        path: '/admin/dashboard', 
        icon: LayoutDashboard, 
        label: 'Dashboard Global',
        description: 'Vue complète plateforme'
      },
      { 
        path: '/admin/cartographie', 
        icon: Globe, 
        label: 'Cartographie Réseau',
        description: 'Carte réseau uFaranga global'
      },
      { 
        path: '/admin/agents', 
        icon: Users, 
        label: 'Gestion Agents',
        description: 'Ajouter, suspendre agents'
      },
      { 
        path: '/admin/clients', 
        icon: UserCheck, 
        label: 'Gestion Clients',
        description: 'KYC, plafonds, suspensions'
      },
      { 
        path: '/admin/transactions', 
        icon: Activity, 
        label: 'Toutes Transactions',
        description: 'Recherche, annulation, litiges'
      },
      { 
        path: '/admin/commissions', 
        icon: DollarSign, 
        label: 'Gestion Commissions',
        description: 'Grilles et rapports'
      },
      { 
        path: '/admin/float-global', 
        icon: Wallet, 
        label: 'Float Global Réseau',
        description: 'Float total et répartition'
      },
      { 
        path: '/admin/reporting', 
        icon: BarChart3, 
        label: 'Reporting Global',
        description: 'Rapports financiers'
      },
      { 
        path: '/admin/fraude', 
        icon: AlertTriangle, 
        label: 'Détection Fraude',
        description: 'Alertes et scoring'
      },
      { 
        path: '/admin/securite', 
        icon: Shield, 
        label: 'Sécurité & Conformité',
        description: 'Logs, audit, AML'
      },
      { 
        path: '/admin/parametres', 
        icon: Settings, 
        label: 'Paramètres Système',
        description: 'Limites, frais, config'
      },
    ]
  },

  // ==================== MODULE CLIENT ====================
  {
    section: 'MODULE CLIENT',
    module: 'client',
    color: 'secondary',
    items: [
      { 
        path: '/client/dashboard', 
        icon: LayoutDashboard, 
        label: 'Dashboard Client',
        description: 'Solde et activité'
      },
      { 
        path: '/client/transfert', 
        icon: ArrowLeftRight, 
        label: 'Transfert Argent',
        description: 'Envoyer de l\'argent'
      },
      { 
        path: '/client/paiement', 
        icon: CreditCard, 
        label: 'Paiements',
        description: 'Factures et services'
      },
      { 
        path: '/client/depot', 
        icon: ArrowDownToLine, 
        label: 'Dépôt',
        description: 'Déposer de l\'argent'
      },
      { 
        path: '/client/retrait', 
        icon: ArrowUpFromLine, 
        label: 'Retrait',
        description: 'Retirer de l\'argent'
      },
      { 
        path: '/client/historique', 
        icon: Clock, 
        label: 'Historique',
        description: 'Toutes transactions'
      },
      { 
        path: '/client/releves', 
        icon: Download, 
        label: 'Relevés',
        description: 'Télécharger relevés'
      },
      { 
        path: '/client/profil', 
        icon: UserCheck, 
        label: 'Mon Profil',
        description: 'Infos personnelles'
      },
      { 
        path: '/client/securite', 
        icon: Lock, 
        label: 'Sécurité Client',
        description: 'PIN, 2FA, appareils'
      },
    ]
  },

  // ==================== MODULE ADMIN TECHNIQUE ====================
  {
    section: 'MODULE ADMIN TECHNIQUE',
    module: 'tech',
    color: 'primary',
    items: [
      { 
        path: '/tech/monitoring', 
        icon: Server, 
        label: 'Monitoring Système',
        description: 'État serveurs et API'
      },
      { 
        path: '/tech/cartographie-agents', 
        icon: Globe, 
        label: 'Cartographie Agents',
        description: 'Carte agents Burundi'
      },
      { 
        path: '/tech/performance', 
        icon: Zap, 
        label: 'Performance',
        description: 'Temps réponse, métriques'
      },
      { 
        path: '/tech/api', 
        icon: Globe, 
        label: 'API Partenaires',
        description: 'Gestion intégrations'
      },
      { 
        path: '/tech/webhooks', 
        icon: Zap, 
        label: 'Webhooks',
        description: 'Configuration callbacks'
      },
      { 
        path: '/tech/sms', 
        icon: Smartphone, 
        label: 'SMS Gateway',
        description: 'Configuration SMS'
      },
      { 
        path: '/tech/email', 
        icon: Mail, 
        label: 'Email Service',
        description: 'Configuration emails'
      },
      { 
        path: '/tech/logs', 
        icon: FileText, 
        label: 'Logs Système',
        description: 'Logs transactions/erreurs'
      },
      { 
        path: '/tech/maintenance', 
        icon: Settings, 
        label: 'Maintenance',
        description: 'Backup, mises à jour'
      },
      { 
        path: '/tech/firewall', 
        icon: Shield, 
        label: 'Firewall & Sécurité',
        description: 'Config sécurité'
      },
      { 
        path: '/tech/detection', 
        icon: AlertTriangle, 
        label: 'Détection Anomalies',
        description: 'Analyse comportementale'
      },
      { 
        path: '/tech/database', 
        icon: Database, 
        label: 'Base de Données',
        description: 'Gestion BDD'
      },
    ]
  },
];

export default allModulesNavigation;
