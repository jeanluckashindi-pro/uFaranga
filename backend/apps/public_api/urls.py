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
    path('health/', views.health_check, name='health'),
    path('status/', views.system_status, name='status'),
    path('version/', views.api_version, name='version'),
    
    # Tarification & Frais
    path('fees/calculator/', views.FeesCalculatorView.as_view(), name='fees-calculator'),
    path('fees/schedule/', views.fees_schedule, name='fees-schedule'),
    path('exchange-rates/', views.exchange_rates, name='exchange-rates'),
    
    # Informations générales
    path('countries/', views.supported_countries, name='countries'),
    path('currencies/', views.supported_currencies, name='currencies'),
    path('transaction-types/', views.transaction_types, name='transaction-types'),
    
    # Validation
    path('validate/phone/', views.validate_phone, name='validate-phone'),
    path('validate/account/', views.validate_account, name='validate-account'),
    
    # Agents
    path('agents/search/', views.search_agents, name='agents-search'),
    path('agents/<uuid:agent_id>/', views.agent_detail, name='agent-detail'),
    
    # Inscription
    path('register/initiate/', views.register_initiate, name='register-initiate'),
    path('register/verify-otp/', views.verify_otp, name='verify-otp'),
    
    # Support
    path('contact/', views.contact_support, name='contact'),
    path('faq/', views.faq, name='faq'),
]
