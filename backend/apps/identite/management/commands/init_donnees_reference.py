"""
Commande pour initialiser les données de référence (types, niveaux KYC, statuts)
Usage: python manage.py init_donnees_reference
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.identite.models import TypeUtilisateur, NiveauKYC, StatutUtilisateur


class Command(BaseCommand):
    help = 'Initialise les données de référence pour le module identité'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initialisation des données de référence...'))
        
        with transaction.atomic():
            self._init_types_utilisateurs()
            self._init_niveaux_kyc()
            self._init_statuts_utilisateurs()
        
        self.stdout.write(self.style.SUCCESS('✓ Données de référence initialisées avec succès!'))

    def _init_types_utilisateurs(self):
        """Initialise les types d'utilisateurs"""
        self.stdout.write('  → Types d\'utilisateurs...')
        
        types = [
            {
                'code': 'CLIENT',
                'libelle': 'Client',
                'description': 'Client standard de la plateforme',
                'ordre_affichage': 1,
            },
            {
                'code': 'AGENT',
                'libelle': 'Agent',
                'description': 'Agent de service (dépôt, retrait, etc.)',
                'ordre_affichage': 2,
            },
            {
                'code': 'MARCHAND',
                'libelle': 'Marchand',
                'description': 'Commerçant acceptant les paiements',
                'ordre_affichage': 3,
            },
            {
                'code': 'ADMIN',
                'libelle': 'Administrateur',
                'description': 'Administrateur de la plateforme',
                'ordre_affichage': 4,
            },
            {
                'code': 'SUPER_ADMIN',
                'libelle': 'Super Administrateur',
                'description': 'Super administrateur avec tous les droits',
                'ordre_affichage': 5,
            },
            {
                'code': 'SYSTEME',
                'libelle': 'Système',
                'description': 'Compte système pour les opérations automatiques',
                'ordre_affichage': 6,
            },
        ]
        
        for type_data in types:
            TypeUtilisateur.objects.update_or_create(
                code=type_data['code'],
                defaults=type_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'    ✓ {len(types)} types créés'))

    def _init_niveaux_kyc(self):
        """Initialise les niveaux KYC"""
        self.stdout.write('  → Niveaux KYC...')
        
        niveaux = [
            {
                'niveau': 0,
                'libelle': 'Non vérifié',
                'description': 'Aucune vérification effectuée',
                'limite_transaction_journaliere': 0,
                'limite_solde_maximum': 0,
                'documents_requis': [],
            },
            {
                'niveau': 1,
                'libelle': 'Basique',
                'description': 'Vérification basique (téléphone + email)',
                'limite_transaction_journaliere': 50000,  # 50,000 BIF
                'limite_solde_maximum': 100000,  # 100,000 BIF
                'documents_requis': ['telephone', 'email'],
            },
            {
                'niveau': 2,
                'libelle': 'Complet',
                'description': 'Vérification complète (pièce d\'identité)',
                'limite_transaction_journaliere': 500000,  # 500,000 BIF
                'limite_solde_maximum': 2000000,  # 2,000,000 BIF
                'documents_requis': ['telephone', 'email', 'piece_identite', 'selfie'],
            },
            {
                'niveau': 3,
                'libelle': 'Premium',
                'description': 'Vérification premium (justificatif de domicile)',
                'limite_transaction_journaliere': 5000000,  # 5,000,000 BIF
                'limite_solde_maximum': 20000000,  # 20,000,000 BIF
                'documents_requis': [
                    'telephone', 'email', 'piece_identite', 
                    'selfie', 'justificatif_domicile'
                ],
            },
        ]
        
        for niveau_data in niveaux:
            NiveauKYC.objects.update_or_create(
                niveau=niveau_data['niveau'],
                defaults=niveau_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'    ✓ {len(niveaux)} niveaux créés'))

    def _init_statuts_utilisateurs(self):
        """Initialise les statuts utilisateurs"""
        self.stdout.write('  → Statuts utilisateurs...')
        
        statuts = [
            {
                'code': 'ACTIF',
                'libelle': 'Actif',
                'description': 'Compte actif et opérationnel',
                'couleur': '#28a745',  # Vert
                'permet_connexion': True,
                'permet_transactions': True,
                'ordre_affichage': 1,
            },
            {
                'code': 'EN_VERIFICATION',
                'libelle': 'En vérification',
                'description': 'Compte en cours de vérification KYC',
                'couleur': '#ffc107',  # Jaune
                'permet_connexion': True,
                'permet_transactions': False,
                'ordre_affichage': 2,
            },
            {
                'code': 'SUSPENDU',
                'libelle': 'Suspendu',
                'description': 'Compte temporairement suspendu',
                'couleur': '#fd7e14',  # Orange
                'permet_connexion': False,
                'permet_transactions': False,
                'ordre_affichage': 3,
            },
            {
                'code': 'BLOQUE',
                'libelle': 'Bloqué',
                'description': 'Compte bloqué pour raisons de sécurité',
                'couleur': '#dc3545',  # Rouge
                'permet_connexion': False,
                'permet_transactions': False,
                'ordre_affichage': 4,
            },
            {
                'code': 'FERME',
                'libelle': 'Fermé',
                'description': 'Compte définitivement fermé',
                'couleur': '#6c757d',  # Gris
                'permet_connexion': False,
                'permet_transactions': False,
                'ordre_affichage': 5,
            },
        ]
        
        for statut_data in statuts:
            StatutUtilisateur.objects.update_or_create(
                code=statut_data['code'],
                defaults=statut_data
            )
        
        self.stdout.write(self.style.SUCCESS(f'    ✓ {len(statuts)} statuts créés'))
