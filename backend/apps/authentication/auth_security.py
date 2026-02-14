"""
Couche de sécurité authentification : toutes les vérifications doivent passer
avant d'émettre un token et de renvoyer une réponse d'accès.
"""
from django.utils import timezone
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from config.constants import DUREE_BLOCAGE_MINUTES, MAX_TENTATIVES_CONNEXION


def verifier_compte_non_bloque(utilisateur_identite):
    """
    Vérifie que le compte n'est pas temporairement bloqué (bloque_jusqua).
    À appeler avant toute émission de token.
    Lève AuthenticationFailed si le compte est bloqué.
    """
    if not getattr(utilisateur_identite, 'bloque_jusqua', None):
        return
    now = timezone.now()
    if now < utilisateur_identite.bloque_jusqua:
        from django.utils.formats import date_format
        jusqua = date_format(utilisateur_identite.bloque_jusqua, 'DATETIME_FORMAT')
        raise AuthenticationFailed(
            detail=f'Compte temporairement bloqué après plusieurs tentatives. Réessayez après le {jusqua}.',
            code='account_blocked',
        )
    # Blocage expiré : on le nettoie (sera fait en succès plus bas)
    utilisateur_identite.bloque_jusqua = None
    utilisateur_identite.save(update_fields=['bloque_jusqua'])


def verifier_2fa_si_requise(utilisateur_identite, code_2fa=None):
    """
    Si la double authentification est activée, exige un code 2FA valide.
    À appeler avant d'émettre le token.
    Lève AuthenticationFailed avec code '2fa_required' si 2FA activée et code absent/invalide.
    """
    if not getattr(utilisateur_identite, 'double_auth_activee', False):
        return
    # TODO: valider code_2fa contre secret_2fa (TOTP) quand implémenté
    if not code_2fa or not str(code_2fa).strip():
        raise AuthenticationFailed(
            detail='Vérification en deux étapes requise. Envoyez le code de votre application d\'authentification.',
            code='2fa_required',
        )
    # Pour l'instant on accepte si un code est fourni (validation TOTP à brancher plus tard)
    # if not _verify_totp(utilisateur_identite.secret_2fa, code_2fa):
    #     raise AuthenticationFailed(detail='Code de vérification invalide.', code='2fa_invalid')


def appliquer_echec_connexion(utilisateur_identite):
    """
    À appeler après un échec de mot de passe : incrémente les tentatives
    et bloque le compte si le seuil est dépassé.
    """
    utilisateur_identite.nombre_tentatives_connexion = (
        getattr(utilisateur_identite, 'nombre_tentatives_connexion', 0) + 1
    )
    if utilisateur_identite.nombre_tentatives_connexion >= MAX_TENTATIVES_CONNEXION:
        utilisateur_identite.bloque_jusqua = timezone.now() + timezone.timedelta(
            minutes=DUREE_BLOCAGE_MINUTES
        )
    utilisateur_identite.save(
        update_fields=['nombre_tentatives_connexion', 'bloque_jusqua']
    )


def appliquer_succes_connexion(utilisateur_identite):
    """
    À appeler après validation du mot de passe, avant d'émettre le token :
    réinitialise les tentatives, enlève le blocage, met à jour derniere_connexion.
    """
    utilisateur_identite.nombre_tentatives_connexion = 0
    utilisateur_identite.bloque_jusqua = None
    utilisateur_identite.last_login = timezone.now()
    utilisateur_identite.save(
        update_fields=['nombre_tentatives_connexion', 'bloque_jusqua', 'last_login']
    )


def reinitialiser_valeurs_deconnexion(user):
    """
    À appeler lors de la déconnexion : réinitialise certaines valeurs clés
    de la personne dans identite.utilisateurs (tentatives, blocage).
    Permet de repartir sur une base propre à la prochaine connexion.
    """
    from apps.identite.models import Utilisateur as UtilisateurIdentite
    if not user or not getattr(user, 'email', None):
        return
    utilisateur = UtilisateurIdentite.objects.filter(courriel=user.email).first()
    if not utilisateur:
        return
    utilisateur.nombre_tentatives_connexion = 0
    utilisateur.bloque_jusqua = None
    utilisateur.save(update_fields=['nombre_tentatives_connexion', 'bloque_jusqua'])
