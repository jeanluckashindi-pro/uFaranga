"""
Service d'envoi de SMS pour les codes de confirmation.
"""
import logging
import random
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from config.settings.services import SMS_CONFIG
from .models import CodeConfirmationSMS, HistoriqueMotDePasse
from apps.identite.models import Utilisateur as UtilisateurIdentite

logger = logging.getLogger('apps')


def generer_code_confirmation():
    """Génère un code de confirmation à 5 chiffres."""
    return str(random.randint(10000, 99999))


def formater_code_sms(code):
    """Formate le code au format UF-CCF-PSW-XXXXX."""
    return f"UF-CCF-PSW-{code}"


def stocker_code_confirmation(telephone, code, duree_minutes=15, type_code='VERIFICATION_TELEPHONE', 
                             utilisateur_id=None, courriel='', prenom='', 
                             adresse_ip=None, user_agent='', message_envoye=''):
    """
    Stocke le code de confirmation dans la base de données.
    Si un code actif existe déjà pour ce numéro, il est marqué comme remplacé.
    
    Args:
        telephone: Numéro de téléphone
        code: Code à 5 chiffres
        duree_minutes: Durée de validité en minutes (défaut: 15)
        type_code: Type de code (VERIFICATION_TELEPHONE, REINITIALISATION_MDP, etc.)
        utilisateur_id: ID de l'utilisateur (optionnel)
        courriel: Email de l'utilisateur (optionnel)
        prenom: Prénom de l'utilisateur (optionnel)
        adresse_ip: Adresse IP de la requête (optionnel)
        user_agent: User agent de la requête (optionnel)
        message_envoye: Message SMS envoyé (optionnel)
    
    Returns:
        CodeConfirmationSMS: L'objet code créé
    """
    try:
        # Marquer tous les codes actifs existants pour ce numéro comme remplacés
        codes_actifs = CodeConfirmationSMS.objects.filter(
            numero_telephone=telephone,
            statut='ACTIF'
        )
        
        if codes_actifs.exists():
            logger.info(f"Remplacement de {codes_actifs.count()} code(s) actif(s) pour {telephone}")
            codes_actifs.update(statut='REMPLACE')
        
        # Créer le nouveau code
        code_formate = formater_code_sms(code)
        date_expiration = timezone.now() + timedelta(minutes=duree_minutes)
        
        code_obj = CodeConfirmationSMS.objects.create(
            utilisateur_id=utilisateur_id,
            numero_telephone=telephone,
            courriel=courriel,
            prenom=prenom,
            code=code,
            code_formate=code_formate,
            type_code=type_code,
            date_expiration=date_expiration,
            duree_validite_minutes=duree_minutes,
            statut='ACTIF',
            adresse_ip=adresse_ip,
            user_agent=user_agent,
            message_envoye=message_envoye,
        )
        
        logger.info(
            f"Code de confirmation créé pour {telephone} "
            f"(valide {duree_minutes} min, expire à {date_expiration})"
        )
        return code_obj
        
    except Exception as e:
        logger.error(f"Erreur lors du stockage du code: {str(e)}")
        return None


def verifier_code_confirmation(telephone, code):
    """
    Vérifie si le code de confirmation est valide.
    
    Args:
        telephone: Numéro de téléphone
        code: Code à vérifier (5 chiffres)
    
    Returns:
        dict: {
            'valide': bool,
            'message': str,
            'code_obj': CodeConfirmationSMS ou None
        }
    """
    try:
        # Rechercher le code actif pour ce numéro
        code_obj = CodeConfirmationSMS.objects.filter(
            numero_telephone=telephone,
            code=str(code),
            statut='ACTIF'
        ).order_by('-date_creation').first()
        
        if not code_obj:
            logger.warning(f"Aucun code actif trouvé pour {telephone}")
            return {
                'valide': False,
                'message': 'Code invalide ou expiré',
                'code_obj': None
            }
        
        # Incrémenter le nombre de tentatives
        code_obj.incrementer_tentatives()
        
        # Vérifier si le code est expiré
        if timezone.now() > code_obj.date_expiration:
            logger.warning(f"Code expiré pour {telephone}")
            code_obj.marquer_comme_expire()
            return {
                'valide': False,
                'message': 'Code expiré',
                'code_obj': code_obj
            }
        
        # Code valide
        logger.info(f"Code de confirmation vérifié avec succès pour {telephone}")
        code_obj.marquer_comme_utilise()
        
        return {
            'valide': True,
            'message': 'Code valide',
            'code_obj': code_obj
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la vérification du code: {str(e)}")
        return {
            'valide': False,
            'message': f'Erreur: {str(e)}',
            'code_obj': None
        }


def envoyer_sms(telephone, message):
    """
    Envoie un SMS via l'API Mediabox.
    
    Args:
        telephone: Numéro de téléphone (ex: "62046725")
        message: Message à envoyer
    
    Returns:
        dict: Résultat de l'envoi avec 'success' (bool) et 'message' (str)
    """
    try:
        url = SMS_CONFIG['SERVICE_URL']
        payload = {
            "phone": telephone,
            "txt_message": message
        }
        
        response = requests.post(
            url,
            json=payload,
            timeout=SMS_CONFIG.get('TIMEOUT', 10),
            verify=SMS_CONFIG.get('VERIFY_SSL', True)
        )
        
        if response.status_code == 200:
            logger.info(f"SMS envoyé avec succès à {telephone}")
            return {
                'success': True,
                'message': 'SMS envoyé avec succès',
                'response': response.json() if response.content else {}
            }
        else:
            logger.error(f"Erreur lors de l'envoi du SMS: {response.status_code} - {response.text}")
            return {
                'success': False,
                'message': f"Erreur lors de l'envoi du SMS: {response.status_code}",
                'error': response.text
            }
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout lors de l'envoi du SMS à {telephone}")
        return {
            'success': False,
            'message': 'Délai d\'attente dépassé lors de l\'envoi du SMS'
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur réseau lors de l'envoi du SMS: {str(e)}")
        return {
            'success': False,
            'message': f'Erreur réseau: {str(e)}'
        }
    
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'envoi du SMS: {str(e)}")
        return {
            'success': False,
            'message': f'Erreur inattendue: {str(e)}'
        }


def envoyer_code_confirmation(telephone, prenom=None, type_code='VERIFICATION_TELEPHONE',
                             utilisateur_id=None, courriel='', adresse_ip=None, user_agent=''):
    """
    Génère et envoie un code de confirmation par SMS.
    
    Args:
        telephone: Numéro de téléphone
        prenom: Prénom de l'utilisateur (optionnel)
        type_code: Type de code (VERIFICATION_TELEPHONE, REINITIALISATION_MDP, etc.)
        utilisateur_id: ID de l'utilisateur (optionnel)
        courriel: Email de l'utilisateur (optionnel)
        adresse_ip: Adresse IP de la requête (optionnel)
        user_agent: User agent de la requête (optionnel)
    
    Returns:
        dict: Résultat avec 'success' (bool), 'message' (str), et 'code_formate' (str) si succès
    """
    # Générer le code
    code = generer_code_confirmation()
    code_formate = formater_code_sms(code)
    
    # Préparer le message
    if prenom:
        message = f"Bonjour {prenom}, votre code de confirmation est: {code_formate}"
    else:
        message = f"Votre code de confirmation est: {code_formate}"
    
    # Envoyer le SMS
    resultat = envoyer_sms(telephone, message)
    
    # Stocker le code dans la base de données (même si l'envoi échoue, pour traçabilité)
    code_obj = stocker_code_confirmation(
        telephone=telephone,
        code=code,
        duree_minutes=15,  # 15 minutes de validité
        type_code=type_code,
        utilisateur_id=utilisateur_id,
        courriel=courriel,
        prenom=prenom or '',
        adresse_ip=adresse_ip,
        user_agent=user_agent,
        message_envoye=message
    )
    
    if not code_obj:
        return {
            'success': False,
            'message': 'Erreur lors du stockage du code de confirmation'
        }
    
    # Ajouter les informations du code dans le résultat
    if resultat['success']:
        resultat['code_formate'] = code_formate
        resultat['code'] = code  # Pour les tests uniquement
        resultat['code_id'] = str(code_obj.id)
        resultat['date_expiration'] = code_obj.date_expiration.isoformat()
    else:
        # Marquer le code comme expiré si l'envoi a échoué
        code_obj.marquer_comme_expire()
        code_obj.metadonnees['erreur_envoi'] = resultat.get('message', 'Erreur inconnue')
        code_obj.save(update_fields=['metadonnees'])
    
    return resultat



def enregistrer_changement_mot_de_passe(utilisateur, ancien_hash, nouveau_hash, 
                                        type_changement='MODIFICATION', code_utilise='',
                                        adresse_ip=None, user_agent='', raison=''):
    """
    Enregistre un changement de mot de passe dans l'historique.
    
    Args:
        utilisateur: Instance de UtilisateurIdentite
        ancien_hash: Hash de l'ancien mot de passe
        nouveau_hash: Hash du nouveau mot de passe
        type_changement: Type de changement (MODIFICATION, REINITIALISATION, etc.)
        code_utilise: Code de confirmation utilisé (si applicable)
        adresse_ip: Adresse IP de la requête
        user_agent: User agent de la requête
        raison: Raison du changement
    
    Returns:
        HistoriqueMotDePasse: L'objet historique créé
    """
    try:
        historique = HistoriqueMotDePasse.objects.create(
            utilisateur_id=utilisateur.id,
            courriel=utilisateur.courriel,
            numero_telephone=utilisateur.numero_telephone,
            type_changement=type_changement,
            ancien_hash=ancien_hash,
            nouveau_hash=nouveau_hash,
            code_confirmation_utilise=code_utilise,
            adresse_ip=adresse_ip,
            user_agent=user_agent,
            raison=raison,
        )
        
        logger.info(
            f"Changement de mot de passe enregistré pour {utilisateur.courriel} "
            f"(type: {type_changement})"
        )
        
        return historique
        
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de l'historique: {str(e)}")
        return None


def obtenir_historique_changements_mdp(utilisateur_id=None, courriel=None, 
                                       numero_telephone=None, limite=10):
    """
    Récupère l'historique des changements de mot de passe.
    
    Args:
        utilisateur_id: ID de l'utilisateur
        courriel: Email de l'utilisateur
        numero_telephone: Numéro de téléphone
        limite: Nombre maximum de résultats
    
    Returns:
        QuerySet: Liste des changements de mot de passe
    """
    try:
        queryset = HistoriqueMotDePasse.objects.all()
        
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
        elif courriel:
            queryset = queryset.filter(courriel=courriel)
        elif numero_telephone:
            queryset = queryset.filter(numero_telephone=numero_telephone)
        else:
            return HistoriqueMotDePasse.objects.none()
        
        return queryset.order_by('-date_changement')[:limite]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'historique: {str(e)}")
        return HistoriqueMotDePasse.objects.none()


def compter_changements_mdp(utilisateur_id=None, courriel=None, numero_telephone=None):
    """
    Compte le nombre total de changements de mot de passe.
    
    Args:
        utilisateur_id: ID de l'utilisateur
        courriel: Email de l'utilisateur
        numero_telephone: Numéro de téléphone
    
    Returns:
        int: Nombre de changements
    """
    try:
        queryset = HistoriqueMotDePasse.objects.all()
        
        if utilisateur_id:
            queryset = queryset.filter(utilisateur_id=utilisateur_id)
        elif courriel:
            queryset = queryset.filter(courriel=courriel)
        elif numero_telephone:
            queryset = queryset.filter(numero_telephone=numero_telephone)
        else:
            return 0
        
        return queryset.count()
        
    except Exception as e:
        logger.error(f"Erreur lors du comptage des changements: {str(e)}")
        return 0


def nettoyer_codes_expires():
    """
    Marque tous les codes expirés comme EXPIRE.
    À exécuter périodiquement (tâche Celery).
    
    Returns:
        int: Nombre de codes marqués comme expirés
    """
    try:
        codes_expires = CodeConfirmationSMS.objects.filter(
            statut='ACTIF',
            date_expiration__lt=timezone.now()
        )
        
        count = codes_expires.count()
        codes_expires.update(statut='EXPIRE')
        
        logger.info(f"{count} code(s) marqué(s) comme expiré(s)")
        return count
        
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des codes expirés: {str(e)}")
        return 0
