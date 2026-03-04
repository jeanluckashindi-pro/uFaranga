"""
Signals pour gérer automatiquement la localisation des utilisateurs.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Utilisateur
from apps.localisation.services import LocalisationService
import logging

logger = logging.getLogger('apps')


@receiver(pre_save, sender=Utilisateur)
def associer_pays_avant_sauvegarde(sender, instance, **kwargs):
    """
    Associe automatiquement le pays à l'utilisateur avant la sauvegarde.
    """
    # Si le pays n'est pas défini mais qu'on a un code ISO
    if not instance.pays and instance.nationalite:
        from apps.localisation.models import Pays
        try:
            pays = Pays.objects.get(code_iso_2=instance.nationalite)
            instance.pays = pays
            logger.info(f"Pays {pays.nom} associé automatiquement à {instance.courriel}")
        except Pays.DoesNotExist:
            logger.warning(f"Pays avec code {instance.nationalite} introuvable pour {instance.courriel}")


@receiver(post_save, sender=Utilisateur)
def verifier_localisation_apres_sauvegarde(sender, instance, created, **kwargs):
    """
    Vérifie la localisation et les restrictions après la sauvegarde de l'utilisateur.
    """
    if created:
        # Nouvel utilisateur créé
        logger.info(f"Nouvel utilisateur créé : {instance.courriel}")
        
        # Vérifier les restrictions géographiques
        restrictions = LocalisationService.obtenir_restrictions_actives(instance)
        if restrictions.exists():
            logger.warning(
                f"Utilisateur {instance.courriel} dans une zone avec {restrictions.count()} restriction(s) active(s)"
            )
        
        # Vérifier les zones à risque
        zones_risque = LocalisationService.obtenir_zones_risque(instance)
        if zones_risque.exists():
            zone_max = zones_risque.first()
            logger.warning(
                f"Utilisateur {instance.courriel} dans une zone à risque {zone_max.niveau_risque} "
                f"(score: {zone_max.score_risque})"
            )
            
            # Si zone critique, on pourrait bloquer l'utilisateur
            if zone_max.niveau_risque == 'CRITIQUE':
                logger.error(
                    f"ALERTE: Utilisateur {instance.courriel} dans une zone à risque CRITIQUE ! "
                    f"Type: {zone_max.type_risque}"
                )
                # On pourrait automatiquement désactiver le compte
                # instance.est_actif = False
                # instance.save(update_fields=['est_actif'])
