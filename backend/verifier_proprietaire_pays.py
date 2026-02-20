#!/usr/bin/env python
"""
Vérifier le propriétaire de la table pays et donner les permissions
"""
import psycopg2

conn = psycopg2.connect(
    dbname='ufaranga',
    user='ufaranga',
    password='12345',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

print("="*60)
print("VÉRIFICATION PROPRIÉTAIRE TABLE PAYS")
print("="*60)

# Vérifier le propriétaire
cursor.execute("""
    SELECT 
        schemaname,
        tablename,
        tableowner
    FROM pg_tables
    WHERE schemaname = 'localisation'
    AND tablename = 'pays'
""")

result = cursor.fetchone()
if result:
    print(f"\nSchéma: {result[0]}")
    print(f"Table: {result[1]}")
    print(f"Propriétaire: {result[2]}")
else:
    print("\n✗ Table pays non trouvée")

# Vérifier les permissions de l'utilisateur ufaranga
cursor.execute("""
    SELECT 
        grantee,
        privilege_type
    FROM information_schema.table_privileges
    WHERE table_schema = 'localisation'
    AND table_name = 'pays'
    AND grantee = 'ufaranga'
""")

print("\nPermissions de l'utilisateur ufaranga:")
permissions = cursor.fetchall()
if permissions:
    for perm in permissions:
        print(f"  ✓ {perm[1]}")
else:
    print("  ✗ Aucune permission")

cursor.close()
conn.close()
