"""
Permissions OAuth 2.0 personnalisées basées sur les scopes
"""
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework import TokenHasScope, TokenHasReadWriteScope


class TokenHasTransactionScope(permissions.BasePermission):
    """
    Permission pour vérifier que le token a le scope 'transactions'
    """
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.is_valid(['transactions'])


class TokenHasWalletScope(permissions.BasePermission):
    """
    Permission pour vérifier que le token a le scope 'wallets'
    """
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.is_valid(['wallets'])


class TokenHasProfileScope(permissions.BasePermission):
    """
    Permission pour vérifier que le token a le scope 'profile'
    """
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.is_valid(['profile'])


class TokenHasAdminScope(permissions.BasePermission):
    """
    Permission pour vérifier que le token a le scope 'admin'
    """
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.is_valid(['admin'])


class TokenHasRequiredScope(permissions.BasePermission):
    """
    Permission générique pour vérifier les scopes requis
    Usage: 
        permission_classes = [TokenHasRequiredScope]
        required_scopes = ['read', 'write']
    """
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        
        # Récupérer les scopes requis depuis la vue
        required_scopes = getattr(view, 'required_scopes', [])
        if not required_scopes:
            return True
        
        return token.is_valid(required_scopes)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission pour autoriser seulement le propriétaire à modifier
    """
    def has_object_permission(self, request, view, obj):
        # Les requêtes de lecture sont autorisées pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Les requêtes d'écriture sont autorisées seulement pour le propriétaire
        return obj.user == request.user


class TokenHasKYCLevel(permissions.BasePermission):
    """
    Permission basée sur le niveau KYC de l'utilisateur
    Usage:
        permission_classes = [TokenHasKYCLevel]
        required_kyc_level = 2
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        required_level = getattr(view, 'required_kyc_level', 0)
        user_kyc_level = getattr(request.user, 'niveau_kyc', 0)
        
        return user_kyc_level >= required_level
