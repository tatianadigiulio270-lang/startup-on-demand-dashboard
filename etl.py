
import csv
import sqlite3
from pathlib import Path
from datetime import datetime

CARTELLA_DATI = Path("dati")
DATABASE = Path("database/data_warehouse.db")


def leggi_csv(nome_file):
    """Legge i dati da un file CSV."""
    with open(
        CARTELLA_DATI / nome_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def esegui_etl():

    # E - ESTRAZIONE
    clienti = leggi_csv("clienti.csv")
    operatori = leggi_csv("operatori.csv")
    fornitori = leggi_csv("fornitori.csv")
    richieste = leggi_csv("richieste.csv")

    # T - TRASFORMAZIONE
    for r in clienti:
        r["id_cliente"] = int(r["id_cliente"])

    for r in operatori:
        r["id_operatore"] = int(r["id_operatore"])

    for r in fornitori:
        r["id_fornitore"] = int(r["id_fornitore"])

    aree = {
        "Nord": 1,
        "Centro": 2,
        "Sud": 3
    }

    for r in richieste:
        r["id_richiesta"] = int(r["id_richiesta"])
        r["id_cliente"] = int(r["id_cliente"])
        r["id_operatore"] = int(r["id_operatore"])
        r["id_fornitore"] = int(r["id_fornitore"])

        r["incasso_euro"] = float(r["incasso_euro"])

        # Durata effettiva
        r["durata_minuti"] = (
            int(r["durata_minuti"])
            if r["durata_minuti"] else None
        )

        # Durata prevista
        r["durata_prevista_minuti"] = (
            int(r["durata_prevista_minuti"])
            if r["durata_prevista_minuti"] else None
        )

        # Ritardo
        r["ritardo_minuti"] = (
            int(r["ritardo_minuti"])
            if r["ritardo_minuti"] else None
        )

        # Normalizzazione della data
        data = datetime.strptime(
            r["data_richiesta"], "%Y-%m-%d"
        )
        r["data_richiesta"] = data.strftime("%Y-%m-%d")

        # Controllo e normalizzazione dell'orario
        ora = datetime.strptime(
            r["ora_richiesta"], "%H:%M"
        )
        r["ora_richiesta"] = ora.strftime("%H:%M")

        # Associazione dell'area geografica
        r["id_area"] = aree[r["area_geografica"]]

    # L - CARICAMENTO
    if not DATABASE.exists():
        raise FileNotFoundError(
            "Database non trovato. "
            "Creare prima il Data Warehouse."
        )

    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with conn:
            cur = conn.cursor()

            # Elimina i vecchi dati prima del caricamento
            cur.execute("DELETE FROM fat_richieste")
            cur.execute("DELETE FROM dim_data")
            cur.execute("DELETE FROM dim_aree")
            cur.execute("DELETE FROM dim_clienti")
            cur.execute("DELETE FROM dim_operatori")
            cur.execute("DELETE FROM dim_fornitori")

            # Caricamento clienti
            cur.executemany("""
                INSERT INTO dim_clienti (
                    id_cliente, nome_cliente,
                    citta, area, data_registrazione
                )
                VALUES (
                    :id_cliente, :nome_cliente,
                    :citta, :area, :data_registrazione
                )
            """, clienti)

            # Caricamento operatori
            cur.executemany("""
                INSERT INTO dim_operatori (
                    id_operatore, nome_operatore,
                    area, tipo_attivita
                )
                VALUES (
                    :id_operatore, :nome_operatore,
                    :area, :tipo_attivita
                )
            """, operatori)

            # Caricamento fornitori
            cur.executemany("""
                INSERT INTO dim_fornitori (
                    id_fornitore, nome_fornitore,
                    categoria, area
                )
                VALUES (
                    :id_fornitore, :nome_fornitore,
                    :categoria, :area
                )
            """, fornitori)

            # Caricamento aree geografiche
            cur.executemany("""
                INSERT INTO dim_aree (
                    id_area, nome_area
                )
                VALUES (?, ?)
            """, [
                (1, "Nord"),
                (2, "Centro"),
                (3, "Sud")
            ])

            # Caricamento dimensione tempo
            date_uniche = sorted({
                r["data_richiesta"]
                for r in richieste
            })

            for valore in date_uniche:
                data = datetime.strptime(
                    valore, "%Y-%m-%d"
                )

                cur.execute("""
                    INSERT INTO dim_data (
                        data, anno, mese, giorno
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    valore,
                    data.year,
                    data.month,
                    data.day
                ))

            # Caricamento richieste
            cur.executemany("""
                INSERT INTO fat_richieste (
                    id_richiesta,
                    id_cliente,
                    id_operatore,
                    id_fornitore,
                    data_richiesta,
                    ora_richiesta,
                    id_area,
                    stato,
                    durata_prevista_minuti,
                    ritardo_minuti,
                    durata_minuti,
                    incasso_euro
                )
                VALUES (
                    :id_richiesta,
                    :id_cliente,
                    :id_operatore,
                    :id_fornitore,
                    :data_richiesta,
                    :ora_richiesta,
                    :id_area,
                    :stato,
                    :durata_prevista_minuti,
                    :ritardo_minuti,
                    :durata_minuti,
                    :incasso_euro
                )
            """, richieste)

        print("ETL completato correttamente!")
        print(f"Clienti caricati: {len(clienti)}")
        print(f"Operatori caricati: {len(operatori)}")
        print(f"Fornitori caricati: {len(fornitori)}")
        print(f"Richieste caricate: {len(richieste)}")
        print(f"Date distinte: {len(date_uniche)}")

    finally:
        conn.close()


if __name__ == "__main__":
    esegui_etl()
