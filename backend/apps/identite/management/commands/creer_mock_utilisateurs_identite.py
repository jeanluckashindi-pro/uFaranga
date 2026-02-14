"""
Commande pour insérer des utilisateurs mock dans identite.utilisateurs
avec les différents profils : CLIENT, AGENT, MARCHAND, ADMIN, SUPER_ADMIN, SYSTEME
"""
from datetime import date
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.identite.models import Utilisateur, ProfilUtilisateur


MOT_DE_PASSE_DEMO = "DemoPass123!"

# Mock data : un utilisateur par type de profil
UTILISATEURS_MOCK = [
    {
        "courriel": "super.admin@ufaranga.bi",
        "numero_telephone": "+25779000001",
        "prenom": "Super",
        "nom_famille": "Admin",
        "date_naissance": date(1985, 5, 10),
        "lieu_naissance": "Bujumbura",
        "nationalite": "BI",
        "pays_residence": "BI",
        "province": "Bujumbura Mairie",
        "ville": "Bujumbura",
        "commune": "Muha",
        "quartier": "Centre-ville",
        "avenue": "Avenue de l'Indépendance",
        "numero_maison": "1",
        "adresse_complete": "Avenue de l'Indépendance, Bujumbura",
        "code_postal": "0000",
        "telephone_verifie": True,
        "courriel_verifie": True,
        "niveau_kyc": 3,
        "type_utilisateur": "SUPER_ADMIN",
        "statut": "ACTIF",
        "raison_statut": "",
        "is_staff": True,
        "is_superuser": True,
        "label": "Super Admin",
    },
    {
        "courriel": "admin@ufaranga.bi",
        "numero_telephone": "+25779000002",
        "prenom": "Jean",
        "nom_famille": "Administrateur",
        "date_naissance": date(1990, 3, 15),
        "lieu_naissance": "Gitega",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "Gitega",
        "province": "Gitega",
        "commune": "Gitega",
        "quartier": "Centre",
        "telephone_verifie": True,
        "courriel_verifie": True,
        "niveau_kyc": 2,
        "type_utilisateur": "ADMIN",
        "statut": "ACTIF",
        "is_staff": True,
        "is_superuser": False,
        "label": "Administrateur",
    },
    {
        "courriel": "agent1@ufaranga.bi",
        "numero_telephone": "+25779000003",
        "prenom": "Marie",
        "nom_famille": "Agent",
        "date_naissance": date(1992, 7, 22),
        "lieu_naissance": "Bujumbura",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "Bujumbura",
        "province": "Bujumbura Mairie",
        "commune": "Mukaza",
        "quartier": "Rohero",
        "avenue": "Avenue du Commerce",
        "numero_maison": "45",
        "telephone_verifie": True,
        "courriel_verifie": True,
        "niveau_kyc": 2,
        "type_utilisateur": "AGENT",
        "statut": "ACTIF",
        "label": "Agent 1",
    },
    {
        "courriel": "marchand1@ufaranga.bi",
        "numero_telephone": "+25779000004",
        "prenom": "Pierre",
        "nom_famille": "Marchand",
        "date_naissance": date(1988, 11, 5),
        "lieu_naissance": "Ngozi",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "Ngozi",
        "province": "Ngozi",
        "commune": "Ngozi",
        "quartier": "Marché central",
        "telephone_verifie": True,
        "courriel_verifie": True,
        "niveau_kyc": 2,
        "type_utilisateur": "MARCHAND",
        "statut": "ACTIF",
        "label": "Marchand 1",
    },
    {
        "courriel": "client1@example.com",
        "numero_telephone": "+25779111111",
        "prenom": "Alice",
        "nom_famille": "Client",
        "date_naissance": date(1995, 1, 20),
        "lieu_naissance": "Bujumbura",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "Bujumbura",
        "province": "Bujumbura Mairie",
        "commune": "Ntahangwa",
        "quartier": "Kamenge",
        "avenue": "Avenue de la Liberté",
        "numero_maison": "12",
        "adresse_complete": "Kamenge, Bujumbura",
        "telephone_verifie": True,
        "courriel_verifie": True,
        "niveau_kyc": 1,
        "type_utilisateur": "CLIENT",
        "statut": "ACTIF",
        "label": "Client 1",
    },
    {
        "courriel": "client2@example.com",
        "numero_telephone": "+25779222222",
        "prenom": "Bernard",
        "nom_famille": "Client",
        "date_naissance": date(1998, 8, 12),
        "lieu_naissance": "Muyinga",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "Muyinga",
        "province": "Muyinga",
        "commune": "Muyinga",
        "quartier": "Centre",
        "telephone_verifie": False,
        "courriel_verifie": False,
        "niveau_kyc": 0,
        "type_utilisateur": "CLIENT",
        "statut": "EN_VERIFICATION",
        "label": "Client 2",
    },
    {
        "courriel": "systeme@ufaranga.bi",
        "numero_telephone": "+25779000000",
        "prenom": "Compte",
        "nom_famille": "Système",
        "date_naissance": date(2020, 1, 1),
        "lieu_naissance": "",
        "nationalite": "BI",
        "pays_residence": "BI",
        "ville": "",
        "type_utilisateur": "SYSTEME",
        "statut": "ACTIF",
        "niveau_kyc": 3,
        "is_staff": True,
        "is_superuser": True,
        "label": "Système",
    },
]


class Command(BaseCommand):
    help = "Insère des utilisateurs mock dans identite.utilisateurs (tous les profils)."

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
            help="Ne pas écraser les utilisateurs existants (par courriel).",
        )

    def handle(self, *args, **options):
        password = options["password"]
        skip_existing = options["skip_existing"]

        for item in UTILISATEURS_MOCK:
            item = item.copy()
            label = item.pop("label")
            courriel = item["courriel"]

            if skip_existing and Utilisateur.objects.filter(courriel=courriel).exists():
                self.stdout.write(
                    self.style.WARNING(f"Déjà existant, ignoré : {label} ({courriel})")
                )
                continue

            try:
                # update_or_create : met à jour si le courriel existe déjà (évite duplicate key)
                user, created = Utilisateur.objects.update_or_create(
                    courriel=courriel,
                    defaults={
                        "numero_telephone": item["numero_telephone"],
                        "prenom": item.get("prenom", ""),
                        "nom_famille": item.get("nom_famille", ""),
                        "date_naissance": item["date_naissance"],
                        "lieu_naissance": item.get("lieu_naissance", ""),
                        "nationalite": item.get("nationalite", "BI"),
                        "pays_residence": item.get("pays_residence", "BI"),
                        "ville": item.get("ville", ""),
                        "province": item.get("province", ""),
                        "commune": item.get("commune", ""),
                        "quartier": item.get("quartier", ""),
                        "avenue": item.get("avenue", ""),
                        "numero_maison": item.get("numero_maison", ""),
                        "adresse_complete": item.get("adresse_complete", ""),
                        "code_postal": item.get("code_postal", ""),
                        "telephone_verifie": item.get("telephone_verifie", False),
                        "courriel_verifie": item.get("courriel_verifie", False),
                        "niveau_kyc": item.get("niveau_kyc", 0),
                        "type_utilisateur": item.get("type_utilisateur", "CLIENT"),
                        "statut": item.get("statut", "ACTIF"),
                        "raison_statut": item.get("raison_statut", ""),
                        "is_staff": item.get("is_staff", False),
                        "is_superuser": item.get("is_superuser", False),
                        "est_actif": True,
                    },
                )
                user.set_password(password)
                user.save(update_fields=["password"])
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Erreur pour {label} ({courriel}) : {e}")
                )
                continue

            ProfilUtilisateur.objects.get_or_create(
                utilisateur=user,
                defaults={
                    "langue": "fr",
                    "devise_preferee": "BIF",
                    "fuseau_horaire": "Africa/Bujumbura",
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Créé : {label} — {courriel}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Mis à jour : {label} — {courriel}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTerminé. Tous les utilisateurs ont le mot de passe : {password}"
            )
        )
        self.stdout.write("Profils : SUPER_ADMIN, ADMIN, AGENT, MARCHAND, CLIENT (x2), SYSTEME")
