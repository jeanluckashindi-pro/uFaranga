from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Login — POST /api/v1/auth/login/
    path('login/', views.LoginView.as_view(), name='login'),

    # Register — POST /api/v1/auth/register/
    path('register/', views.RegisterView.as_view(), name='register'),

    # Refresh Token — POST /api/v1/auth/token/refresh/
    path('token/refresh/', views.RefreshTokenView.as_view(), name='token-refresh'),

    # Logout — POST /api/v1/auth/logout/
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Logout All Sessions — POST /api/v1/auth/logout-all/
    path('logout-all/', views.LogoutAllView.as_view(), name='logout-all'),

    # Change Password — POST /api/v1/auth/change-password/
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    # Me — GET /api/v1/auth/me/
    path('me/', views.MeView.as_view(), name='me'),
]
