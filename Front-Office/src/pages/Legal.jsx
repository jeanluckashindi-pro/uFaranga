import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import {
  FileText, Lock, Cookie, Scale, Shield, CheckCircle,
  AlertCircle, Eye, Database, UserCheck, Building2
} from 'lucide-react';

const Legal = () => {
  const location = useLocation();
  const hash = location.hash;

  useEffect(() => {
    if (hash) {
      const element = document.querySelector(hash);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  }, [hash]);

  const sections = [
    { id: 'terms', title: 'Conditions d\'utilisation', icon: FileText },
    { id: 'privacy', title: 'Politique de confidentialité', icon: Lock },
    { id: 'cookies', title: 'Politique de cookies', icon: Cookie },
    { id: 'mentions', title: 'Mentions légales', icon: Scale },
    { id: 'aml', title: 'Lutte anti-blanchiment', icon: Shield }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero */}
      <section className="py-20 bg-gradient-to-b from-primary/10 to-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Scale className="w-5 h-5" />
              <span className="font-semibold">Informations Légales</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-anton uppercase mb-6">
              MENTIONS LÉGALES
            </h1>
            <p className="text-xl text-gray-300">
              Transparence et conformité réglementaire
            </p>
          </div>
        </div>
      </section>

      {/* Navigation */}
      <section className="sticky top-0 z-40 bg-black/95 backdrop-blur-sm border-b border-gray-800 py-4">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-3">
            {sections.map((section) => (
              <a
                key={section.id}
                href={`#${section.id}`}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors inline-flex items-center gap-2 ${
                  hash === `#${section.id}`
                    ? 'bg-primary text-black'
                    : 'border border-gray-700 hover:border-primary/50'
                }`}
              >
                <section.icon className="w-4 h-4" />
                <span className="hidden sm:inline">{section.title}</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto space-y-20">
            {/* Terms */}
            <div id="terms" className="scroll-mt-24">
              <div className="border border-gray-800 rounded-xl p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                    <FileText className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-anton uppercase">CONDITIONS D'UTILISATION</h2>
                    <p className="text-sm text-gray-500">Dernière mise à jour : 10 février 2026</p>
                  </div>
                </div>

                <div className="space-y-6 text-gray-300">
                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      1. Acceptation des conditions
                    </h3>
                    <p className="leading-relaxed">
                      En utilisant les services uFaranga, vous acceptez les présentes conditions d'utilisation dans leur intégralité. 
                      Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser nos services.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      2. Description du service
                    </h3>
                    <p className="leading-relaxed mb-3">
                      uFaranga est une plateforme de services financiers mobiles permettant d'effectuer :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Transferts d'argent nationaux et internationaux</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Paiements marchands et factures</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Épargne et tontines</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Micro-crédit et services bancaires</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      3. Conditions d'éligibilité
                    </h3>
                    <p className="leading-relaxed">
                      Pour utiliser uFaranga, vous devez avoir au moins 18 ans et être légalement capable de contracter. 
                      Vous devez fournir des informations exactes et à jour lors de votre inscription.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      4. Responsabilités de l'utilisateur
                    </h3>
                    <p className="leading-relaxed mb-3">
                      Vous vous engagez à :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Maintenir la confidentialité de vos identifiants</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Ne pas utiliser le service à des fins illégales</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Respecter les limites de transaction</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span>Signaler toute activité suspecte</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      5. Frais et tarification
                    </h3>
                    <p className="leading-relaxed">
                      Les frais applicables sont affichés avant chaque transaction. uFaranga se réserve le droit de modifier 
                      ses tarifs avec un préavis de 30 jours.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-primary" />
                      6. Résiliation
                    </h3>
                    <p className="leading-relaxed">
                      Vous pouvez fermer votre compte à tout moment. uFaranga se réserve le droit de suspendre ou fermer 
                      un compte en cas de violation des conditions d'utilisation.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Privacy */}
            <div id="privacy" className="scroll-mt-24">
              <div className="border border-gray-800 rounded-xl p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-secondary/20 flex items-center justify-center">
                    <Lock className="w-6 h-6 text-secondary" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-anton uppercase">POLITIQUE DE CONFIDENTIALITÉ</h2>
                    <p className="text-sm text-gray-500">Dernière mise à jour : 10 février 2026</p>
                  </div>
                </div>

                <div className="space-y-6 text-gray-300">
                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <Database className="w-5 h-5 text-secondary" />
                      Collecte des données
                    </h3>
                    <p className="leading-relaxed mb-3">
                      Nous collectons les données suivantes :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Informations d'identification (nom, prénom, date de naissance)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Coordonnées (email, téléphone, adresse)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Données de transaction (montants, dates, bénéficiaires)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Données techniques (adresse IP, type d'appareil)</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <Eye className="w-5 h-5 text-secondary" />
                      Utilisation des données
                    </h3>
                    <p className="leading-relaxed mb-3">
                      Vos données sont utilisées pour :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Fournir et améliorer nos services</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Prévenir la fraude et assurer la sécurité</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Respecter nos obligations légales et réglementaires</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Vous contacter concernant votre compte</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <Shield className="w-5 h-5 text-secondary" />
                      Protection des données
                    </h3>
                    <p className="leading-relaxed">
                      Nous utilisons des mesures de sécurité de niveau bancaire incluant le chiffrement AES-256, 
                      l'authentification multi-facteurs et des audits de sécurité réguliers.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <UserCheck className="w-5 h-5 text-secondary" />
                      Vos droits
                    </h3>
                    <p className="leading-relaxed mb-3">
                      Conformément au RGPD, vous disposez des droits suivants :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Droit d'accès à vos données personnelles</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Droit de rectification des données inexactes</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Droit à l'effacement (droit à l'oubli)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Droit à la portabilité de vos données</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-secondary mt-1">•</span>
                        <span>Droit d'opposition au traitement</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5 text-secondary" />
                      Conservation des données
                    </h3>
                    <p className="leading-relaxed">
                      Nous conservons vos données pendant la durée nécessaire à la fourniture de nos services et 
                      conformément aux obligations légales (minimum 5 ans pour les données de transaction).
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Cookies */}
            <div id="cookies" className="scroll-mt-24">
              <div className="border border-gray-800 rounded-xl p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                    <Cookie className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-anton uppercase">POLITIQUE DE COOKIES</h2>
                    <p className="text-sm text-gray-500">Dernière mise à jour : 10 février 2026</p>
                  </div>
                </div>

                <div className="space-y-6 text-gray-300">
                  <p className="leading-relaxed">
                    Nous utilisons des cookies et technologies similaires pour améliorer votre expérience sur notre plateforme.
                  </p>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Types de cookies utilisés</h3>
                    <div className="space-y-4">
                      <div className="p-4 rounded-lg bg-gray-900/50">
                        <h4 className="font-semibold mb-2">Cookies essentiels</h4>
                        <p className="text-sm text-gray-400">
                          Nécessaires au fonctionnement du site (authentification, sécurité, préférences)
                        </p>
                      </div>
                      <div className="p-4 rounded-lg bg-gray-900/50">
                        <h4 className="font-semibold mb-2">Cookies de performance</h4>
                        <p className="text-sm text-gray-400">
                          Nous aident à comprendre comment vous utilisez notre site pour l'améliorer
                        </p>
                      </div>
                      <div className="p-4 rounded-lg bg-gray-900/50">
                        <h4 className="font-semibold mb-2">Cookies fonctionnels</h4>
                        <p className="text-sm text-gray-400">
                          Mémorisent vos préférences et personnalisent votre expérience
                        </p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Gestion des cookies</h3>
                    <p className="leading-relaxed">
                      Vous pouvez gérer vos préférences de cookies à tout moment via les paramètres de votre navigateur. 
                      Notez que la désactivation de certains cookies peut affecter le fonctionnement du site.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Mentions légales */}
            <div id="mentions" className="scroll-mt-24">
              <div className="border border-gray-800 rounded-xl p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-secondary/20 flex items-center justify-center">
                    <Building2 className="w-6 h-6 text-secondary" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-anton uppercase">MENTIONS LÉGALES</h2>
                    <p className="text-sm text-gray-500">Informations sur l'entreprise</p>
                  </div>
                </div>

                <div className="space-y-6 text-gray-300">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="font-bold mb-2">Raison sociale</h3>
                      <p>uFaranga SARL</p>
                    </div>
                    <div>
                      <h3 className="font-bold mb-2">Forme juridique</h3>
                      <p>Société à Responsabilité Limitée</p>
                    </div>
                    <div>
                      <h3 className="font-bold mb-2">Siège social</h3>
                      <p>Avenue de la Liberté<br />Bujumbura, Burundi</p>
                    </div>
                    <div>
                      <h3 className="font-bold mb-2">Registre de commerce</h3>
                      <p>RC/BJM/2024/12345</p>
                    </div>
                    <div>
                      <h3 className="font-bold mb-2">NIF</h3>
                      <p>4000123456</p>
                    </div>
                    <div>
                      <h3 className="font-bold mb-2">Capital social</h3>
                      <p>500,000,000 BIF</p>
                    </div>
                  </div>

                  <div className="pt-6 border-t border-gray-800">
                    <h3 className="font-bold mb-3">Contact</h3>
                    <div className="space-y-2">
                      <p>Email : <a href="mailto:legal@ufaranga.com" className="text-primary hover:underline">legal@ufaranga.com</a></p>
                      <p>Téléphone : <a href="tel:+25779123456" className="text-primary hover:underline">+257 79 123 456</a></p>
                      <p>Support : <a href="mailto:support@ufaranga.com" className="text-primary hover:underline">support@ufaranga.com</a></p>
                    </div>
                  </div>

                  <div className="pt-6 border-t border-gray-800">
                    <h3 className="font-bold mb-3">Régulation</h3>
                    <p className="leading-relaxed">
                      uFaranga est régulé et supervisé par la Banque de la République du Burundi (BRB) 
                      en tant qu'établissement de paiement agréé.
                    </p>
                  </div>

                  <div className="pt-6 border-t border-gray-800">
                    <h3 className="font-bold mb-3">Hébergement</h3>
                    <p className="leading-relaxed">
                      Ce site est hébergé par AWS (Amazon Web Services)<br />
                      410 Terry Avenue North, Seattle, WA 98109, USA
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* AML */}
            <div id="aml" className="scroll-mt-24">
              <div className="border border-gray-800 rounded-xl p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                    <Shield className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h2 className="text-3xl font-anton uppercase">LUTTE ANTI-BLANCHIMENT</h2>
                    <p className="text-sm text-gray-500">Politique AML/CFT</p>
                  </div>
                </div>

                <div className="space-y-6 text-gray-300">
                  <p className="leading-relaxed">
                    uFaranga respecte strictement les réglementations en matière de lutte contre le blanchiment d'argent (AML) 
                    et le financement du terrorisme (CFT).
                  </p>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Vérification d'identité (KYC)</h3>
                    <p className="leading-relaxed mb-3">
                      Tous les utilisateurs doivent fournir :
                    </p>
                    <ul className="space-y-2 ml-6">
                      <li className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                        <span>Une pièce d'identité valide (carte d'identité, passeport)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                        <span>Une preuve de domicile récente</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                        <span>Des informations sur la source des fonds</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Surveillance des transactions</h3>
                    <p className="leading-relaxed">
                      Nous surveillons en permanence les transactions pour détecter toute activité suspecte. 
                      Les transactions inhabituelles peuvent faire l'objet d'une vérification supplémentaire.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Déclaration des opérations suspectes</h3>
                    <p className="leading-relaxed">
                      Conformément à la loi, nous sommes tenus de déclarer toute opération suspecte aux autorités compétentes 
                      sans en informer le client concerné.
                    </p>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold mb-3">Limites de transaction</h3>
                    <p className="leading-relaxed">
                      Des limites de transaction sont appliquées en fonction du niveau de vérification de votre compte 
                      pour prévenir le blanchiment d'argent.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-b from-black to-primary/5">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto border border-primary/30 rounded-xl p-12 text-center bg-gradient-to-r from-primary/10 to-secondary/10">
            <Scale className="w-16 h-16 text-primary mx-auto mb-6" />
            <h2 className="text-4xl font-anton uppercase mb-4">QUESTIONS LÉGALES ?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Notre équipe juridique est à votre disposition
            </p>
            <a
              href="/contact"
              className="bg-white text-black px-8 py-4 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
            >
              Nous contacter
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Legal;
