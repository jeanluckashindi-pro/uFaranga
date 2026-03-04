"""
Services pour la gestion automatique de la localisation et des vérifications géographiques.
Approche générique basée sur les divisions administratives (niveau0, niveau1, niveau2, etc.)
"""
from datetime import date
from django.db.models import Q
from .models import (
    Pays, DivisionNiveau0, DivisionNiveau1, DivisionNiveau2,
    FuseauHoraire, ZoneRisque, RestrictionGeographique, CorridorPaiement
)


class LocalisationService:
    """Service pour gérer automatiquement la localisation d'un utilisateur"""
    @staticmethod
    def associer_pays_utilisateur(utilisateur):
        """
        Associe automatiquement le pays à l'utilisateur basé sur son code ISO.
        Appelé lors de la création ou mise à jour de l'utilisateur.
        """
        # Associer le pays basé sur nationalité
        if utilisateur.nationalite and not utilisateur.pays:
            try:
                pays = Pays.objects.get(code_iso_2=utilisateur.nationalite)
                utilisateur.pays = pays
                utilisateur.save(update_fields=['pays'])
            except Pays.DoesNotExist:
                pass
        
        # Associer le pays basé sur pays_residence si différent
        if utilisateur.pays_residence and utilisateur.pays_residence != utilisateur.nationalite:
            try:
                pays_residence = Pays.objects.get(code_iso_2=utilisateur.pays_residence)
                # On peut stocker le pays de résidence dans les métadonnées
                if not utilisateur.metadonnees:
                    utilisateur.metadonnees = {}
                utilisateur.metadonnees['pays_residence_id'] = str(pays_residence.id)
                utilisateur.save(update_fields=['metadonnees'])
            except Pays.DoesNotExist:
                pass
    
    @staticmethod
    def obtenir_fuseau_horaire(utilisateur):
        """Obtient le fuseau horaire de l'utilisateur basé sur son pays"""
        if not utilisateur.pays:
            return None
        
        # Chercher dans les métadonnées du pays
        if utilisateur.pays.fuseau_horaire_id:
            try:
                return FuseauHoraire.objects.get(id=utilisateur.pays.fuseau_horaire_id)
            except FuseauHoraire.DoesNotExist:
                pass
        
        return None
    
    @staticmethod
    def obtenir_zones_risque(utilisateur):
        """
        Obtient toutes les zones à risque applicables à l'utilisateur.
        Retourne une liste de zones à risque actives.
        """
        if not utilisateur.pays:
            return []
        
        zones = ZoneRisque.objects.filter(
            pays=utilisateur.pays,
            est_actif=True
        )
        
        # Filtrer par province si disponible
        if utilisateur.province_geo:
            zones = zones.filter(
                Q(province_id=utilisateur.province_geo) | Q(province_id__isnull=True)
            )
        
        # Filtrer par district si disponible
        if utilisateur.district:
            zones = zones.filter(
                Q(district_id=utilisateur.district) | Q(district_id__isnull=True)
            )
        
        # Filtrer par quartier si disponible
        if utilisateur.quartier_geo:
            zones = zones.filter(
                Q(quartier_id=utilisateur.quartier_geo) | Q(quartier_id__isnull=True)
            )
        
        return zones.order_by('-score_risque')
    
    @staticmethod
    def obtenir_restrictions_actives(utilisateur):
        """
        Obtient toutes les restrictions géographiques actives pour l'utilisateur.
        Retourne une liste de restrictions en vigueur.
        """
        if not utilisateur.pays:
            return []
        
        aujourd_hui = date.today()
        
        restrictions = RestrictionGeographique.objects.filter(
            pays=utilisateur.pays,
            est_actif=True,
            date_debut__lte=aujourd_hui
        ).filter(
            Q(date_fin__isnull=True) | Q(date_fin__gte=aujourd_hui)
        )
        
        return restrictions.order_by('-niveau_restriction')
    
    @staticmethod
    def verifier_autorisation_transaction(utilisateur, montant=None, type_transaction='STANDARD'):
        """
        Vérifie si l'utilisateur est autorisé à effectuer une transaction.
        
        Args:
            utilisateur: Instance de Utilisateur
            montant: Montant de la transaction (optionnel)
            type_transaction: Type de transaction (STANDARD, TRANSFERT_ENTRANT, TRANSFERT_SORTANT)
        
        Returns:
            dict: {
                'autorise': bool,
                'raison': str,
                'restrictions': list,
                'zones_risque': list,
                'verification_renforcee': bool
            }
        """
        resultat = {
            'autorise': True,
            'raison': '',
            'restrictions': [],
            'zones_risque': [],
            'verification_renforcee': False,
            'limite_montant': None
        }
        
        # Vérifier si le pays est autorisé
        if utilisateur.pays and not utilisateur.pays.autorise_systeme:
            resultat['autorise'] = False
            resultat['raison'] = f"Le pays {utilisateur.pays.nom} n'est pas autorisé sur le système"
            return resultat
        
        # Vérifier les restrictions géographiques
        restrictions = LocalisationService.obtenir_restrictions_actives(utilisateur)
        resultat['restrictions'] = list(restrictions)
        
        for restriction in restrictions:
            # Vérifier selon le type de transaction
            if type_transaction == 'STANDARD' and not restriction.autorise_transactions:
                resultat['autorise'] = False
                resultat['raison'] = f"Transactions interdites : {restriction.description}"
                return resultat
            
            if type_transaction == 'TRANSFERT_ENTRANT' and not restriction.autorise_transferts_entrants:
                resultat['autorise'] = False
                resultat['raison'] = f"Transferts entrants interdits : {restriction.description}"
                return resultat
            
            if type_transaction == 'TRANSFERT_SORTANT' and not restriction.autorise_transferts_sortants:
                resultat['autorise'] = False
                resultat['raison'] = f"Transferts sortants interdits : {restriction.description}"
                return resultat
            
            # Vérifier les limites de montant
            if montant:
                if restriction.montant_max_journalier and montant > restriction.montant_max_journalier:
                    resultat['autorise'] = False
                    resultat['raison'] = f"Montant dépasse la limite journalière de {restriction.montant_max_journalier}"
                    return resultat
                
                if restriction.limite_montant:
                    resultat['limite_montant'] = float(restriction.montant_max_journalier)
        
        # Vérifier les zones à risque
        zones_risque = LocalisationService.obtenir_zones_risque(utilisateur)
        resultat['zones_risque'] = list(zones_risque)
        
        for zone in zones_risque:
            # Si zone critique, bloquer
            if zone.niveau_risque == 'CRITIQUE':
                resultat['autorise'] = False
                resultat['raison'] = f"Zone à risque critique : {zone.description}"
                return resultat
            
            # Si vérification renforcée requise
            if zone.verification_renforcee:
                resultat['verification_renforcee'] = True
            
            # Vérifier les limites de transaction
            if montant and zone.limite_transaction and montant > zone.limite_transaction:
                resultat['autorise'] = False
                resultat['raison'] = f"Montant dépasse la limite pour zone à risque {zone.niveau_risque}"
                return resultat
        
        return resultat
    
    @staticmethod
    def obtenir_corridors_disponibles(utilisateur, pays_destination_code=None):
        """
        Obtient les corridors de paiement disponibles pour l'utilisateur.
        
        Args:
            utilisateur: Instance de Utilisateur
            pays_destination_code: Code ISO du pays de destination (optionnel)
        
        Returns:
            QuerySet de CorridorPaiement
        """
        if not utilisateur.pays:
            return CorridorPaiement.objects.none()
        
        corridors = CorridorPaiement.objects.filter(
            pays_origine=utilisateur.pays,
            est_actif=True
        )
        
        if pays_destination_code:
            try:
                pays_dest = Pays.objects.get(code_iso_2=pays_destination_code)
                corridors = corridors.filter(pays_destination=pays_dest)
            except Pays.DoesNotExist:
                return CorridorPaiement.objects.none()
        
        return corridors.order_by('-est_prioritaire', '-volume_transactions_mensuel')
    
    @staticmethod
    def obtenir_info_complete_localisation(utilisateur):
        """
        Obtient toutes les informations de localisation pour un utilisateur.
        Utile pour l'affichage dans le profil ou pour les logs.
        """
        info = {
            'pays': None,
            'fuseau_horaire': None,
            'zones_risque': [],
            'restrictions_actives': [],
            'corridors_disponibles': [],
            'verification_renforcee': False,
            'autorise_transactions': True
        }
        
        if utilisateur.pays:
            info['pays'] = {
                'id': str(utilisateur.pays.id),
                'code_iso_2': utilisateur.pays.code_iso_2,
                'nom': utilisateur.pays.nom,
                'continent': utilisateur.pays.continent,
                'autorise_systeme': utilisateur.pays.autorise_systeme
            }
        
        fuseau = LocalisationService.obtenir_fuseau_horaire(utilisateur)
        if fuseau:
            info['fuseau_horaire'] = {
                'code': fuseau.code,
                'nom': fuseau.nom,
                'offset_utc': fuseau.offset_utc
            }
        
        zones = LocalisationService.obtenir_zones_risque(utilisateur)
        info['zones_risque'] = [{
            'niveau': zone.niveau_risque,
            'type': zone.type_risque,
            'score': zone.score_risque,
            'verification_renforcee': zone.verification_renforcee
        } for zone in zones]
        
        restrictions = LocalisationService.obtenir_restrictions_actives(utilisateur)
        info['restrictions_actives'] = [{
            'type': r.type_restriction,
            'niveau': r.niveau_restriction,
            'autorise_transactions': r.autorise_transactions
        } for r in restrictions]
        
        corridors = LocalisationService.obtenir_corridors_disponibles(utilisateur)
        info['corridors_disponibles'] = [{
            'code': c.code,
            'destination': c.pays_destination.nom,
            'destination_code': c.pays_destination.code_iso_2
        } for c in corridors[:10]]  # Limiter à 10
        
        # Vérifier si vérification renforcée nécessaire
        info['verification_renforcee'] = any(z.verification_renforcee for z in zones)
        
        # Vérifier si transactions autorisées
        verif = LocalisationService.verifier_autorisation_transaction(utilisateur)
        info['autorise_transactions'] = verif['autorise']
        
        return info
