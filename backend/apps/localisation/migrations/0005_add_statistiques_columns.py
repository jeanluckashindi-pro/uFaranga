# Generated manually on 2026-02-20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localisation', '0004_numerotelephone_limitenumerosparpays_and_more'),
    ]

    operations = [
        # Pays
        migrations.AddField(
            model_name='pays',
            name='nombre_agents',
            field=models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce pays'),
        ),
        migrations.AddField(
            model_name='pays',
            name='nombre_utilisateurs',
            field=models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce pays'),
        ),
        migrations.AddField(
            model_name='pays',
            name='nombre_agents_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce pays'),
        ),
        migrations.AddField(
            model_name='pays',
            name='nombre_utilisateurs_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce pays'),
        ),
        
        # Province
        migrations.AddField(
            model_name='province',
            name='nombre_agents',
            field=models.IntegerField(default=0, help_text='Nombre total d\'agents dans cette province'),
        ),
        migrations.AddField(
            model_name='province',
            name='nombre_utilisateurs',
            field=models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans cette province'),
        ),
        migrations.AddField(
            model_name='province',
            name='nombre_agents_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans cette province'),
        ),
        migrations.AddField(
            model_name='province',
            name='nombre_utilisateurs_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans cette province'),
        ),
        
        # District
        migrations.AddField(
            model_name='district',
            name='nombre_agents',
            field=models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce district'),
        ),
        migrations.AddField(
            model_name='district',
            name='nombre_utilisateurs',
            field=models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce district'),
        ),
        migrations.AddField(
            model_name='district',
            name='nombre_agents_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce district'),
        ),
        migrations.AddField(
            model_name='district',
            name='nombre_utilisateurs_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce district'),
        ),
        
        # Quartier
        migrations.AddField(
            model_name='quartier',
            name='nombre_agents',
            field=models.IntegerField(default=0, help_text='Nombre total d\'agents dans ce quartier'),
        ),
        migrations.AddField(
            model_name='quartier',
            name='nombre_utilisateurs',
            field=models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs dans ce quartier'),
        ),
        migrations.AddField(
            model_name='quartier',
            name='nombre_agents_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'agents actifs dans ce quartier'),
        ),
        migrations.AddField(
            model_name='quartier',
            name='nombre_utilisateurs_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs dans ce quartier'),
        ),
        
        # PointDeService
        migrations.AddField(
            model_name='pointdeservice',
            name='nombre_agents',
            field=models.IntegerField(default=0, help_text='Nombre total d\'agents à ce point de service'),
        ),
        migrations.AddField(
            model_name='pointdeservice',
            name='nombre_utilisateurs',
            field=models.IntegerField(default=0, help_text='Nombre total d\'utilisateurs à ce point de service'),
        ),
        migrations.AddField(
            model_name='pointdeservice',
            name='nombre_agents_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'agents actifs à ce point de service'),
        ),
        migrations.AddField(
            model_name='pointdeservice',
            name='nombre_utilisateurs_actifs',
            field=models.IntegerField(default=0, help_text='Nombre d\'utilisateurs actifs à ce point de service'),
        ),
    ]
