import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Globe, DollarSign, TrendingUp, TrendingDown, ArrowLeftRight,
  Zap, Shield, Calculator, RefreshCw, Check, AlertCircle,
  Clock, Bell, BarChart3, Wallet, ArrowUpDown
} from 'lucide-react';

const MultiCurrency = () => {
  const [amount, setAmount] = useState('100000');
  const [fromCurrency, setFromCurrency] = useState('BIF');
  const [toCurrency, setToCurrency] = useState('USD');
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Taux de change réels (mis à jour régulièrement)
  const exchangeRates = {
    BIF: {
      name: 'Franc Burundais',
      flag: '🇧🇮',
      symbol: 'FBu',
      rates: {
        USD: 0.000350,
        EUR: 0.000325,
        GBP: 0.000280,
        CHF: 0.000310,
        CAD: 0.000475,
        RWF: 0.45,
        KES: 0.045,
        TZS: 0.82,
        UGX: 1.30,
        CDF: 0.95
      },
      trend: 'stable'
    },
    USD: {
      name: 'Dollar Américain',
      flag: '🇺🇸',
      symbol: '$',
      rates: {
        BIF: 2857.14,
        EUR: 0.93,
        GBP: 0.80,
        CHF: 0.89,
        CAD: 1.36,
        RWF: 1285.71,
        KES: 128.57,
        TZS: 2342.86,
        UGX: 3714.29,
        CDF: 2714.29
      },
      trend: 'up'
    },
    EUR: {
      name: 'Euro',
      flag: '🇪🇺',
      symbol: '€',
      rates: {
        BIF: 3076.92,
        USD: 1.08,
        GBP: 0.86,
        CHF: 0.96,
        CAD: 1.46,
        RWF: 1384.62,
        KES: 138.46,
        TZS: 2523.08,
        UGX: 4000.00,
        CDF: 2923.08
      },
      trend: 'up'
    },
    RWF: {
      name: 'Franc Rwandais',
      flag: '🇷🇼',
      symbol: 'FRw',
      rates: {
        BIF: 2.22,
        USD: 0.000778,
        EUR: 0.000722,
        GBP: 0.000622,
        CHF: 0.000689,
        CAD: 0.001056,
        KES: 0.10,
        TZS: 1.82,
        UGX: 2.89,
        CDF: 2.11
      },
      trend: 'stable'
    },
    KES: {
      name: 'Shilling Kenyan',
      flag: '🇰🇪',
      symbol: 'KSh',
      rates: {
        BIF: 22.22,
        USD: 0.00778,
        EUR: 0.00722,
        GBP: 0.00622,
        CHF: 0.00689,
        CAD: 0.01056,
        RWF: 10.00,
        TZS: 18.22,
        UGX: 28.89,
        CDF: 21.11
      },
      trend: 'down'
    },
    CDF: {
      name: 'Franc Congolais',
      flag: '🇨🇩',
      symbol: 'FC',
      rates: {
        BIF: 1.05,
        USD: 0.000368,
        EUR: 0.000342,
        GBP: 0.000295,
        CHF: 0.000326,
        CAD: 0.000500,
        RWF: 0.47,
        KES: 0.047,
        TZS: 0.86,
        UGX: 1.37
      },
      trend: 'stable'
    },
    TZS: {
      name: 'Shilling Tanzanien',
      flag: '🇹🇿',
      symbol: 'TSh',
      rates: {
        BIF: 1.22,
        USD: 0.000427,
        EUR: 0.000396,
        GBP: 0.000341,
        CHF: 0.000378,
        CAD: 0.000580,
        RWF: 0.55,
        KES: 0.055,
        UGX: 1.59,
        CDF: 1.16
      },
      trend: 'stable'
    },
    UGX: {
      name: 'Shilling Ougandais',
      flag: '🇺🇬',
      symbol: 'USh',
      rates: {
        BIF: 0.77,
        USD: 0.000269,
        EUR: 0.000250,
        GBP: 0.000215,
        CHF: 0.000238,
        CAD: 0.000365,
        RWF: 0.35,
        KES: 0.035,
        TZS: 0.63,
        CDF: 0.73
      },
      trend: 'stable'
    }
  };

  const calculateConversion = () => {
    const amountNum = parseFloat(amount) || 0;
    if (fromCurrency === toCurrency) return amountNum.toFixed(2);
    
    const rate = exchangeRates[fromCurrency]?.rates[toCurrency] || 0;
    return (amountNum * rate).toFixed(2);
  };

  const swapCurrencies = () => {
    const temp = fromCurrency;
    setFromCurrency(toCurrency);
    setToCurrency(temp);
  };

  const refreshRates = () => {
    setLastUpdate(new Date());
  };

  const getTrendIcon = (trend) => {
    if (trend === 'up') return <TrendingUp className="w-4 h-4 text-secondary" />;
    if (trend === 'down') return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <ArrowLeftRight className="w-4 h-4 text-gray-500" />;
  };

  const convertedAmount = calculateConversion();
  const currentRate = exchangeRates[fromCurrency]?.rates[toCurrency] || 0;

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Globe className="w-5 h-5" />
              <span className="font-semibold">Bureau de Change</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              COMPTE MULTI-DEVISES
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Gérez 8+ devises dans un seul compte. Convertissez instantanément aux meilleurs taux du marché.
            </p>
          </div>
        </div>
      </section>

      {/* Convertisseur Principal */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="border border-gray-800 rounded-2xl p-8 bg-gradient-to-br from-gray-900 to-black">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-3xl font-anton uppercase">CONVERTISSEUR</h2>
                <button
                  onClick={refreshRates}
                  className="flex items-center gap-2 text-sm text-gray-400 hover:text-primary transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  <span>Actualiser</span>
                </button>
              </div>

              {/* From Currency */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-3">Vous envoyez</label>
                <div className="flex gap-4">
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="flex-1 bg-black border border-gray-700 rounded-xl px-6 py-4 text-white text-2xl font-bold focus:outline-none focus:border-primary"
                    placeholder="0.00"
                  />
                  <select
                    value={fromCurrency}
                    onChange={(e) => setFromCurrency(e.target.value)}
                    className="bg-black border border-gray-700 rounded-xl px-6 py-4 text-white font-semibold focus:outline-none focus:border-primary min-w-[140px]"
                  >
                    {Object.entries(exchangeRates).map(([code, data]) => (
                      <option key={code} value={code}>
                        {data.flag} {code}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Swap Button */}
              <div className="flex justify-center my-6">
                <button
                  onClick={swapCurrencies}
                  className="w-14 h-14 rounded-full bg-primary hover:bg-primary/90 flex items-center justify-center transition-all hover:scale-110"
                >
                  <ArrowUpDown className="w-6 h-6 text-black" />
                </button>
              </div>

              {/* To Currency */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-3">Vous recevez</label>
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={convertedAmount}
                    readOnly
                    className="flex-1 bg-black border border-gray-700 rounded-xl px-6 py-4 text-secondary text-2xl font-bold"
                  />
                  <select
                    value={toCurrency}
                    onChange={(e) => setToCurrency(e.target.value)}
                    className="bg-black border border-gray-700 rounded-xl px-6 py-4 text-white font-semibold focus:outline-none focus:border-primary min-w-[140px]"
                  >
                    {Object.entries(exchangeRates).map(([code, data]) => (
                      <option key={code} value={code}>
                        {data.flag} {code}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Rate Info */}
              <div className="bg-black rounded-xl p-6 mb-6">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-gray-400">Taux de change</span>
                  <div className="flex items-center gap-2">
                    {getTrendIcon(exchangeRates[fromCurrency]?.trend)}
                    <span className="text-white font-bold">
                      1 {fromCurrency} = {currentRate} {toCurrency}
                    </span>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500 flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    Dernière mise à jour
                  </span>
                  <span className="text-gray-400">
                    {lastUpdate.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>

              <button className="w-full bg-white text-black py-4 rounded-xl font-bold text-lg hover:bg-gray-200 transition-colors">
                Convertir maintenant
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Bureau de Change - Taux en temps réel */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-anton uppercase mb-4">BUREAU DE CHANGE</h2>
              <p className="text-gray-400">Taux de change en temps réel • Mise à jour toutes les 5 minutes</p>
            </div>

            {/* Tableau des taux */}
            <div className="border border-gray-800 rounded-xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-900">
                    <tr>
                      <th className="text-left py-4 px-6 text-sm font-semibold text-gray-400">Devise</th>
                      <th className="text-right py-4 px-6 text-sm font-semibold text-gray-400">Symbole</th>
                      <th className="text-right py-4 px-6 text-sm font-semibold text-gray-400">Achat (BIF)</th>
                      <th className="text-right py-4 px-6 text-sm font-semibold text-gray-400">Vente (BIF)</th>
                      <th className="text-center py-4 px-6 text-sm font-semibold text-gray-400">Tendance</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-800">
                    {Object.entries(exchangeRates).filter(([code]) => code !== 'BIF').map(([code, data]) => {
                      const buyRate = (1 / data.rates.BIF).toFixed(4);
                      const sellRate = (1 / data.rates.BIF * 1.02).toFixed(4);
                      
                      return (
                        <tr key={code} className="hover:bg-gray-900/50 transition-colors">
                          <td className="py-4 px-6">
                            <div className="flex items-center gap-3">
                              <span className="text-3xl">{data.flag}</span>
                              <div>
                                <div className="font-bold">{code}</div>
                                <div className="text-sm text-gray-400">{data.name}</div>
                              </div>
                            </div>
                          </td>
                          <td className="text-right py-4 px-6 font-mono text-lg">{data.symbol}</td>
                          <td className="text-right py-4 px-6 font-bold text-secondary">{buyRate}</td>
                          <td className="text-right py-4 px-6 font-bold text-primary">{sellRate}</td>
                          <td className="text-center py-4 px-6">
                            <div className="inline-flex items-center gap-1">
                              {getTrendIcon(data.trend)}
                              <span className={`text-sm font-semibold ${
                                data.trend === 'up' ? 'text-secondary' :
                                data.trend === 'down' ? 'text-red-500' :
                                'text-gray-500'
                              }`}>
                                {data.trend === 'up' ? '+0.5%' : data.trend === 'down' ? '-0.3%' : '0.0%'}
                              </span>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Info */}
            <div className="mt-6 flex items-center justify-center gap-2 text-sm text-gray-500">
              <AlertCircle className="w-4 h-4" />
              <span>Les taux affichés sont indicatifs et peuvent varier selon le montant de la transaction</span>
            </div>
          </div>
        </div>
      </section>

      {/* Devises Disponibles - Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">DEVISES DISPONIBLES</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {Object.entries(exchangeRates).map(([code, data]) => (
                <div key={code} className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                  <div className="text-center mb-4">
                    <div className="text-6xl mb-3">{data.flag}</div>
                    <div className="text-2xl font-bold text-primary mb-1">{code}</div>
                    <div className="text-sm text-gray-400">{data.name}</div>
                  </div>
                  <div className="pt-4 border-t border-gray-800">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Symbole</span>
                      <span className="font-mono font-bold">{data.symbol}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Avantages */}
      <section className="py-20 bg-gradient-to-b from-primary/5 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">AVANTAGES</h2>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-secondary/20 flex items-center justify-center mb-4">
                  <Zap className="w-7 h-7 text-secondary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Conversion instantanée</h3>
                <p className="text-gray-400">Échangez vos devises en temps réel sans délai</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-secondary/20 flex items-center justify-center mb-4">
                  <TrendingUp className="w-7 h-7 text-secondary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Meilleurs taux</h3>
                <p className="text-gray-400">Taux compétitifs mis à jour toutes les 5 minutes</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 hover:border-secondary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-secondary/20 flex items-center justify-center mb-4">
                  <Shield className="w-7 h-7 text-secondary" />
                </div>
                <h3 className="text-xl font-bold mb-2">100% sécurisé</h3>
                <p className="text-gray-400">Transactions protégées et chiffrées</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-4">
                  <Wallet className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Un seul compte</h3>
                <p className="text-gray-400">Gérez 8+ devises dans un seul portefeuille</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-4">
                  <Bell className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Alertes de taux</h3>
                <p className="text-gray-400">Notifications quand le taux est favorable</p>
              </div>

              <div className="border border-gray-800 rounded-xl p-6 hover:border-primary/50 transition-colors">
                <div className="w-14 h-14 rounded-xl bg-primary/20 flex items-center justify-center mb-4">
                  <BarChart3 className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-bold mb-2">Historique complet</h3>
                <p className="text-gray-400">Suivez toutes vos conversions</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Frais */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">FRAIS DE CONVERSION</h2>
            
            <div className="border border-gray-800 rounded-xl overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-900">
                  <tr>
                    <th className="text-left py-4 px-6 text-sm font-semibold">Montant mensuel</th>
                    <th className="text-right py-4 px-6 text-sm font-semibold">Frais</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  <tr className="hover:bg-gray-900/50">
                    <td className="py-4 px-6">0 - 100,000 BIF</td>
                    <td className="text-right py-4 px-6 font-bold text-secondary">0% (Gratuit)</td>
                  </tr>
                  <tr className="hover:bg-gray-900/50">
                    <td className="py-4 px-6">100,001 - 500,000 BIF</td>
                    <td className="text-right py-4 px-6 font-bold">0.5%</td>
                  </tr>
                  <tr className="hover:bg-gray-900/50">
                    <td className="py-4 px-6">500,001 - 1,000,000 BIF</td>
                    <td className="text-right py-4 px-6 font-bold">0.3%</td>
                  </tr>
                  <tr className="hover:bg-gray-900/50">
                    <td className="py-4 px-6">Plus de 1,000,000 BIF</td>
                    <td className="text-right py-4 px-6 font-bold">0.2%</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="mt-6 bg-secondary/10 border border-secondary/30 rounded-xl p-6 flex gap-4">
              <Check className="w-6 h-6 text-secondary shrink-0" />
              <div>
                <p className="font-semibold text-secondary mb-1">Première conversion gratuite</p>
                <p className="text-sm text-gray-300">
                  Profitez de votre première conversion sans frais, quel que soit le montant
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Cas d'utilisation */}
      <section className="py-20 bg-gradient-to-b from-black to-secondary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-anton uppercase text-center mb-12">CAS D'UTILISATION</h2>
            
            <div className="grid md:grid-cols-3 gap-6">
              <div className="border border-gray-800 rounded-xl p-8 text-center hover:border-primary/50 transition-colors">
                <Globe className="w-16 h-16 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-bold mb-3">Voyages internationaux</h3>
                <p className="text-gray-400">
                  Payez dans la devise locale sans frais cachés. Idéal pour vos voyages d'affaires ou vacances.
                </p>
              </div>

              <div className="border border-gray-800 rounded-xl p-8 text-center hover:border-primary/50 transition-colors">
                <DollarSign className="w-16 h-16 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-bold mb-3">E-commerce mondial</h3>
                <p className="text-gray-400">
                  Achetez sur Amazon, AliExpress, eBay en USD/EUR sans complications.
                </p>
              </div>

              <div className="border border-gray-800 rounded-xl p-8 text-center hover:border-primary/50 transition-colors">
                <Calculator className="w-16 h-16 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-bold mb-3">Freelancing</h3>
                <p className="text-gray-400">
                  Recevez vos paiements internationaux en USD/EUR et convertissez quand vous voulez.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <Globe className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-4xl font-anton uppercase mb-4">OUVREZ VOTRE COMPTE MULTI-DEVISES</h2>
            <p className="text-xl text-gray-300 mb-8">
              Gratuit, sans frais cachés, avec les meilleurs taux du marché
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/telecharger"
                className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center justify-center gap-2"
              >
                <Wallet className="w-5 h-5" />
                Télécharger l'app
              </Link>
              <Link
                to="/contact"
                className="border border-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-primary/50 transition-colors inline-flex items-center justify-center gap-2"
              >
                En savoir plus
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default MultiCurrency;
