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
]
