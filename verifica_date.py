
import sqlite3

DATABASE = "database/data_warehouse.db"

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

print("=== CONTROLLO DATE CLIENTI ===")

cur.execute("""
    SELECT
        r.id_richiesta,
        c.nome_cliente,
        c.data_registrazione,
        r.data_richiesta
    FROM fat_richieste r
    JOIN dim_clienti c
        ON r.id_cliente = c.id_cliente
    WHERE date(r.data_richiesta) < date(c.data_registrazione)
    ORDER BY r.data_richiesta
""")

anomalie = cur.fetchall()

print(f"Richieste precedenti alla registrazione: {len(anomalie)}")

if anomalie:
    print("\nEsempi di anomalie:")
    for richiesta in anomalie[:10]:
        id_richiesta, cliente, registrazione, data_richiesta = richiesta

        print(
            f"Richiesta {id_richiesta} - {cliente} - "
            f"Registrazione: {registrazione[8:10]}/{registrazione[5:7]}/{registrazione[:4]} - "
            f"Richiesta: {data_richiesta[8:10]}/{data_richiesta[5:7]}/{data_richiesta[:4]}"
        )
else:
    print("Nessuna anomalia rilevata!")

conn.close()

print("=== CONTROLLO TERMINATO ===")
