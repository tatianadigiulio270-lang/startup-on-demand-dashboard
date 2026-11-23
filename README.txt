# PROJECT WORK – DATA WAREHOUSE E BUSINESS INTELLIGENCE

## 1. Descrizione del progetto

Il progetto consiste nella realizzazione di un prototipo di Business Intelligence per una startup digitale che offre servizi on-demand, appartenenti alle categorie Pulizie, Consegne e Assistenza.

L'obiettivo è integrare in un unico archivio organizzato i dati provenienti da diverse fonti simulate: piattaforma di gestione delle richieste, applicazione clienti, sistema di gestione degli operatori e archivio dei fornitori.

Il sistema permette di analizzare l'andamento dell'attività aziendale attraverso indicatori, grafici e filtri interattivi.

Tutti i dati sono sintetici, inventati e utilizzati esclusivamente a scopo didattico.

## 2. Tecnologie utilizzate

- Python: generazione dei dati e procedura ETL.
- SQLite: gestione del Data Warehouse.
- SQL: interrogazioni e calcolo degli indicatori.
- Pandas: elaborazione e analisi dei dati.
- Streamlit: realizzazione della dashboard interattiva.
- Altair: realizzazione dei grafici.

## 3. Dataset sintetico

Il prototipo utilizza 1.200 record sintetici, suddivisi in:

- 300 clienti.
- 300 operatori.
- 300 fornitori.
- 300 richieste di servizio.

I dati vengono esportati in quattro file CSV separati, contenuti nella cartella `dati/`.

Il generatore utilizza `random.seed(42)` per rendere riproducibile la generazione.

Le richieste sono distribuite nel periodo dal 01/01/2026 al 31/10/2026, con maggiore frequenza in determinate fasce orarie e nei giorni di venerdì e sabato.

Sono simulate richieste completate, annullate e in corso, oltre a durate previste ed eventuali ritardi.

## 4. Struttura del progetto

- `genera_dati.py`: genera i dati sintetici e i file CSV.
- `crea_dw.py`: crea la struttura del Data Warehouse SQLite.
- `etl.py`: estrae, trasforma e carica i dati nel database.
- `dashboard.py`: realizza la dashboard interattiva.
- `query_kpi.sql`: contiene le interrogazioni SQL per gli indicatori principali.
- `verifica_query.py`: esegue le interrogazioni SQL e ne mostra i risultati.
- `README.txt`: contiene la descrizione e le istruzioni del progetto.
- `dati/`: contiene i quattro file CSV.
- `database/`: contiene il database SQLite.

## 5. Struttura del Data Warehouse

Il database utilizza uno schema a stella, composto da una tabella centrale dei fatti e cinque dimensioni.

Tabella centrale:

- `fat_richieste`: contiene gli identificativi delle richieste e i collegamenti alle dimensioni, oltre a data, ora, stato, durata prevista, ritardo, durata effettiva e incasso.

Tabelle dimensionali:

- `dim_clienti`: informazioni sui clienti.
- `dim_operatori`: informazioni sugli operatori.
- `dim_fornitori`: informazioni sui fornitori.
- `dim_data`: informazioni sulle date.
- `dim_aree`: informazioni sulle aree geografiche.

Le tabelle sono collegate attraverso chiavi primarie ed esterne.

## 6. Procedura ETL

La procedura ETL è composta da tre fasi:

**Estrazione:** lettura dei quattro file CSV.

**Trasformazione:** conversione degli identificativi e degli importi, normalizzazione di date e orari, gestione dei valori mancanti e associazione delle aree geografiche ai relativi identificativi.

**Caricamento:** inserimento dei dati nelle tabelle dimensionali e nella tabella dei fatti del Data Warehouse SQLite.

La procedura permette di ripetere il caricamento sostituendo i dati precedentemente presenti nelle tabelle.

## 7. Installazione ed esecuzione

È necessario avere Python installato sul computer.

Aprire un terminale nella cartella principale del progetto.

Installare le librerie necessarie:

`python -m pip install pandas streamlit altair`

Eseguire nell'ordine:

**1. Generazione dei dati sintetici**

`python genera_dati.py`

**2. Creazione del Data Warehouse**

`python crea_dw.py`

**3. Esecuzione dell'ETL**

`python etl.py`

**4. Verifica delle interrogazioni SQL**

`python verifica_query.py`

**5. Avvio della dashboard**

`python -m streamlit run dashboard.py`

La dashboard si apre nel browser e permette di esplorare i dati attraverso grafici e filtri.

**Nota:** il comando di creazione del Data Warehouse crea le tabelle mancanti, ma non modifica automaticamente la struttura di eventuali tabelle già esistenti. Per riprodurre il progetto da zero è consigliabile utilizzare una cartella di lavoro nuova oppure un database SQLite nuovo, conservando eventuali database precedenti.

## 8. Indicatori principali

La dashboard presenta cinque indicatori:

- Numero totale delle richieste.
- Incassi totali delle richieste completate.
- Tempo medio di erogazione dei servizi completati.
- Percentuale di clienti abituali.
- Numero di clienti attivi nel periodo selezionato.

I clienti abituali sono definiti come clienti che hanno effettuato almeno due richieste completate, rispetto ai clienti con almeno una richiesta completata.

I clienti attivi sono i clienti distinti che hanno effettuato almeno una richiesta nel periodo selezionato, indipendentemente dallo stato.

## 9. Grafici e filtri

La dashboard comprende:

- Richieste per stato.
- Incassi per area geografica.
- Classifica dei cinque fornitori con maggiori incassi.
- Distribuzione delle richieste per categoria di servizio.
- Andamento mensile delle richieste.
- Tabella dettagliata delle richieste.

Sono disponibili filtri interattivi per:

- Periodo temporale.
- Area geografica: Nord, Centro e Sud.
- Categoria di servizio: Pulizie, Consegne e Assistenza.

Gli indicatori e i grafici si aggiornano in base ai filtri selezionati.

## 10. Interrogazioni SQL

Il file `query_kpi.sql` contiene quattro interrogazioni per calcolare:

1. Numero totale delle richieste.
2. Incassi totali delle richieste completate.
3. Tempo medio di erogazione dei servizi completati.
4. Percentuale di clienti abituali.

Le interrogazioni vengono eseguite attraverso `verifica_query.py` e utilizzano i dati del Data Warehouse SQLite.

## 11. Risultati del prototipo

Con tutti i filtri selezionati, il prototipo ha restituito:

- Richieste totali: 300.
- Incassi complessivi: 19.183,98 €.
- Tempo medio di erogazione: 72,4 minuti.
- Clienti abituali: 36,2%.

Il numero dei clienti attivi viene calcolato dalla dashboard come numero di clienti distinti che hanno effettuato almeno una richiesta nel periodo selezionato.

I quattro indicatori sono stati calcolati attraverso interrogazioni SQL eseguite sul Data Warehouse SQLite dopo la rigenerazione dei dati.

- Clienti attivi: 170.

I clienti attivi sono i clienti distinti che hanno effettuato almeno una richiesta nel periodo considerato, indipendentemente dallo stato della richiesta.

## 12. Limiti e possibili miglioramenti

Il prototipo presenta alcune limitazioni:

- Utilizzo di dati sintetici anziché reali.
- Assenza di un collegamento automatico ai sistemi operativi di una startup.
- Caricamento completo dei dati anziché aggiornamento incrementale.
- Assenza di gestione storica delle modifiche nelle dimensioni.
- Controlli sulla qualità dei dati limitati.

Possibili miglioramenti futuri includono l'integrazione con fonti reali, controlli automatici sulla qualità, aggiornamenti incrementali e gestione dello storico delle dimensioni.

## 13. Finalità del progetto

Il progetto è un prototipo dimostrativo e riproducibile, sviluppato esclusivamente a scopo didattico, per mostrare come integrare dati provenienti da fonti differenti e trasformarli in informazioni utili alle decisioni aziendali attraverso un Data Warehouse e una dashboard di Business Intelligence.## 14. Verifica della qualità dei dati

È stato realizzato lo script `verifica_dati.py` per controllare la coerenza del Data Warehouse.

Lo script verifica:
- Il numero di record nelle quattro tabelle principali.
- L'integrità delle chiavi esterne.
- La compatibilità tra le categorie degli operatori e dei fornitori.
- L'assenza di richieste completate senza durata.
- L'assenza di richieste annullate con incasso positivo.

La verifica ha restituito 300 record per ciascuna delle quattro tabelle principali e zero anomalie nei controlli effettuati.

Per eseguire la verifica:

`python verifica_dati.py`

I risultati confermano la coerenza dei dati rispetto ai vincoli verificati nel prototipo.