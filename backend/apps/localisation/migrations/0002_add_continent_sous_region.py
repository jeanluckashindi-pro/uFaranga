"""
Migration pour ajouter les colonnes continent et sous_region à la table pays
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localisation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pays',
            name='continent',
            field=models.CharField(
                max_length=50,
                blank=True,
                null=True,
                db_index=True,
                help_text='Continent du pays (ex: Afrique, Europe, Asie)'
            ),
        ),
        migrations.AddField(
            model_name='pays',
            name='sous_region',
            field=models.CharField(
                max_length=100,
                blank=True,
                null=True,
                db_index=True,
                help_text='Sous-région géographique (ex: Afrique de l\'Est, Afrique Centrale)'
            ),
        ),
    ]
