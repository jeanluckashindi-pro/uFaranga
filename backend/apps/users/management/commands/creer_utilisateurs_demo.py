"""
Commande pour créer des utilisateurs de démonstration avec différents profils :
- Admin système (superuser)
- Admin technique (staff)
- Clients (2)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile

User = get_user_model()

# Mot de passe commun pour la démo (à changer en production)
MOT_DE_PASSE_DEMO = "DemoPass123!"


UTILISATEURS_DEMO = [
    {
        "email": "admin.systeme@ufaranga.bi",
        "username": "admin_systeme",
        "first_name": "Admin",
        "last_name": "Système",
        "phone_number": "+25779000001",
        "country": "BI",
        "city": "Bujumbura",
        "is_staff": True,
        "is_superuser": True,
        "is_email_verified": True,
        "is_phone_verified": True,
        "kyc_level": 2,
        "label": "Admin système",
    },
    {
        "email": "admin.technique@ufaranga.bi",
        "username": "admin_technique",
        "first_name": "Admin",
        "last_name": "Technique",
        "phone_number": "+25779000002",
        "country": "BI",
        "city": "Bujumbura",
        "is_staff": True,
        "is_superuser": False,
        "is_email_verified": True,
        "is_phone_verified": True,
        "kyc_level": 2,
        "label": "Admin technique",
    },
    {
        "email": "client1@example.com",
        "username": "client1",
        "first_name": "Jean",
        "last_name": "Client",
        "phone_number": "+25779111111",
        "country": "BI",
        "city": "Bujumbura",
        "is_staff": False,
        "is_superuser": False,
        "is_email_verified": True,
        "is_phone_verified": True,
        "kyc_level": 1,
        "label": "Client 1",
    },
    {
        "email": "client2@example.com",
        "username": "client2",
        "first_name": "Marie",
        "last_name": "Client",
        "phone_number": "+25779222222",
        "country": "BI",
        "city": "Gitega",
        "is_staff": False,
        "is_superuser": False,
        "is_email_verified": False,
        "is_phone_verified": False,
        "kyc_level": 0,
        "label": "Client 2",
    },
    {
        "email": "systeme@ufaranga.bi",
        "username": "systeme",
        "first_name": "Compte",
        "last_name": "Système",
        "phone_number": "+25779000000",
        "country": "BI",
        "city": "Bujumbura",
        "is_staff": True,
        "is_superuser": True,
        "is_email_verified": True,
        "is_phone_verified": True,
        "kyc_level": 2,
        "label": "Système",
    },
]


class Command(BaseCommand):
    help = "Crée des utilisateurs de démo : admin système, admin technique, 2 clients."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            type=str,
            default=MOT_DE_PASSE_DEMO,
            help="Mot de passe pour tous les utilisateurs (défaut: DemoPass123!)",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Ne pas recréer les utilisateurs qui existent déjà (par email).",
        )

    def handle(self, *args, **options):
        password = options["password"]
        skip_existing = options["skip_existing"]

        for item in UTILISATEURS_DEMO:
            item = item.copy()
            label = item.pop("label")
            email = item.pop("email")

            if skip_existing and User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f"Déjà existant, ignoré : {label} ({email})")
                )
                continue

            user, created = User.objects.update_or_create(
                email=email,
                defaults={**item},
            )
            user.set_password(password)
            user.save()

            UserProfile.objects.get_or_create(user=user)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Créé : {label} — {email}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Mis à jour : {label} — {email}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTerminé. Tous les utilisateurs ont le mot de passe : {password}"
            )
        )
        self.stdout.write(
            "Connexion : POST /api/v1/authentification/connexion/ avec email + password (ou username)"
        )
