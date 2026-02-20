"""
Commande pour ajouter les Foreign Keys à la table utilisateurs
Usage: python manage.py ajouter_foreign_keys
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Ajoute les Foreign Keys à la table utilisateurs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Ajout des Foreign Keys...'))
        
        with connection.cursor() as cursor:
            try:
                # Supprimer les contraintes si elles existent
                self.stdout.write('  → Suppression des anciennes contraintes...')
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    DROP CONSTRAINT IF EXISTS utilisateurs_type_utilisateur_fkey CASCADE;
                """)
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    DROP CONSTRAINT IF EXISTS utilisateurs_niveau_kyc_fkey CASCADE;
                """)
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    DROP CONSTRAINT IF EXISTS utilisateurs_statut_fkey CASCADE;
                """)
                
                # Ajouter les Foreign Keys
                self.stdout.write('  → Ajout de la FK type_utilisateur...')
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    ADD CONSTRAINT utilisateurs_type_utilisateur_fkey 
                    FOREIGN KEY (type_utilisateur) 
                    REFERENCES identite.types_utilisateurs(code);
                """)
                
                self.stdout.write('  → Ajout de la FK niveau_kyc...')
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    ADD CONSTRAINT utilisateurs_niveau_kyc_fkey 
                    FOREIGN KEY (niveau_kyc) 
                    REFERENCES identite.niveaux_kyc(niveau);
                """)
                
                self.stdout.write('  → Ajout de la FK statut...')
                cursor.execute("""
                    ALTER TABLE identite.utilisateurs 
                    ADD CONSTRAINT utilisateurs_statut_fkey 
                    FOREIGN KEY (statut) 
                    REFERENCES identite.statuts_utilisateurs(code);
                """)
                
                # Créer les index
                self.stdout.write('  → Création des index...')
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_utilisateurs_type 
                    ON identite.utilisateurs(type_utilisateur);
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_utilisateurs_niveau_kyc 
                    ON identite.utilisateurs(niveau_kyc);
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_utilisateurs_statut 
                    ON identite.utilisateurs(statut);
                """)
                
                # Vérifier
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'FOREIGN KEY'
                      AND table_schema = 'identite'
                      AND table_name = 'utilisateurs'
                      AND constraint_name LIKE 'utilisateurs_%_fkey';
                """)
                count = cursor.fetchone()[0]
                
                self.stdout.write(self.style.SUCCESS(f'\n✓ Foreign Keys ajoutées avec succès!'))
                self.stdout.write(self.style.SUCCESS(f'✓ {count} Foreign Keys créées (3 attendues)'))
                
                if count == 3:
                    self.stdout.write(self.style.SUCCESS('\n🎉 Structure correcte! Vous pouvez redémarrer Django.'))
                else:
                    self.stdout.write(self.style.WARNING(f'\n⚠️ Seulement {count} Foreign Keys créées au lieu de 3'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'\n✗ Erreur: {str(e)}'))
                raise
