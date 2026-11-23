
-- QUERY 1: Numero totale delle richieste
SELECT COUNT(*) AS numero_richieste
FROM fat_richieste;


-- QUERY 2: Incassi totali delle richieste completate
SELECT ROUND(SUM(incasso_euro), 2) AS incassi_totali
FROM fat_richieste
WHERE stato = 'Completata';


-- QUERY 3: Tempo medio di erogazione del servizio
SELECT ROUND(AVG(durata_minuti), 1) AS tempo_medio_minuti
FROM fat_richieste
WHERE stato = 'Completata';


-- QUERY 4: Percentuale di clienti abituali
-- Si considerano i clienti con almeno una richiesta completata.
-- Un cliente è abituale se ha almeno due richieste completate.

WITH richieste_per_cliente AS (
    SELECT
        id_cliente,
        COUNT(*) AS numero_richieste
    FROM fat_richieste
    WHERE stato = 'Completata'
    GROUP BY id_cliente
)
SELECT
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN numero_richieste >= 2 THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        1
    ) AS percentuale_clienti_abituali
FROM richieste_per_cliente;
