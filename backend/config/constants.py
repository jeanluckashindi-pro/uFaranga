
from datetime import timedelta


# =============================================================================
# AUTHENTIFICATION — Connexion / sécurité
# =============================================================================
# Nombre d'échecs de mot de passe avant blocage temporaire du compte
MAX_TENTATIVES_CONNEXION = 5
# Durée du blocage (en minutes) après dépassement du seuil
DUREE_BLOCAGE_MINUTES = 15

ACCESS_TOKEN_LIFETIME_MINUTES = 60
# Refresh token : durée par défaut (sans "Se souvenir de moi"), en jours
REFRESH_TOKEN_LIFETIME_DAYS = 7
# Refresh token : durée si "Se souvenir de moi" coché, en jours
REFRESH_TOKEN_LIFETIME_REMEMBER_ME_DAYS = 30

# Timedeltas dérivés (pour SIMPLE_JWT et usage direct)
ACCESS_TOKEN_LIFETIME = timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES)
REFRESH_TOKEN_LIFETIME = timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS)
REFRESH_TOKEN_LIFETIME_REMEMBER_ME = timedelta(days=REFRESH_TOKEN_LIFETIME_REMEMBER_ME_DAYS)
