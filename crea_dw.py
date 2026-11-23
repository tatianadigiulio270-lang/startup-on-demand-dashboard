
import sqlite3
from pathlib import Path

# Crea la cartella del database
Path("database").mkdir(exist_ok=True)

# Apre il database SQLite
conn = sqlite3.connect("database/data_warehouse.db")
cur = conn.cursor()

# Attiva il controllo delle chiavi esterne
cur.execute("PRAGMA foreign_keys = ON")

# Dimensione clienti
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_clienti (
    id_cliente INTEGER PRIMARY KEY,
    nome_cliente TEXT,
    citta TEXT,
    area TEXT,
    data_registrazione TEXT
)
""")

# Dimensione operatori
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_operatori (
    id_operatore INTEGER PRIMARY KEY,
    nome_operatore TEXT,
    area TEXT,
    tipo_attivita TEXT
)
""")

# Dimensione fornitori
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_fornitori (
    id_fornitore INTEGER PRIMARY KEY,
    nome_fornitore TEXT,
    categoria TEXT,
    area TEXT
)
""")

# Dimensione tempo
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_data (
    data TEXT PRIMARY KEY,
    anno INTEGER,
    mese INTEGER,
    giorno INTEGER
)
""")

# Dimensione aree geografiche
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_aree (
    id_area INTEGER PRIMARY KEY,
    nome_area TEXT
)
""")

# Tabella centrale dei fatti
cur.execute("""
CREATE TABLE IF NOT EXISTS fat_richieste (
    id_richiesta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_operatore INTEGER,
    id_fornitore INTEGER,
    data_richiesta TEXT,
    ora_richiesta TEXT,
    id_area INTEGER,
    stato TEXT,
    durata_prevista_minuti INTEGER,
    ritardo_minuti INTEGER,
    durata_minuti INTEGER,
    incasso_euro REAL,

    FOREIGN KEY (id_cliente)
        REFERENCES dim_clienti(id_cliente),

    FOREIGN KEY (id_operatore)
        REFERENCES dim_operatori(id_operatore),

    FOREIGN KEY (id_fornitore)
        REFERENCES dim_fornitori(id_fornitore),

    FOREIGN KEY (data_richiesta)
        REFERENCES dim_data(data),

    FOREIGN KEY (id_area)
        REFERENCES dim_aree(id_area)
)
""")

conn.commit()
conn.close()

print("Data warehouse creato correttamente!")