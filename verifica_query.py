
import sqlite3
from pathlib import Path

DATABASE = Path("database/data_warehouse.db")
FILE_SQL = Path("query_kpi.sql")

# Legge le quattro query SQL
testo_sql = FILE_SQL.read_text(encoding="utf-8-sig")

# Divide le query usando il punto e virgola
query = [
    q.strip()
    for q in testo_sql.split(";")
    if q.strip()
]

nomi = [
    "Numero totale richieste",
    "Incassi totali (€)",
    "Tempo medio servizio (minuti)",
    "Percentuale clienti abituali (%)"
]

# Connessione al database
conn = sqlite3.connect(DATABASE)

try:
    for nome, istruzione in zip(nomi, query):
        risultato = conn.execute(istruzione).fetchone()[0]
        print(f"{nome}: {risultato}")
finally:
    conn.close()
