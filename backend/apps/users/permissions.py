from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Permission personnalisée :
    - L'utilisateur peut accéder/modifier son propre profil
    - Les admins peuvent accéder/modifier tous les profils
    """

    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.is_staff:
            return True
        # L'utilisateur ne peut accéder qu'à son propre objet
        return obj == request.user or (hasattr(obj, 'user') and obj.user == request.user)


class IsServiceAccount(BasePermission):
    """
    Permission pour les appels inter-services.
    Les services utilisent un header spécial X-Service-Key.
    """

    def has_permission(self, request, view):
        import os
        service_key = request.headers.get('X-Service-Key', '')
        expected_key = os.environ.get('INTERNAL_SERVICE_KEY', 'ufaranga-internal-key')
        return service_key == expected_key
