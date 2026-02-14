"""
Droits d'accès au CRUD localisation : réservé aux personnes autorisées (SYSTEME, SUPER_ADMIN).
"""
from rest_framework import permissions


class IsSystemeOrSuperAdmin(permissions.BasePermission):
    """
    Autorise uniquement les utilisateurs dont le type (identite.utilisateurs)
    est SYSTEME ou SUPER_ADMIN.
    """
    message = "Accès réservé aux comptes Système et Super Administrateur."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        from apps.identite.models import Utilisateur as UtilisateurIdentite
        utilisateur = UtilisateurIdentite.objects.filter(
            courriel=request.user.email
        ).first()
        if not utilisateur:
            return False
        return utilisateur.type_utilisateur in ('SYSTEME', 'SUPER_ADMIN')
