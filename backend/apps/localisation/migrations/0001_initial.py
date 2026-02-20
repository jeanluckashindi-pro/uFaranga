# Migration initiale - Les tables existent déjà en base de données PostgreSQL
# Cette migration définit les modèles pour Django mais sera appliquée avec --fake

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code_iso_2', models.CharField(db_index=True, max_length=2, unique=True)),
                ('code_iso_3', models.CharField(blank=True, max_length=3)),
                ('nom', models.CharField(max_length=100)),
                ('nom_anglais', models.CharField(blank=True, max_length=100)),
                ('continent', models.CharField(blank=True, db_index=True, help_text='Continent du pays (ex: Afrique, Europe, Asie)', max_length=50, null=True)),
                ('sous_region', models.CharField(blank=True, db_index=True, help_text="Sous-région géographique (ex: Afrique de l'Est, Afrique Centrale)", max_length=100, null=True)),
                ('latitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('nombre_agents', models.IntegerField(default=0, help_text="Nombre total d'agents dans ce pays")),
                ('nombre_utilisateurs', models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce pays')),
                ('nombre_agents_actifs', models.IntegerField(default=0, help_text="Nombre d'agents actifs dans ce pays")),
                ('nombre_utilisateurs_actifs', models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce pays')),
                ('autorise_systeme', models.BooleanField(default=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Pays',
                'verbose_name_plural': 'Pays',
                'db_table': 'localisation"."pays',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('nom', models.CharField(max_length=100)),
                ('latitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('nombre_agents', models.IntegerField(default=0, help_text="Nombre total d'agents dans cette province")),
                ('nombre_utilisateurs', models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans cette province')),
                ('nombre_agents_actifs', models.IntegerField(default=0, help_text="Nombre d'agents actifs dans cette province")),
                ('nombre_utilisateurs_actifs', models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans cette province')),
                ('autorise_systeme', models.BooleanField(default=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
                ('pays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provinces', to='localisation.pays')),
            ],
            options={
                'verbose_name': 'Province / Région',
                'verbose_name_plural': 'Provinces / Régions',
                'db_table': 'localisation"."provinces',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('nom', models.CharField(max_length=100)),
                ('latitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('nombre_agents', models.IntegerField(default=0, help_text="Nombre total d'agents dans ce district")),
                ('nombre_utilisateurs', models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce district')),
                ('nombre_agents_actifs', models.IntegerField(default=0, help_text="Nombre d'agents actifs dans ce district")),
                ('nombre_utilisateurs_actifs', models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce district')),
                ('autorise_systeme', models.BooleanField(default=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='localisation.province')),
            ],
            options={
                'verbose_name': 'District / Ville',
                'verbose_name_plural': 'Districts / Villes',
                'db_table': 'localisation"."districts',
            },
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('nom', models.CharField(max_length=100)),
                ('latitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude_centre', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('nombre_agents', models.IntegerField(default=0, help_text="Nombre total d'agents dans ce quartier")),
                ('nombre_utilisateurs', models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce quartier')),
                ('nombre_agents_actifs', models.IntegerField(default=0, help_text="Nombre d'agents actifs dans ce quartier")),
                ('nombre_utilisateurs_actifs', models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce quartier')),
                ('autorise_systeme', models.BooleanField(default=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quartiers', to='localisation.district')),
            ],
            options={
                'verbose_name': 'Quartier / Zone',
                'verbose_name_plural': 'Quartiers / Zones',
                'db_table': 'localisation"."quartiers',
            },
        ),
        migrations.CreateModel(
            name='PointDeService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
                ('nom', models.CharField(max_length=100)),
                ('type_point', models.CharField(choices=[('AGENT', 'Agent'), ('GUICHET', 'Guichet'), ('PARTENAIRE', 'Partenaire'), ('AUTRE', 'Autre')], default='AGENT', max_length=20)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('adresse_complementaire', models.TextField(blank=True)),
                ('nombre_agents', models.IntegerField(default=0, help_text="Nombre total d'agents à ce point de service")),
                ('nombre_utilisateurs', models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs à ce point de service')),
                ('nombre_agents_actifs', models.IntegerField(default=0, help_text="Nombre d'agents actifs à ce point de service")),
                ('nombre_utilisateurs_actifs', models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs à ce point de service')),
                ('autorise_systeme', models.BooleanField(default=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('metadonnees', models.JSONField(blank=True, default=dict)),
                ('agent_utilisateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='points_de_service_agent', to='identite.utilisateur')),
                ('quartier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points_de_service', to='localisation.quartier')),
            ],
            options={
                'verbose_name': 'Point de service / Agent',
                'verbose_name_plural': 'Points de service / Agents',
                'db_table': 'localisation"."points_de_service',
            },
        ),
        migrations.AddIndex(
            model_name='pays',
            index=models.Index(fields=['continent'], name='pays_contine_f2ca79_idx'),
        ),
        migrations.AddIndex(
            model_name='pays',
            index=models.Index(fields=['sous_region'], name='pays_sous_re_a6efd2_idx'),
        ),
        migrations.AddIndex(
            model_name='pays',
            index=models.Index(fields=['code_iso_2'], name='pays_code_is_bf11fe_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='province',
            unique_together={('pays', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together={('province', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='quartier',
            unique_together={('district', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='pointdeservice',
            unique_together={('quartier', 'code')},
        ),
    ]
