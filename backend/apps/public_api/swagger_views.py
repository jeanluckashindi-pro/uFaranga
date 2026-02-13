"""
Vues Swagger/OpenAPI pour l'API publique
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.settings import spectacular_settings
from rest_framework import serializers


class PublicAPISchemaView(APIView):
    """
    Vue pour générer le schéma OpenAPI de l'API publique uniquement
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """Génère le schéma OpenAPI filtré"""
        
        # Schéma OpenAPI manuel pour l'API publique
        schema = {
            'openapi': '3.0.3',
            'info': {
                'title': 'API Publique uFaranga',
                'version': '1.0.0',
                'description': 'Documentation interactive de l\'API publique uFaranga.',
                'contact': {
                    'name': 'uFaranga Support',
                    'email': 'developers@ufaranga.bi'
                }
            },
            'servers': [
                {'url': 'http://localhost:8000', 'description': 'Local'},
                {'url': 'https://sandbox-api.ufaranga.bi', 'description': 'Sandbox'},
                {'url': 'https://api.ufaranga.bi', 'description': 'Production'}
            ],
            'tags': [
                {'name': 'Système', 'description': 'Santé et statut'},
                {'name': 'Tarification', 'description': 'Frais et taux de change'},
                {'name': 'Informations', 'description': 'Pays, devises, types'},
                {'name': 'Validation', 'description': 'Validation téléphone/compte'},
                {'name': 'Agents', 'description': 'Recherche d\'agents'},
                {'name': 'Inscription', 'description': 'Inscription utilisateurs'},
                {'name': 'Support', 'description': 'Contact et FAQ'}
            ],
            'paths': self._get_public_paths(),
            'components': {
                'securitySchemes': {
                    'ApiKeyAuth': {
                        'type': 'apiKey',
                        'in': 'header',
                        'name': 'Authorization',
                        'description': 'Format : ApiKey votre_cle_api'
                    }
                },
                'schemas': self._get_schemas()
            },
            'security': [{'ApiKeyAuth': []}]
        }
        
        return Response(schema)
    
    def _get_public_paths(self):
        """Définit manuellement les paths de l'API publique"""
        return {
            '/api/public/health/': {
                'get': {
                    'tags': ['Système'],
                    'summary': 'Vérification de santé',
                    'description': 'Vérifie l\'état de santé du système',
                    'operationId': 'health_check',
                    'responses': {
                        '200': {
                            'description': 'Système en bonne santé',
                            'content': {
                                'application/json': {
                                    'example': {
                                        'status': 'healthy',
                                        'timestamp': '2026-02-13T16:00:00Z',
                                        'version': '1.0.0',
                                        'environment': 'development'
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/api/public/status/': {
                'get': {
                    'tags': ['Système'],
                    'summary': 'Statut des services',
                    'description': 'Retourne le statut de tous les services',
                    'operationId': 'system_status',
                    'responses': {
                        '200': {'description': 'Statut des services'}
                    }
                }
            },
            '/api/public/version/': {
                'get': {
                    'tags': ['Système'],
                    'summary': 'Version de l\'API',
                    'operationId': 'api_version',
                    'responses': {
                        '200': {'description': 'Version de l\'API'}
                    }
                }
            },
            '/api/public/fees/calculator/': {
                'get': {
                    'tags': ['Tarification'],
                    'summary': 'Calculer les frais',
                    'description': 'Calcule les frais pour une transaction',
                    'operationId': 'calculate_fees',
                    'parameters': [
                        {
                            'name': 'amount',
                            'in': 'query',
                            'required': True,
                            'schema': {'type': 'number'},
                            'description': 'Montant de la transaction'
                        },
                        {
                            'name': 'type',
                            'in': 'query',
                            'required': True,
                            'schema': {
                                'type': 'string',
                                'enum': ['P2P', 'DEPOT', 'RETRAIT', 'PAIEMENT_MARCHAND', 
                                        'PAIEMENT_FACTURE', 'RECHARGE_TELEPHONIQUE',
                                        'VIREMENT_BANCAIRE', 'TRANSFERT_INTERNATIONAL']
                            },
                            'description': 'Type de transaction'
                        },
                        {
                            'name': 'currency',
                            'in': 'query',
                            'schema': {'type': 'string', 'default': 'BIF'},
                            'description': 'Devise'
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'Frais calculés',
                            'content': {
                                'application/json': {
                                    'example': {
                                        'montant': 10000.0,
                                        'devise': 'BIF',
                                        'type_transaction': 'P2P',
                                        'frais': 100.0,
                                        'commission': 50.0,
                                        'montant_total': 10150.0
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/api/public/fees/schedule/': {
                'get': {
                    'tags': ['Tarification'],
                    'summary': 'Grille tarifaire',
                    'description': 'Retourne la grille tarifaire complète',
                    'operationId': 'fees_schedule',
                    'responses': {
                        '200': {'description': 'Grille tarifaire'}
                    }
                }
            },
            '/api/public/exchange-rates/': {
                'get': {
                    'tags': ['Tarification'],
                    'summary': 'Taux de change',
                    'description': 'Taux de change en temps réel',
                    'operationId': 'exchange_rates',
                    'responses': {
                        '200': {'description': 'Taux de change'}
                    }
                }
            },
            '/api/public/countries/': {
                'get': {
                    'tags': ['Informations'],
                    'summary': 'Pays supportés',
                    'operationId': 'countries',
                    'responses': {
                        '200': {'description': 'Liste des pays'}
                    }
                }
            },
            '/api/public/currencies/': {
                'get': {
                    'tags': ['Informations'],
                    'summary': 'Devises supportées',
                    'operationId': 'currencies',
                    'responses': {
                        '200': {'description': 'Liste des devises'}
                    }
                }
            },
            '/api/public/transaction-types/': {
                'get': {
                    'tags': ['Informations'],
                    'summary': 'Types de transactions',
                    'operationId': 'transaction_types',
                    'responses': {
                        '200': {'description': 'Types de transactions'}
                    }
                }
            },
            '/api/public/validate/phone/': {
                'post': {
                    'tags': ['Validation'],
                    'summary': 'Valider un téléphone',
                    'description': 'Valide le format d\'un numéro de téléphone',
                    'operationId': 'validate_phone',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'phone': {'type': 'string', 'example': '+25779123456'}
                                    },
                                    'required': ['phone']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'Validation réussie'}
                    }
                }
            },
            '/api/public/validate/account/': {
                'post': {
                    'tags': ['Validation'],
                    'summary': 'Vérifier un compte',
                    'description': 'Vérifie si un compte existe',
                    'operationId': 'validate_account',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'account': {'type': 'string'}
                                    },
                                    'required': ['account']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'Vérification effectuée'}
                    }
                }
            },
            '/api/public/agents/search/': {
                'get': {
                    'tags': ['Agents'],
                    'summary': 'Rechercher des agents',
                    'description': 'Recherche d\'agents à proximité',
                    'operationId': 'search_agents',
                    'parameters': [
                        {'name': 'latitude', 'in': 'query', 'schema': {'type': 'number'}},
                        {'name': 'longitude', 'in': 'query', 'schema': {'type': 'number'}},
                        {'name': 'radius', 'in': 'query', 'schema': {'type': 'integer', 'default': 5000}},
                        {'name': 'city', 'in': 'query', 'schema': {'type': 'string'}},
                        {'name': 'name', 'in': 'query', 'schema': {'type': 'string'}}
                    ],
                    'responses': {
                        '200': {'description': 'Liste des agents'}
                    }
                }
            },
            '/api/public/agents/{agent_id}/': {
                'get': {
                    'tags': ['Agents'],
                    'summary': 'Détails d\'un agent',
                    'operationId': 'agent_detail',
                    'parameters': [
                        {'name': 'agent_id', 'in': 'path', 'required': True, 'schema': {'type': 'string', 'format': 'uuid'}}
                    ],
                    'responses': {
                        '200': {'description': 'Détails de l\'agent'}
                    }
                }
            },
            '/api/public/register/initiate/': {
                'post': {
                    'tags': ['Inscription'],
                    'summary': 'Initier une inscription',
                    'operationId': 'register_initiate',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'phone': {'type': 'string'},
                                        'email': {'type': 'string'},
                                        'first_name': {'type': 'string'},
                                        'last_name': {'type': 'string'}
                                    },
                                    'required': ['phone', 'email', 'first_name', 'last_name']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': {'description': 'Inscription initiée'}
                    }
                }
            },
            '/api/public/register/verify-otp/': {
                'post': {
                    'tags': ['Inscription'],
                    'summary': 'Vérifier le code OTP',
                    'operationId': 'verify_otp',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'phone': {'type': 'string'},
                                        'otp': {'type': 'string'}
                                    },
                                    'required': ['phone', 'otp']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {'description': 'OTP vérifié'}
                    }
                }
            },
            '/api/public/contact/': {
                'post': {
                    'tags': ['Support'],
                    'summary': 'Contacter le support',
                    'operationId': 'contact_support',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string'},
                                        'email': {'type': 'string'},
                                        'subject': {'type': 'string'},
                                        'message': {'type': 'string'}
                                    },
                                    'required': ['name', 'email', 'subject', 'message']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': {'description': 'Message envoyé'}
                    }
                }
            },
            '/api/public/faq/': {
                'get': {
                    'tags': ['Support'],
                    'summary': 'Questions fréquentes',
                    'operationId': 'faq',
                    'responses': {
                        '200': {'description': 'Liste des FAQ'}
                    }
                }
            }
        }
    
    def _get_schemas(self):
        """Définit les schémas de données"""
        return {}


class PublicAPISwaggerView(APIView):
    """
    Vue Swagger UI pour l'API publique
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """Affiche Swagger UI"""
        return render(request, 'public_api/swagger.html', {
            'schema_url': '/api/public/schema/',
            'title': 'API Publique uFaranga - Documentation'
        })


class PublicAPIRedocView(APIView):
    """
    Vue ReDoc pour l'API publique
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        """Affiche ReDoc"""
        return render(request, 'public_api/redoc.html', {
            'schema_url': '/api/public/schema/',
            'title': 'uFaranga Public API'
        })
