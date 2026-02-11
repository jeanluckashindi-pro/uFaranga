import React from 'react';
import { Webhook, Zap, Shield, Code, CheckCircle, Bell } from 'lucide-react';
import GlassCard from '../components/ui/GlassCard';
import GradientButton from '../components/ui/GradientButton';
import Section from '../components/ui/Section';

const Webhooks = () => {
  const events = [
    { name: 'payment.success', description: 'Paiement réussi' },
    { name: 'payment.failed', description: 'Paiement échoué' },
    { name: 'transfer.completed', description: 'Transfert complété' },
    { name: 'refund.processed', description: 'Remboursement traité' },
    { name: 'account.updated', description: 'Compte mis à jour' },
    { name: 'kyc.verified', description: 'KYC vérifié' },
  ];

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[40%] h-[40%] bg-primary/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-[40%] h-[40%] bg-secondary/10 rounded-full blur-[120px]"></div>
      </div>

      <Section className="relative z-10">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
            <Webhook className="w-10 h-10 text-primary" />
          </div>
          <h1 className="text-5xl md:text-6xl font-anton uppercase mb-6">Webhooks</h1>
          <p className="text-xl text-gray-300 mb-8">
            Recevez des notifications en temps réel pour tous les événements importants
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Zap className="w-12 h-12 text-primary mx-auto mb-4" />
            <h3 className="text-xl font-bold mb-2">Temps réel</h3>
            <p className="text-gray-400">Notifications instantanées</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Shield className="w-12 h-12 text-secondary mx-auto mb-4" />
            <h3 className="text-xl font-bold mb-2">Sécurisé</h3>
            <p className="text-gray-400">Signature HMAC SHA-256</p>
          </GlassCard>
          <GlassCard className="bg-black/40 border-white/10 p-6 text-center">
            <Bell className="w-12 h-12 text-purple-400 mx-auto mb-4" />
            <h3 className="text-xl font-bold mb-2">Fiable</h3>
            <p className="text-gray-400">Retry automatique</p>
          </GlassCard>
        </div>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Événements disponibles</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {events.map((event, i) => (
              <div key={i} className="flex items-center gap-3 bg-white/5 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-secondary shrink-0" />
                <div>
                  <div className="font-mono text-sm text-primary">{event.name}</div>
                  <div className="text-xs text-gray-400">{event.description}</div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard className="bg-black/40 border-white/10 p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Exemple de payload</h2>
          <div className="bg-[#0d1117] rounded-xl p-6 overflow-x-auto">
            <pre className="text-sm text-gray-300">
              <code>{`{
  "event": "payment.success",
  "timestamp": "2024-02-11T10:30:00Z",
  "data": {
    "id": "pay_abc123",
    "amount": 50000,
    "currency": "BIF",
    "status": "completed",
    "customer": {
      "id": "cust_xyz789",
      "phone": "+25779123456"
    }
  },
  "signature": "sha256=..."
}`}</code>
            </pre>
          </div>
        </GlassCard>

        <GlassCard className="bg-black/40 border-white/10 p-8">
          <h2 className="text-2xl font-bold mb-6">Configuration</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">URL du webhook</label>
              <input
                type="url"
                placeholder="https://votre-site.com/webhooks/ufaranga"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary transition-colors"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Secret de signature</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value="whsec_••••••••••••••••"
                  readOnly
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white"
                />
                <button className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-colors">
                  Régénérer
                </button>
              </div>
            </div>
            <GradientButton className="w-full">Enregistrer la configuration</GradientButton>
          </div>
        </GlassCard>
      </Section>
    </div>
  );
};

export default Webhooks;
