from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Connexion — POST /api/v1/authentification/connexion/
    path('connexion/', views.LoginView.as_view(), name='login'),

    # Inscription — POST /api/v1/authentification/inscription/
    path('inscription/', views.RegisterView.as_view(), name='register'),

    # Actualiser le jeton — POST /api/v1/authentification/jeton/actualiser/
    path('jeton/actualiser/', views.RefreshTokenView.as_view(), name='token-refresh'),

    # Déconnexion — POST /api/v1/authentification/deconnexion/
    path('deconnexion/', views.LogoutView.as_view(), name='logout'),

    # Déconnexion de toutes les sessions — POST /api/v1/authentification/deconnexion-toutes/
    path('deconnexion-toutes/', views.LogoutAllView.as_view(), name='logout-all'),

    # Déconnecter les autres sessions (garder la session actuelle) — POST /api/v1/authentification/deconnexion-autres/
    path('deconnexion-autres/', views.LogoutOtherSessionsView.as_view(), name='logout-other-sessions'),

    # Modifier le mot de passe — POST /api/v1/authentification/modifier-mot-de-passe/
    path('modifier-mot-de-passe/', views.ChangePasswordView.as_view(), name='change-password'),

    # Moi (profil connecté) — GET /api/v1/authentification/moi/
    path('moi/', views.MeView.as_view(), name='me'),

    # Sessions actives (connexion multiple) — GET /api/v1/authentification/sessions-actives/
    path('sessions-actives/', views.SessionsActivesView.as_view(), name='sessions-actives'),

    # Envoyer code de confirmation — POST /api/v1/authentification/envoyer-code-confirmation/
    path('envoyer-code-confirmation/', views.EnvoyerCodeConfirmationView.as_view(), name='envoyer-code-confirmation'),

    # Vérifier code de confirmation — POST /api/v1/authentification/verifier-code-confirmation/
    path('verifier-code-confirmation/', views.VerifierCodeConfirmationView.as_view(), name='verifier-code-confirmation'),

    # Réinitialiser mot de passe avec SMS — POST /api/v1/authentification/reinitialiser-mot-de-passe-sms/
    path('reinitialiser-mot-de-passe-sms/', views.ReinitialiserMotDePasseSMSView.as_view(), name='reinitialiser-mot-de-passe-sms'),

    # Historique des changements de mot de passe — GET /api/v1/authentification/historique-mot-de-passe/
    path('historique-mot-de-passe/', views.HistoriqueMotDePasseView.as_view(), name='historique-mot-de-passe'),
]
