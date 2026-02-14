"""
URLs pour l'API publique
"""
from django.urls import path
from . import views
from .swagger_views import PublicAPISchemaView, PublicAPISwaggerView, PublicAPIRedocView

app_name = 'public_api'

urlpatterns = [
    # Documentation API
    path('schema/', PublicAPISchemaView.as_view(), name='schema'),
    path('docs/', PublicAPISwaggerView.as_view(), name='docs'),
    path('redoc/', PublicAPIRedocView.as_view(), name='redoc'),
    
    # Système
    path('sante/', views.health_check, name='health'),
    path('statut/', views.system_status, name='status'),
    path('version/', views.api_version, name='version'),
    
    # Tarification & Frais
    path('frais/calculateur/', views.FeesCalculatorView.as_view(), name='fees-calculator'),
    path('frais/grille/', views.fees_schedule, name='fees-schedule'),
    path('taux-change/', views.exchange_rates, name='exchange-rates'),
    
    # Informations générales
    path('pays/', views.supported_countries, name='countries'),
    path('devises/', views.supported_currencies, name='currencies'),
    path('types-transaction/', views.transaction_types, name='transaction-types'),
    
    # Validation
    path('valider/telephone/', views.validate_phone, name='validate-phone'),
    path('valider/compte/', views.validate_account, name='validate-account'),
    
    # Agents
    path('agents/recherche/', views.search_agents, name='agents-search'),
    path('agents/<uuid:agent_id>/', views.agent_detail, name='agent-detail'),
    
    # Inscription
    path('inscription/initier/', views.register_initiate, name='register-initiate'),
    path('inscription/verifier-otp/', views.verify_otp, name='verify-otp'),
    
    # Support
    path('contact/', views.contact_support, name='contact'),
    path('faq/', views.faq, name='faq'),
]
