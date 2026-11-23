
import sqlite3

conn = sqlite3.connect("database/data_warehouse.db")
cur = conn.cursor()

print("=== VERIFICA REALISMO DEI DATI ===")

# Richieste per stato
cur.execute("""
    SELECT stato, COUNT(*)
    FROM fat_richieste
    GROUP BY stato
""")

print("\nRichieste per stato:")
for stato, numero in cur.fetchall():
    print(f"{stato}: {numero}")

# Richieste completate con ritardo
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste
    WHERE stato = 'Completata'
      AND ritardo_minuti > 0
""")

print(f"\nRichieste con ritardo: {cur.fetchone()[0]}")

# Richieste nei giorni di venerdi e sabato
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste
    WHERE strftime('%w', data_richiesta) IN ('5', '6')
""")

print(f"Richieste di venerdi e sabato: {cur.fetchone()[0]}")

# Richieste nelle fasce orarie frequenti
cur.execute("""
    SELECT COUNT(*)
    FROM fat_richieste
    WHERE CAST(substr(ora_richiesta, 1, 2) AS INTEGER)
          IN (9, 10, 11, 12, 17, 18, 19)
""")

print(f"Richieste nelle fasce orarie frequenti: {cur.fetchone()[0]}")

conn.close()

print("\n=== VERIFICA TERMINATA ===")
