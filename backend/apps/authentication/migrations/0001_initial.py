# Generated migration for authentication models

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='HistoriqueMotDePasse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('utilisateur_id', models.UUIDField(db_index=True)),
                ('courriel', models.EmailField(db_index=True, max_length=254)),
                ('numero_telephone', models.CharField(db_index=True, max_length=20)),
                ('type_changement', models.CharField(choices=[('CREATION', 'Création du compte'), ('MODIFICATION', "Modification par l'utilisateur"), ('REINITIALISATION', 'Réinitialisation par SMS'), ('REINITIALISATION_EMAIL', 'Réinitialisation par email'), ('FORCE_ADMIN', 'Forcé par un administrateur'), ('EXPIRATION', 'Changement suite à expiration')], default='MODIFICATION', max_length=30)),
                ('ancien_hash', models.CharField(blank=True, max_length=255)),
                ('nouveau_hash', models.CharField(max_length=255)),
                ('adresse_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('code_confirmation_utilise', models.CharField(blank=True, max_length=5)),
                ('date_changement', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('raison', models.TextField(blank=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Historique Mot de Passe',
                'verbose_name_plural': 'Historiques Mots de Passe',
                'db_table': 'authentification"."historique_mot_de_passe',
                'ordering': ['-date_changement'],
            },
        ),
        migrations.CreateModel(
            name='CodeConfirmationSMS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('utilisateur_id', models.UUIDField(blank=True, db_index=True, null=True)),
                ('numero_telephone', models.CharField(db_index=True, max_length=20)),
                ('courriel', models.EmailField(blank=True, db_index=True, max_length=254)),
                ('prenom', models.CharField(blank=True, max_length=100)),
                ('code', models.CharField(db_index=True, max_length=5)),
                ('code_formate', models.CharField(max_length=50)),
                ('type_code', models.CharField(choices=[('VERIFICATION_TELEPHONE', 'Vérification de téléphone'), ('REINITIALISATION_MDP', 'Réinitialisation mot de passe'), ('DOUBLE_AUTH', 'Double authentification'), ('CONFIRMATION_TRANSACTION', 'Confirmation de transaction'), ('AUTRE', 'Autre')], default='VERIFICATION_TELEPHONE', max_length=30)),
                ('date_creation', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('date_expiration', models.DateTimeField(db_index=True)),
                ('duree_validite_minutes', models.IntegerField(default=15)),
                ('statut', models.CharField(choices=[('ACTIF', 'Actif'), ('UTILISE', 'Utilisé'), ('EXPIRE', 'Expiré'), ('REMPLACE', 'Remplacé par un nouveau code')], db_index=True, default='ACTIF', max_length=20)),
                ('date_utilisation', models.DateTimeField(blank=True, null=True)),
                ('nombre_tentatives', models.IntegerField(default=0)),
                ('adresse_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('message_envoye', models.TextField(blank=True)),
                ('reponse_service_sms', models.JSONField(blank=True, default=dict)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Code Confirmation SMS',
                'verbose_name_plural': 'Codes Confirmation SMS',
                'db_table': 'authentification"."codes_confirmation_sms',
                'ordering': ['-date_creation'],
            },
        ),
        migrations.AddIndex(
            model_name='historiquemotdepasse',
            index=models.Index(fields=['utilisateur_id', '-date_changement'], name='authentific_utilisa_idx'),
        ),
        migrations.AddIndex(
            model_name='historiquemotdepasse',
            index=models.Index(fields=['courriel', '-date_changement'], name='authentific_courrie_idx'),
        ),
        migrations.AddIndex(
            model_name='historiquemotdepasse',
            index=models.Index(fields=['numero_telephone', '-date_changement'], name='authentific_numero__idx'),
        ),
        migrations.AddIndex(
            model_name='historiquemotdepasse',
            index=models.Index(fields=['type_changement'], name='authentific_type_ch_idx'),
        ),
        migrations.AddIndex(
            model_name='codeconfirmationsms',
            index=models.Index(fields=['numero_telephone', 'statut', '-date_creation'], name='authentific_numero__idx2'),
        ),
        migrations.AddIndex(
            model_name='codeconfirmationsms',
            index=models.Index(fields=['code', 'statut'], name='authentific_code_idx'),
        ),
        migrations.AddIndex(
            model_name='codeconfirmationsms',
            index=models.Index(fields=['utilisateur_id', '-date_creation'], name='authentific_utilisa_idx2'),
        ),
        migrations.AddIndex(
            model_name='codeconfirmationsms',
            index=models.Index(fields=['date_expiration', 'statut'], name='authentific_date_ex_idx'),
        ),
    ]
