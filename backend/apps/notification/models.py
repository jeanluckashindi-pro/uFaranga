"""
Modèles pour le schéma NOTIFICATION
Système de notifications
"""
from django.db import models
from django.utils import timezone
import uuid


class Notification(models.Model):
    """Notifications - notification.notifications"""
    
    TYPE_NOTIFICATION_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('PUSH', 'Push'),
        ('IN_APP', 'In-App'),
        ('WEBHOOK', 'Webhook'),
    ]
    
    PRIORITE_CHOICES = [
        ('FAIBLE', 'Faible'),
        ('NORMALE', 'Normale'),
        ('HAUTE', 'Haute'),
        ('URGENTE', 'Urgente'),
    ]
    
    STATUT_ENVOI_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ENVOYE', 'Envoyé'),
        ('ECHEC', 'Échec'),
        ('ANNULE', 'Annulé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur_id = models.UUIDField(db_index=True)
    
    # Type et canal
    type_notification = models.CharField(
        max_length=50,
        choices=TYPE_NOTIFICATION_CHOICES,
        db_index=True
    )
    canal = models.CharField(max_length=20)
    
    # Destinataire
    destinataire = models.CharField(max_length=255)
    
    # Contenu
    sujet = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    message_html = models.TextField(blank=True)
    
    # Template
    template_id = models.CharField(max_length=100, blank=True)
    variables_template = models.JSONField(default=dict, blank=True)
    
    # Priorité
    priorite = models.CharField(
        max_length=20,
        choices=PRIORITE_CHOICES,
        default='NORMALE'
    )
    
    # Envoi
    statut_envoi = models.CharField(
        max_length=20,
        choices=STATUT_ENVOI_CHOICES,
        default='EN_ATTENTE',
        db_index=True
    )
    nombre_tentatives = models.IntegerField(default=0)
    max_tentatives = models.IntegerField(default=3)
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_lecture = models.DateTimeField(null=True, blank=True)
    
    # Erreurs
    erreur_envoi = models.TextField(blank=True)
    code_erreur = models.CharField(max_length=50, blank=True)
    
    # Planification
    date_planification = models.DateTimeField(null=True, blank=True)
    
    # Fournisseur
    fournisseur = models.CharField(max_length=50, blank=True)
    id_externe = models.CharField(max_length=100, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(default=timezone.now)
    metadonnees = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'notification"."notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['utilisateur_id']),
            models.Index(fields=['statut_envoi']),
            models.Index(fields=['type_notification']),
            models.Index(
                fields=['statut_envoi', 'nombre_tentatives', 'date_planification'],
                name='idx_notif_en_attente'
            ),
        ]
    
    def __str__(self):
        return f"{self.type_notification} - {self.destinataire} - {self.statut_envoi}"
