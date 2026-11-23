
import sqlite3

DATABASE = "database/data_warehouse.db"

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

print("=== VERIFICA DATA WAREHOUSE ===")

# Controllo numero di record
tabelle = [
    "dim_clienti",
    "dim_operatori",
    "dim_fornitori",
    "fat_richieste"
]

for tabella in tabelle:
    cur.execute(f"SELECT COUNT(*) FROM {tabella}")
    print(f"{tabella}: {cur.fetchone()[0]} record")

# Controllo chiavi esterne
cur.execute("PRAGMA foreign_key_check")
errori = cur.fetchall()

print(f"Errori nelle chiavi esterne: {len(errori)}")

# Controllo categorie tra operatori e fornitori
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste r
    JOIN dim_operatori o
        ON r.id_operatore = o.id_operatore
    JOIN dim_fornitori f
        ON r.id_fornitore = f.id_fornitore
    WHERE o.tipo_attivita != f.categoria
""")

print(f"Operatori e fornitori incompatibili: {cur.fetchone()[0]}")

# Controllo richieste completate senza durata
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste
    WHERE stato = 'Completata'
      AND durata_minuti IS NULL
""")

print(f"Richieste completate senza durata: {cur.fetchone()[0]}")

# Controllo richieste annullate con incasso
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste
    WHERE stato = 'Annullata'
      AND incasso_euro > 0
""")

print(f"Richieste annullate con incasso: {cur.fetchone()[0]}")

conn.close()

print("=== VERIFICA TERMINATA ===")
