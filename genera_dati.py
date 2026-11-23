
import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

# Rende i dati riproducibili
random.seed(42)

# Cartella dei dati
CARTELLA_DATI = Path("dati")
CARTELLA_DATI.mkdir(exist_ok=True)

# Numero di record per tipologia
NUM_RECORD = 300

# 1. Clienti fittizi
clienti = []

zone_citta = {
    "Roma": "Centro",
    "Milano": "Nord",
    "Perugia": "Centro",
    "Napoli": "Sud"
}

for i in range(1, NUM_RECORD + 1):
    citta = random.choice(list(zone_citta.keys()))

    clienti.append({
        "id_cliente": i,
        "nome_cliente": f"Cliente {i}",
        "citta": citta,
        "area": zone_citta[citta],
        "data_registrazione": (
            f"2026-{random.randint(1, 9):02d}-01"
        )
    })

# 2. Operatori fittizi
operatori = [
    {
        "id_operatore": i,
        "nome_operatore": f"Operatore {i}",
        "area": random.choice(["Nord", "Centro", "Sud"]),
        "tipo_attivita": random.choice(
            ["Pulizie", "Consegne", "Assistenza"]
        )
    }
    for i in range(1, NUM_RECORD + 1)
]

# 3. Fornitori fittizi
fornitori = [
    {
        "id_fornitore": i,
        "nome_fornitore": f"Fornitore {i}",
        "categoria": random.choice(
            ["Pulizie", "Consegne", "Assistenza"]
        ),
        "area": random.choice(["Nord", "Centro", "Sud"])
    }
    for i in range(1, NUM_RECORD + 1)
]

# 4. Richieste di servizio fittizie
richieste = []

data_inizio = datetime(2026, 1, 1)
data_fine = datetime(2026, 10, 31)
giorni_disponibili = (data_fine - data_inizio).days

ore_frequenti = [9, 10, 11, 12, 17, 18, 19]

for i in range(1, NUM_RECORD + 1):

    # Venerdi e sabato hanno piu richieste
    while True:
        giorni_casuali = random.randint(
            0, giorni_disponibili
        )
        giorno_richiesta = data_inizio + timedelta(
            days=giorni_casuali
        )

        if giorno_richiesta.weekday() in [4, 5]:
            break

        if random.random() < 0.60:
            break

    # Fasce orarie piu frequenti
    if random.random() < 0.75:
        ora = random.choice(ore_frequenti)
    else:
        ora = random.randint(8, 21)

    minuto = random.randint(0, 59)

    data_ora = giorno_richiesta.replace(
        hour=ora,
        minute=minuto
    )

    data = data_ora.strftime("%Y-%m-%d")

    # Stato della richiesta
    stato = random.choices(
        ["Completata", "Annullata", "In corso"],
        weights=[75, 15, 10]
    )[0]

    # Durata e ritardi
    if stato == "Completata":
        durata_prevista = random.randint(15, 120)

        if random.random() < 0.20:
            ritardo = random.randint(5, 30)
        else:
            ritardo = 0

        durata = durata_prevista + ritardo
        incasso = round(random.uniform(20, 150), 2)

    else:
        durata_prevista = None
        ritardo = None
        durata = None
        incasso = 0

    # Fornitore e operatore della stessa categoria
    fornitore = random.choice(fornitori)

    operatori_compatibili = [
        op for op in operatori
        if op["tipo_attivita"] == fornitore["categoria"]
    ]

    operatore = random.choice(operatori_compatibili)

    # Seleziona soltanto clienti gia registrati
    clienti_disponibili = [
        cliente for cliente in clienti
        if cliente["data_registrazione"] <= data
    ]

    cliente_scelto = random.choice(clienti_disponibili)

    richieste.append({
        "id_richiesta": i,
        "id_cliente": cliente_scelto["id_cliente"],
        "id_operatore": operatore["id_operatore"],
        "id_fornitore": fornitore["id_fornitore"],
        "data_richiesta": data,
        "ora_richiesta": data_ora.strftime("%H:%M"),
        "area_geografica": operatore["area"],
        "stato": stato,
        "durata_prevista_minuti": durata_prevista,
        "ritardo_minuti": ritardo,
        "durata_minuti": durata,
        "incasso_euro": incasso
    })

# 5. Esportazione dei dati in CSV
archivi = {
    "clienti.csv": clienti,
    "operatori.csv": operatori,
    "fornitori.csv": fornitori,
    "richieste.csv": richieste
}

for nome_file, righe in archivi.items():
    with open(
        CARTELLA_DATI / nome_file,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        scrittore = csv.DictWriter(
            file,
            fieldnames=righe[0].keys()
        )

        scrittore.writeheader()
        scrittore.writerows(righe)

    print(f"Creato: {nome_file} ({len(righe)} record)")

print("Dati generati correttamente!")
print(f"Clienti: {len(clienti)}")
print(f"Operatori: {len(operatori)}")
print(f"Fornitori: {len(fornitori)}")
print(f"Richieste: {len(richieste)}")
print(f"File salvati nella cartella: {CARTELLA_DATI}")