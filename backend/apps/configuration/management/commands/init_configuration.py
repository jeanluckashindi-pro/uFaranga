"""
Commande pour initialiser la configuration système
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from apps.configuration.models import (
    ParametreSysteme,
    LimiteTransaction,
    TauxChange
)


class Command(BaseCommand):
    help = 'Initialise la configuration système avec les valeurs par défaut'
    
    def handle(self, *args, **options):
        self.stdout.write('Initialisation de la configuration système...')
        
        # Paramètres système
        self.init_parametres_systeme()
        
        # Limites de transaction
        self.init_limites_transactions()
        
        # Taux de change
        self.init_taux_change()
        
        self.stdout.write(self.style.SUCCESS('Configuration initialisée avec succès!'))
    
    def init_parametres_systeme(self):
        """Initialise les paramètres système"""
        parametres = [
            {
                'cle': 'DEVISE_PRINCIPALE',
                'valeur': 'BIF',
                'type_valeur': 'STRING',
                'description': 'Devise principale du système',
                'categorie': 'GENERAL'
            },
            {
                'cle': 'FRAIS_TRANSACTION_P2P_POURCENTAGE',
                'valeur': '1.0',
                'type_valeur': 'DECIMAL',
                'description': 'Pourcentage de frais pour les transactions P2P',
                'categorie': 'FRAIS'
            },
            {
                'cle': 'FRAIS_TRANSACTION_P2P_MIN',
                'valeur': '100',
                'type_valeur': 'DECIMAL',
                'description': 'Frais minimum pour les transactions P2P (BIF)',
                'categorie': 'FRAIS'
            },
            {
                'cle': 'FRAIS_TRANSACTION_P2P_MAX',
                'valeur': '5000',
                'type_valeur': 'DECIMAL',
                'description': 'Frais maximum pour les transactions P2P (BIF)',
                'categorie': 'FRAIS'
            },
            {
                'cle': 'SYNC_BANCAIRE_FREQUENCE_MINUTES',
                'valeur': '5',
                'type_valeur': 'INTEGER',
                'description': 'Fréquence de synchronisation avec les banques (minutes)',
                'categorie': 'BANCAIRE'
            },
            {
                'cle': 'SCORE_FRAUDE_SEUIL_ALERTE',
                'valeur': '70',
                'type_valeur': 'INTEGER',
                'description': 'Seuil de score de fraude pour déclencher une alerte',
                'categorie': 'SECURITE'
            },
            {
                'cle': 'SCORE_FRAUDE_SEUIL_BLOCAGE',
                'valeur': '90',
                'type_valeur': 'INTEGER',
                'description': 'Seuil de score de fraude pour bloquer automatiquement',
                'categorie': 'SECURITE'
            },
        ]
        
        for param in parametres:
            ParametreSysteme.objects.get_or_create(
                cle=param['cle'],
                defaults=param
            )
        
        self.stdout.write(f'  ✓ {len(parametres)} paramètres système créés')
    
    def init_limites_transactions(self):
        """Initialise les limites de transaction par niveau KYC"""
        limites = [
            # Niveau KYC 0 - Non vérifié (très limité)
            {
                'niveau_kyc': 0,
                'type_utilisateur': 'CLIENT',
                'type_transaction': 'P2P',
                'montant_min': Decimal('100'),
                'montant_max_unitaire': Decimal('10000'),
                'montant_max_quotidien': Decimal('20000'),
                'montant_max_mensuel': Decimal('100000'),
                'nombre_max_quotidien': 5,
            },
            # Niveau KYC 1 - Basique (CNI)
            {
                'niveau_kyc': 1,
                'type_utilisateur': 'CLIENT',
                'type_transaction': 'P2P',
                'montant_min': Decimal('100'),
                'montant_max_unitaire': Decimal('50000'),
                'montant_max_quotidien': Decimal('200000'),
                'montant_max_mensuel': Decimal('2000000'),
                'nombre_max_quotidien': 20,
            },
            # Niveau KYC 2 - Complet (CNI + Justificatifs)
            {
                'niveau_kyc': 2,
                'type_utilisateur': 'CLIENT',
                'type_transaction': 'P2P',
                'montant_min': Decimal('100'),
                'montant_max_unitaire': Decimal('500000'),
                'montant_max_quotidien': Decimal('2000000'),
                'montant_max_mensuel': Decimal('20000000'),
                'nombre_max_quotidien': 50,
            },
            # Niveau KYC 3 - Premium (Tout validé)
            {
                'niveau_kyc': 3,
                'type_utilisateur': 'CLIENT',
                'type_transaction': 'P2P',
                'montant_min': Decimal('100'),
                'montant_max_unitaire': Decimal('5000000'),
                'montant_max_quotidien': Decimal('10000000'),
                'montant_max_mensuel': Decimal('100000000'),
                'nombre_max_quotidien': 100,
            },
            # Agents - Limites plus élevées
            {
                'niveau_kyc': 2,
                'type_utilisateur': 'AGENT',
                'type_transaction': 'DEPOT',
                'montant_min': Decimal('1000'),
                'montant_max_unitaire': Decimal('1000000'),
                'montant_max_quotidien': Decimal('10000000'),
                'montant_max_mensuel': Decimal('100000000'),
            },
            {
                'niveau_kyc': 2,
                'type_utilisateur': 'AGENT',
                'type_transaction': 'RETRAIT',
                'montant_min': Decimal('1000'),
                'montant_max_unitaire': Decimal('1000000'),
                'montant_max_quotidien': Decimal('10000000'),
                'montant_max_mensuel': Decimal('100000000'),
            },
        ]
        
        for limite in limites:
            LimiteTransaction.objects.get_or_create(
                niveau_kyc=limite['niveau_kyc'],
                type_utilisateur=limite['type_utilisateur'],
                type_transaction=limite['type_transaction'],
                date_debut_validite=timezone.now().date(),
                defaults=limite
            )
        
        self.stdout.write(f'  ✓ {len(limites)} limites de transaction créées')
    
    def init_taux_change(self):
        """Initialise les taux de change"""
        taux = [
            {
                'devise_source': 'BIF',
                'devise_cible': 'USD',
                'taux': Decimal('0.00035'),  # 1 BIF = 0.00035 USD (exemple)
                'source': 'Banque Centrale du Burundi'
            },
            {
                'devise_source': 'USD',
                'devise_cible': 'BIF',
                'taux': Decimal('2857.14'),  # 1 USD = 2857.14 BIF (exemple)
                'source': 'Banque Centrale du Burundi'
            },
            {
                'devise_source': 'BIF',
                'devise_cible': 'EUR',
                'taux': Decimal('0.00032'),  # 1 BIF = 0.00032 EUR (exemple)
                'source': 'Banque Centrale du Burundi'
            },
            {
                'devise_source': 'EUR',
                'devise_cible': 'BIF',
                'taux': Decimal('3125.00'),  # 1 EUR = 3125 BIF (exemple)
                'source': 'Banque Centrale du Burundi'
            },
        ]
        
        for t in taux:
            TauxChange.objects.get_or_create(
                devise_source=t['devise_source'],
                devise_cible=t['devise_cible'],
                date_debut_validite=timezone.now(),
                defaults=t
            )
        
        self.stdout.write(f'  ✓ {len(taux)} taux de change créés')
