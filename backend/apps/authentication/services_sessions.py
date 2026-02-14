"""
Logique "un compte utilisé par plusieurs personnes en même temps".
Compte le nombre de sessions actives (jetons JWT non révoqués) par utilisateur.
"""
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

User = get_user_model()


def get_sessions_actives_count(user):
    """
    Retourne le nombre de sessions actives pour un utilisateur (users.User).
    Une session = un refresh token JWT non blacklisté et non expiré.
    Si > 1 : le même compte est utilisé à plusieurs endroits en même temps.
    """
    if not user or not user.pk:
        return 0
    now = timezone.now()
    # Tokens non blacklistés et non expirés = sessions actives
    return OutstandingToken.objects.filter(
        user_id=user.pk,
        expires_at__gt=now,
    ).filter(
        blacklistedtoken__isnull=True
    ).count()


def compte_utilise_par_plusieurs_sessions(user):
    """
    True si ce compte a plus d'une session active (même compte utilisé par
    plusieurs personnes ou appareils en même temps).
    """
    return get_sessions_actives_count(user) > 1


def get_sessions_actives_info(user):
    """
    Retourne un dict avec le nombre de sessions actives et un booléen
    pour l'utilisation concurrente du compte.
    """
    count = get_sessions_actives_count(user)
    return {
        'nombre_sessions_actives': count,
        'connexion_multiple': count > 1,
        'message': (
            f'Ce compte est actuellement utilisé sur {count} session(s) (appareil(s) ou connexion(s)).'
            if count > 0 else 'Aucune session active.'
        ),
    }
