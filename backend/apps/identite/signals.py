"""
Signals pour la création automatique de profils et audit
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur, ProfilUtilisateur


@receiver(post_save, sender=Utilisateur)
def creer_profil_utilisateur(sender, instance, created, **kwargs):
    """Créer automatiquement un profil lors de la création d'un utilisateur"""
    if created:
        ProfilUtilisateur.objects.create(utilisateur=instance)


@receiver(post_save, sender=Utilisateur)
def sauvegarder_profil_utilisateur(sender, instance, **kwargs):
    """Sauvegarder le profil lors de la mise à jour de l'utilisateur"""
    if hasattr(instance, 'profil'):
        instance.profil.save()
