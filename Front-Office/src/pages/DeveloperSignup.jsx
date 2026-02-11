import { useState } from 'react';
import {
  User, Building2, Mail, Phone, Lock, Globe, Code,
  FileText, Key, Shield, CheckCircle, ArrowRight, ArrowLeft,
  Upload, Eye, EyeOff, AlertCircle, Smartphone, CreditCard,
  FileCheck, Server, Webhook, Settings
} from 'lucide-react';

const DeveloperSignup = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [accountType, setAccountType] = useState('individual');
  const [formData, setFormData] = useState({
    // Step 1: Informations du développeur
    fullName: '',
    accountType: 'individual',
    country: '',
    email: '',
    phone: '',
    
    // Step 2: Sécurité
    password: '',
    confirmPassword: '',
    enable2FA: false,
    twoFAMethod: 'sms',
    
    // Step 3: Vérification (KYC)
    idType: 'passport',
    idNumber: '',
    idFile: null,
    selfieFile: null,
    // Entreprise
    companyName: '',
    registrationNumber: '',
    nif: '',
    legalAddress: '',
    legalRepName: '',
    legalRepIdFile: null,
    
    // Step 4: Informations techniques
    appName: '',
    appDescription: '',
    websiteUrl: '',
    callbackUrl: '',
    webhookUrl: '',
    platform: [],
    environment: 'sandbox',
    
    // Step 5: Configuration paiement
    currency: 'BIF',
    paymentMethods: [],
    transactionLimit: '1000000',
    
    // Step 6: Acceptation
    acceptTerms: false,
    acceptPrivacy: false,
    acceptCompliance: false
  });

  const totalSteps = 6;

  const steps = [
    { number: 1, title: 'Informations', icon: User },
    { number: 2, title: 'Sécurité', icon: Lock },
    { number: 3, title: 'Vérification', icon: Shield },
    { number: 4, title: 'Technique', icon: Code },
    { number: 5, title: 'Paiement', icon: CreditCard },
    { number: 6, title: 'Validation', icon: CheckCircle }
  ];

  const countries = [
    'Burundi', 'Rwanda', 'RD Congo', 'Kenya', 'Tanzanie', 'Ouganda', 'France', 'Belgique', 'Canada', 'Autre'
  ];

  const platforms = ['Web', 'Android', 'iOS', 'Desktop'];
  const paymentMethods = ['Mobile Money', 'Carte bancaire', 'Virement bancaire', 'Crypto'];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleFileChange = (e, fieldName) => {
    const file = e.target.files[0];
    setFormData(prev => ({
      ...prev,
      [fieldName]: file
    }));
  };

  const handlePlatformToggle = (platform) => {
    setFormData(prev => ({
      ...prev,
      platform: prev.platform.includes(platform)
        ? prev.platform.filter(p => p !== platform)
        : [...prev.platform, platform]
    }));
  };

  const handlePaymentMethodToggle = (method) => {
    setFormData(prev => ({
      ...prev,
      paymentMethods: prev.paymentMethods.includes(method)
        ? prev.paymentMethods.filter(m => m !== method)
        : [...prev.paymentMethods, method]
    }));
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Ici, envoyer les données au backend
    alert('Compte développeur créé avec succès! Vérifiez votre email pour activer votre compte.');
  };

  return (
    <div className="min-h-screen bg-black py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 bg-primary/20 text-primary px-4 py-2 rounded-full mb-6">
              <Code className="w-5 h-5" />
              <span className="font-semibold">Inscription Développeur</span>
            </div>
            <h1 className="text-4xl lg:text-5xl font-anton uppercase mb-4">
              CRÉER UN COMPTE DÉVELOPPEUR
            </h1>
            <p className="text-gray-400">
              Accédez à l'API uFaranga et intégrez les paiements mobiles dans vos applications
            </p>
          </div>

          {/* Progress Steps */}
          <div className="mb-12">
            <div className="flex items-center justify-between">
              {steps.map((step, index) => (
                <div key={step.number} className="flex items-center flex-1">
                  <div className="flex flex-col items-center flex-1">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-all ${
                      currentStep >= step.number
                        ? 'bg-primary border-primary text-black'
                        : 'border-gray-700 text-gray-500'
                    }`}>
                      {currentStep > step.number ? (
                        <CheckCircle className="w-6 h-6" />
                      ) : (
                        <step.icon className="w-6 h-6" />
                      )}
                    </div>
                    <span className={`text-xs mt-2 hidden md:block ${
                      currentStep >= step.number ? 'text-white' : 'text-gray-500'
                    }`}>
                      {step.title}
                    </span>
                  </div>
                  {index < steps.length - 1 && (
                    <div className={`h-0.5 flex-1 transition-all ${
                      currentStep > step.number ? 'bg-primary' : 'bg-gray-800'
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit}>
            <div className="border border-gray-800 rounded-xl p-8 mb-6">

              {/* Step 1: Informations du développeur */}
              {currentStep === 1 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">INFORMATIONS DU DÉVELOPPEUR</h2>
                  
                  {/* Type de compte */}
                  <div>
                    <label className="block text-sm font-semibold mb-3">Type de compte *</label>
                    <div className="grid md:grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={() => {
                          setAccountType('individual');
                          setFormData(prev => ({ ...prev, accountType: 'individual' }));
                        }}
                        className={`p-6 rounded-xl border-2 transition-all text-left ${
                          accountType === 'individual'
                            ? 'border-primary bg-primary/10'
                            : 'border-gray-800 hover:border-gray-700'
                        }`}
                      >
                        <User className="w-8 h-8 text-primary mb-3" />
                        <div className="font-bold mb-1">Individuel</div>
                        <div className="text-sm text-gray-400">Pour développeurs indépendants</div>
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setAccountType('company');
                          setFormData(prev => ({ ...prev, accountType: 'company' }));
                        }}
                        className={`p-6 rounded-xl border-2 transition-all text-left ${
                          accountType === 'company'
                            ? 'border-primary bg-primary/10'
                            : 'border-gray-800 hover:border-gray-700'
                        }`}
                      >
                        <Building2 className="w-8 h-8 text-primary mb-3" />
                        <div className="font-bold mb-1">Entreprise / Startup</div>
                        <div className="text-sm text-gray-400">Pour organisations</div>
                      </button>
                    </div>
                  </div>

                  {/* Nom complet */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">
                      {accountType === 'individual' ? 'Nom complet *' : 'Nom de l\'entreprise *'}
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="text"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder={accountType === 'individual' ? 'Jean Dupont' : 'Ma Startup SARL'}
                        required
                      />
                    </div>
                  </div>

                  {/* Pays */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">Pays *</label>
                    <div className="relative">
                      <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <select
                        name="country"
                        value={formData.country}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        required
                      >
                        <option value="">Sélectionnez un pays</option>
                        {countries.map(country => (
                          <option key={country} value={country}>{country}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Email */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">Email professionnel *</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="dev@example.com"
                        required
                      />
                    </div>
                  </div>

                  {/* Téléphone */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">Numéro de téléphone *</label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="+257 79 123 456"
                        required
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Step 2: Sécurité */}
              {currentStep === 2 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">SÉCURITÉ DU COMPTE</h2>
                  
                  {/* Mot de passe */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">Mot de passe *</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-12 py-3 focus:border-primary focus:outline-none"
                        placeholder="Minimum 8 caractères"
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                      >
                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      Utilisez au moins 8 caractères avec majuscules, minuscules, chiffres et symboles
                    </p>
                  </div>

                  {/* Confirmation mot de passe */}
                  <div>
                    <label className="block text-sm font-semibold mb-2">Confirmer le mot de passe *</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="password"
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="Retapez votre mot de passe"
                        required
                      />
                    </div>
                  </div>

                  {/* 2FA */}
                  <div className="border border-gray-800 rounded-lg p-6">
                    <div className="flex items-start gap-3 mb-4">
                      <input
                        type="checkbox"
                        name="enable2FA"
                        checked={formData.enable2FA}
                        onChange={handleInputChange}
                        className="mt-1"
                        id="enable2FA"
                      />
                      <div className="flex-1">
                        <label htmlFor="enable2FA" className="font-semibold cursor-pointer">
                          Activer l'authentification à deux facteurs (2FA)
                        </label>
                        <p className="text-sm text-gray-400 mt-1">
                          Recommandé pour une sécurité maximale
                        </p>
                      </div>
                    </div>

                    {formData.enable2FA && (
                      <div className="mt-4 space-y-3">
                        <label className="block text-sm font-semibold mb-2">Méthode 2FA</label>
                        <div className="space-y-2">
                          {[
                            { value: 'sms', label: 'SMS', icon: Phone },
                            { value: 'email', label: 'Email', icon: Mail },
                            { value: 'app', label: 'Application (Google Authenticator)', icon: Smartphone }
                          ].map(method => (
                            <label key={method.value} className="flex items-center gap-3 p-3 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                              <input
                                type="radio"
                                name="twoFAMethod"
                                value={method.value}
                                checked={formData.twoFAMethod === method.value}
                                onChange={handleInputChange}
                              />
                              <method.icon className="w-5 h-5 text-gray-400" />
                              <span>{method.label}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Info sécurité */}
                  <div className="bg-primary/10 border border-primary/30 rounded-lg p-4 flex gap-3">
                    <AlertCircle className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                    <div className="text-sm">
                      <p className="font-semibold text-primary mb-1">Codes de récupération</p>
                      <p className="text-gray-300">
                        Après validation, vous recevrez des codes de récupération. Conservez-les en lieu sûr.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 3: Vérification KYC */}
              {currentStep === 3 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">VÉRIFICATION D'IDENTITÉ (KYC)</h2>
                  
                  {accountType === 'individual' ? (
                    <>
                      {/* Type de pièce d'identité */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Type de pièce d'identité *</label>
                        <select
                          name="idType"
                          value={formData.idType}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          required
                        >
                          <option value="passport">Passeport</option>
                          <option value="id_card">Carte d'identité nationale</option>
                          <option value="driver_license">Permis de conduire</option>
                        </select>
                      </div>

                      {/* Numéro de pièce */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Numéro de pièce d'identité *</label>
                        <input
                          type="text"
                          name="idNumber"
                          value={formData.idNumber}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          placeholder="Ex: AB123456"
                          required
                        />
                      </div>

                      {/* Upload pièce d'identité */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Pièce d'identité (recto-verso) *</label>
                        <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-primary/50 transition-colors">
                          <Upload className="w-12 h-12 text-gray-500 mx-auto mb-3" />
                          <input
                            type="file"
                            onChange={(e) => handleFileChange(e, 'idFile')}
                            accept="image/*,.pdf"
                            className="hidden"
                            id="idFile"
                            required
                          />
                          <label htmlFor="idFile" className="cursor-pointer">
                            <span className="text-primary font-semibold">Cliquez pour uploader</span>
                            <span className="text-gray-400"> ou glissez-déposez</span>
                            <p className="text-xs text-gray-500 mt-2">PNG, JPG ou PDF (max. 5MB)</p>
                          </label>
                          {formData.idFile && (
                            <p className="text-sm text-secondary mt-3">✓ {formData.idFile.name}</p>
                          )}
                        </div>
                      </div>

                      {/* Selfie */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Photo selfie avec pièce d'identité *</label>
                        <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-primary/50 transition-colors">
                          <Upload className="w-12 h-12 text-gray-500 mx-auto mb-3" />
                          <input
                            type="file"
                            onChange={(e) => handleFileChange(e, 'selfieFile')}
                            accept="image/*"
                            className="hidden"
                            id="selfieFile"
                            required
                          />
                          <label htmlFor="selfieFile" className="cursor-pointer">
                            <span className="text-primary font-semibold">Cliquez pour uploader</span>
                            <p className="text-xs text-gray-500 mt-2">Photo claire de vous tenant votre pièce d'identité</p>
                          </label>
                          {formData.selfieFile && (
                            <p className="text-sm text-secondary mt-3">✓ {formData.selfieFile.name}</p>
                          )}
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      {/* Entreprise */}
                      <div>
                        <label className="block text-sm font-semibold mb-2">Nom de l'entreprise *</label>
                        <input
                          type="text"
                          name="companyName"
                          value={formData.companyName}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          placeholder="Ma Startup SARL"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-semibold mb-2">Numéro de registre de commerce *</label>
                        <input
                          type="text"
                          name="registrationNumber"
                          value={formData.registrationNumber}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          placeholder="RC-123456"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-semibold mb-2">NIF (Numéro d'Identification Fiscale) *</label>
                        <input
                          type="text"
                          name="nif"
                          value={formData.nif}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          placeholder="4000123456"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-semibold mb-2">Adresse légale *</label>
                        <textarea
                          name="legalAddress"
                          value={formData.legalAddress}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          rows="3"
                          placeholder="Adresse complète du siège social"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-semibold mb-2">Nom du représentant légal *</label>
                        <input
                          type="text"
                          name="legalRepName"
                          value={formData.legalRepName}
                          onChange={handleInputChange}
                          className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                          placeholder="Nom complet du gérant"
                          required
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-semibold mb-2">Pièce d'identité du représentant légal *</label>
                        <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-primary/50 transition-colors">
                          <Upload className="w-12 h-12 text-gray-500 mx-auto mb-3" />
                          <input
                            type="file"
                            onChange={(e) => handleFileChange(e, 'legalRepIdFile')}
                            accept="image/*,.pdf"
                            className="hidden"
                            id="legalRepIdFile"
                            required
                          />
                          <label htmlFor="legalRepIdFile" className="cursor-pointer">
                            <span className="text-primary font-semibold">Cliquez pour uploader</span>
                            <p className="text-xs text-gray-500 mt-2">Pièce d'identité + signature</p>
                          </label>
                          {formData.legalRepIdFile && (
                            <p className="text-sm text-secondary mt-3">✓ {formData.legalRepIdFile.name}</p>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}

              {/* Step 4: Informations techniques */}
              {currentStep === 4 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">INFORMATIONS TECHNIQUES</h2>
                  
                  <div>
                    <label className="block text-sm font-semibold mb-2">Nom de l'application *</label>
                    <div className="relative">
                      <Code className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="text"
                        name="appName"
                        value={formData.appName}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="Mon Application"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Description de l'application *</label>
                    <textarea
                      name="appDescription"
                      value={formData.appDescription}
                      onChange={handleInputChange}
                      className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                      rows="4"
                      placeholder="Décrivez votre application et son utilisation de l'API uFaranga..."
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">URL du site web</label>
                    <div className="relative">
                      <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="url"
                        name="websiteUrl"
                        value={formData.websiteUrl}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="https://monapp.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">URL de callback *</label>
                    <div className="relative">
                      <ArrowRight className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="url"
                        name="callbackUrl"
                        value={formData.callbackUrl}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="https://monapp.com/callback"
                        required
                      />
                    </div>
                    <p className="text-xs text-gray-500 mt-1">URL de retour après paiement</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">URL de webhook *</label>
                    <div className="relative">
                      <Webhook className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                      <input
                        type="url"
                        name="webhookUrl"
                        value={formData.webhookUrl}
                        onChange={handleInputChange}
                        className="w-full bg-black border border-gray-700 rounded-lg pl-11 pr-4 py-3 focus:border-primary focus:outline-none"
                        placeholder="https://monapp.com/webhooks/ufaranga"
                        required
                      />
                    </div>
                    <p className="text-xs text-gray-500 mt-1">URL pour recevoir les notifications en temps réel</p>
                  </div>

                  {/* Plateformes */}
                  <div>
                    <label className="block text-sm font-semibold mb-3">Plateformes cibles *</label>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {platforms.map(platform => (
                        <button
                          key={platform}
                          type="button"
                          onClick={() => handlePlatformToggle(platform)}
                          className={`p-4 rounded-lg border-2 transition-all ${
                            formData.platform.includes(platform)
                              ? 'border-primary bg-primary/10'
                              : 'border-gray-800 hover:border-gray-700'
                          }`}
                        >
                          <Smartphone className="w-6 h-6 mx-auto mb-2 text-primary" />
                          <div className="text-sm font-semibold">{platform}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Environnement */}
                  <div>
                    <label className="block text-sm font-semibold mb-3">Environnement initial</label>
                    <div className="grid md:grid-cols-2 gap-4">
                      <label className="flex items-center gap-3 p-4 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                        <input
                          type="radio"
                          name="environment"
                          value="sandbox"
                          checked={formData.environment === 'sandbox'}
                          onChange={handleInputChange}
                        />
                        <Server className="w-5 h-5 text-secondary" />
                        <div>
                          <div className="font-semibold">Sandbox (Test)</div>
                          <div className="text-xs text-gray-400">Argent fictif, tests illimités</div>
                        </div>
                      </label>
                      <label className="flex items-center gap-3 p-4 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                        <input
                          type="radio"
                          name="environment"
                          value="production"
                          checked={formData.environment === 'production'}
                          onChange={handleInputChange}
                        />
                        <Server className="w-5 h-5 text-primary" />
                        <div>
                          <div className="font-semibold">Production</div>
                          <div className="text-xs text-gray-400">Transactions réelles</div>
                        </div>
                      </label>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 5: Configuration paiement */}
              {currentStep === 5 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">CONFIGURATION PAIEMENT</h2>
                  
                  <div>
                    <label className="block text-sm font-semibold mb-2">Devise principale *</label>
                    <select
                      name="currency"
                      value={formData.currency}
                      onChange={handleInputChange}
                      className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                      required
                    >
                      <option value="BIF">BIF - Franc Burundais</option>
                      <option value="USD">USD - Dollar Américain</option>
                      <option value="EUR">EUR - Euro</option>
                      <option value="RWF">RWF - Franc Rwandais</option>
                    </select>
                  </div>

                  {/* Moyens de paiement */}
                  <div>
                    <label className="block text-sm font-semibold mb-3">Moyens de paiement acceptés *</label>
                    <div className="space-y-3">
                      {paymentMethods.map(method => (
                        <label
                          key={method}
                          className={`flex items-center gap-3 p-4 border-2 rounded-lg cursor-pointer transition-all ${
                            formData.paymentMethods.includes(method)
                              ? 'border-primary bg-primary/10'
                              : 'border-gray-800 hover:border-gray-700'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={formData.paymentMethods.includes(method)}
                            onChange={() => handlePaymentMethodToggle(method)}
                          />
                          <CreditCard className="w-5 h-5 text-primary" />
                          <span className="font-semibold">{method}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Limite de transaction (BIF) *</label>
                    <select
                      name="transactionLimit"
                      value={formData.transactionLimit}
                      onChange={handleInputChange}
                      className="w-full bg-black border border-gray-700 rounded-lg px-4 py-3 focus:border-primary focus:outline-none"
                      required
                    >
                      <option value="1000000">1,000,000 BIF / transaction</option>
                      <option value="5000000">5,000,000 BIF / transaction</option>
                      <option value="10000000">10,000,000 BIF / transaction</option>
                      <option value="unlimited">Illimité (nécessite validation)</option>
                    </select>
                  </div>

                  {/* Mode test */}
                  <div className="border border-secondary/30 rounded-lg p-6 bg-gradient-to-br from-secondary/5 to-black">
                    <div className="flex items-start gap-3 mb-4">
                      <Settings className="w-6 h-6 text-secondary shrink-0" />
                      <div>
                        <h3 className="font-bold mb-2">Mode Test (Sandbox)</h3>
                        <p className="text-sm text-gray-400 mb-4">
                          Vous aurez accès à un environnement de test complet avec :
                        </p>
                        <ul className="space-y-2 text-sm text-gray-300">
                          <li className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-secondary" />
                            Comptes virtuels de test
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-secondary" />
                            Transactions simulées (argent fictif)
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-secondary" />
                            Webhooks de test
                          </li>
                          <li className="flex items-center gap-2">
                            <CheckCircle className="w-4 h-4 text-secondary" />
                            Clés API séparées de la production
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Step 6: Validation */}
              {currentStep === 6 && (
                <div className="space-y-6">
                  <h2 className="text-2xl font-anton uppercase mb-6">VALIDATION ET CONFORMITÉ</h2>
                  
                  {/* Résumé */}
                  <div className="border border-gray-800 rounded-lg p-6 bg-gray-900/30">
                    <h3 className="font-bold mb-4">Résumé de votre inscription</h3>
                    <div className="space-y-3 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Type de compte:</span>
                        <span className="font-semibold">{accountType === 'individual' ? 'Individuel' : 'Entreprise'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Nom:</span>
                        <span className="font-semibold">{formData.fullName || '-'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Email:</span>
                        <span className="font-semibold">{formData.email || '-'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Application:</span>
                        <span className="font-semibold">{formData.appName || '-'}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Environnement:</span>
                        <span className="font-semibold">{formData.environment === 'sandbox' ? 'Sandbox (Test)' : 'Production'}</span>
                      </div>
                    </div>
                  </div>

                  {/* Acceptation des conditions */}
                  <div className="space-y-4">
                    <label className="flex items-start gap-3 p-4 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                      <input
                        type="checkbox"
                        name="acceptTerms"
                        checked={formData.acceptTerms}
                        onChange={handleInputChange}
                        required
                        className="mt-1"
                      />
                      <div className="text-sm">
                        <span className="font-semibold">J'accepte les </span>
                        <a href="/legal" className="text-primary hover:underline">Conditions Générales d'Utilisation</a>
                        <span className="font-semibold"> de l'API uFaranga *</span>
                      </div>
                    </label>

                    <label className="flex items-start gap-3 p-4 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                      <input
                        type="checkbox"
                        name="acceptPrivacy"
                        checked={formData.acceptPrivacy}
                        onChange={handleInputChange}
                        required
                        className="mt-1"
                      />
                      <div className="text-sm">
                        <span className="font-semibold">J'accepte la </span>
                        <a href="/legal" className="text-primary hover:underline">Politique de Confidentialité</a>
                        <span className="font-semibold"> *</span>
                      </div>
                    </label>

                    <label className="flex items-start gap-3 p-4 border border-gray-800 rounded-lg cursor-pointer hover:border-gray-700">
                      <input
                        type="checkbox"
                        name="acceptCompliance"
                        checked={formData.acceptCompliance}
                        onChange={handleInputChange}
                        required
                        className="mt-1"
                      />
                      <div className="text-sm">
                        <span className="font-semibold">Je m'engage à respecter les normes AML/KYC et RGPD *</span>
                        <p className="text-gray-400 mt-1">
                          Je comprends que mes transactions seront auditées et que je dois respecter les réglementations en vigueur.
                        </p>
                      </div>
                    </label>
                  </div>

                  {/* Info après validation */}
                  <div className="space-y-4">
                    <div className="bg-primary/10 border border-primary/30 rounded-lg p-4">
                      <div className="flex gap-3">
                        <Key className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                        <div className="text-sm">
                          <p className="font-semibold text-primary mb-1">Clés API</p>
                          <p className="text-gray-300">
                            Après validation de votre compte (24-48h), vous recevrez vos clés API par email :
                          </p>
                          <ul className="mt-2 space-y-1 text-gray-400">
                            <li>• API Key (publique) - pour les requêtes client</li>
                            <li>• Secret Key (privée) - à garder confidentielle</li>
                            <li>• Webhook Secret - pour vérifier les signatures</li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <div className="bg-secondary/10 border border-secondary/30 rounded-lg p-4">
                      <div className="flex gap-3">
                        <FileCheck className="w-5 h-5 text-secondary shrink-0 mt-0.5" />
                        <div className="text-sm">
                          <p className="font-semibold text-secondary mb-1">Logs & Audit</p>
                          <p className="text-gray-300">
                            Toutes vos transactions API seront enregistrées et disponibles dans votre tableau de bord développeur pour audit et conformité.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Navigation buttons */}
            <div className="flex justify-between items-center mt-8">
              <button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 1}
                className={`px-6 py-3 rounded-lg font-semibold transition-colors inline-flex items-center gap-2 ${
                  currentStep === 1
                    ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                    : 'border border-gray-700 hover:border-primary/50'
                }`}
              >
                <ArrowLeft className="w-5 h-5" />
                Précédent
              </button>

              {currentStep < totalSteps ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="bg-white text-black px-8 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors inline-flex items-center gap-2"
                >
                  Suivant
                  <ArrowRight className="w-5 h-5" />
                </button>
              ) : (
                <button
                  type="submit"
                  className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
                >
                  <CheckCircle className="w-5 h-5" />
                  Créer mon compte
                </button>
              )}
            </div>
          </form>

          {/* Help text */}
          <div className="text-center mt-8 text-sm text-gray-400">
            <p>Besoin d'aide ? <a href="/support" className="text-primary hover:underline">Contactez notre support développeur</a></p>
            <p className="mt-2">Déjà un compte ? <a href="/login" className="text-primary hover:underline">Se connecter</a></p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeveloperSignup;
