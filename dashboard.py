
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# Configurazione della pagina
st.set_page_config(
    page_title="Dashboard Startup On-Demand",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard - Startup di servizi On-Demand")
st.caption("Analisi dei dati della startup tramite Data Warehouse")

# Connessione al database
DATABASE = "database/data_warehouse.db"




@st.cache_data
def carica_dati():
    conn = sqlite3.connect(DATABASE)

    query = """
        SELECT
            r.id_richiesta,
            r.id_cliente,
            c.nome_cliente,
            f.categoria AS categoria_servizio,
            f.nome_fornitore,
            r.data_richiesta,
            a.nome_area AS area_geografica,
            r.stato,
            r.durata_minuti,
            r.incasso_euro
        FROM fat_richieste AS r
                LEFT JOIN dim_clienti AS c
            ON r.id_cliente = c.id_cliente
        LEFT JOIN dim_fornitori AS f
            ON r.id_fornitore = f.id_fornitore
        LEFT JOIN dim_aree AS a
            ON r.id_area = a.id_area
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    df["data_richiesta"] = pd.to_datetime(df["data_richiesta"])

    return df



df = carica_dati()

if df.empty:
    st.warning("Non ci sono dati nel database. Esegui prima python etl.py.")
    st.stop()

# Filtri laterali
st.sidebar.header("Filtri")

aree = ["Nord", "Centro", "Sud"]
aree_scelte = st.sidebar.multiselect(
    "Area geografica",
    options=aree,
    default=aree
)
# Filtro per categoria di servizio
categorie = ["Pulizie", "Consegne", "Assistenza"]

categorie_scelte = st.sidebar.multiselect(
    "Categoria del servizio",
    options=categorie,
    default=categorie
)
data_min = df["data_richiesta"].min().date()
data_max = df["data_richiesta"].max().date()


intervallo_date = st.sidebar.date_input(
    "Periodo (GG/MM/AAAA)",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
    format="DD/MM/YYYY"
)


filtrato = df[
    df["area_geografica"].isin(aree_scelte)
    & df["categoria_servizio"].isin(categorie_scelte)
].copy()

if isinstance(intervallo_date, (tuple, list)) and len(intervallo_date) == 2:
    inizio, fine = intervallo_date
    filtrato = filtrato[
        filtrato["data_richiesta"].dt.date.between(inizio, fine)
    ]

# Indicatori principali
completate = filtrato[filtrato["stato"] == "Completata"]
numero_richieste = len(filtrato)
tempo_medio = completate["durata_minuti"].mean()
incasso_totale = completate["incasso_euro"].sum()
clienti_per_richieste = (
    completate.groupby("id_cliente")["id_richiesta"].nunique()
)

clienti_abituali = int((clienti_per_richieste >= 2).sum())
clienti_totali = len(clienti_per_richieste)

percentuale_abituali = (
    clienti_abituali / clienti_totali * 100
    if clienti_totali > 0 else 0
)




col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Richieste totali", f"{numero_richieste}")
col2.metric(
    "Tempo medio servizio",
    f"{tempo_medio:.1f} min" if pd.notna(tempo_medio) else "N/D"
)
col3.metric("Incassi totali", f"€ {incasso_totale:,.2f}")
col4.metric("Clienti abituali", f"{percentuale_abituali:.1f}%")
col4.caption(
    f"{clienti_abituali} su {clienti_totali} clienti "
    "con almeno una richiesta completata"
)
# Numero di clienti attivi nel periodo selezionato
clienti_attivi = filtrato["id_cliente"].nunique()

col5.metric("Clienti attivi", f"{clienti_attivi}")
st.divider()

# Grafici

sinistra, destra = st.columns(2)


with sinistra:
    st.subheader("Richieste per stato")

    richieste_stato = (
        filtrato["stato"]
        .value_counts()
        .reindex(
            ["Completata", "Annullata", "In corso"],
            fill_value=0
        )
        .reset_index()
    )

    richieste_stato.columns = [
        "Stato",
        "Numero richieste"
    ]

    grafico_stato = alt.Chart(richieste_stato).mark_bar().encode(
        y=alt.Y(
            "Stato:N",
            title=None,
            sort=["Completata", "Annullata", "In corso"]
        ),
        x=alt.X(
            "Numero richieste:Q",
            title="Numero di richieste"
        ),
        tooltip=[
            alt.Tooltip("Stato:N", title="Stato"),
            alt.Tooltip(
                "Numero richieste:Q",
                title="Numero di richieste"
            )
        ]
    ).properties(
        height=250
    )

    st.altair_chart(
        grafico_stato,
        use_container_width=True
    )


with destra:
    st.subheader("Incassi per area geografica")

    incassi_area = (
        completate.groupby("area_geografica")["incasso_euro"]
        .sum()
        .reindex(["Nord", "Centro", "Sud"])
        .reset_index()
    )

    grafico_incassi = alt.Chart(incassi_area).mark_bar().encode(
        x=alt.X(
            "area_geografica:N",
            title="Area geografica",
            sort=["Nord", "Centro", "Sud"]
        ),
        y=alt.Y("incasso_euro:Q", title="Incassi (€)")
    )

    st.altair_chart(grafico_incassi, use_container_width=True)




# Grafico dei 5 fornitori con maggiori incassi
st.subheader("Top 5 fornitori per incassi")

top_fornitori = (
    completate.groupby("nome_fornitore")["incasso_euro"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

grafico_fornitori = alt.Chart(top_fornitori).mark_bar().encode(
    x=alt.X(
        "incasso_euro:Q",
        title="Incassi (€)"
    ),
    y=alt.Y(
        "nome_fornitore:N",
        title="Fornitore",
        sort="-x"
    ),
    tooltip=[
        alt.Tooltip("nome_fornitore:N", title="Fornitore"),
        alt.Tooltip(
            "incasso_euro:Q",
            title="Incassi (€)",
            format=",.2f"
        )
    ]
).properties(
    height=250
)

st.altair_chart(grafico_fornitori, use_container_width=True)

# Grafico delle richieste per categoria di servizio
st.subheader("Richieste per categoria di servizio")

richieste_categoria = (
    filtrato.groupby("categoria_servizio")
    .size()
    .reindex(
        ["Pulizie", "Consegne", "Assistenza"],
        fill_value=0
    )
    .reset_index(name="numero_richieste")
)

grafico_categorie = alt.Chart(richieste_categoria).mark_bar().encode(
    x=alt.X(
        "categoria_servizio:N",
        title="Categoria del servizio",
        sort=["Pulizie", "Consegne", "Assistenza"],
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y(
        "numero_richieste:Q",
        title="Numero di richieste"
    ),
    tooltip=[
        alt.Tooltip(
            "categoria_servizio:N",
            title="Categoria"
        ),
        alt.Tooltip(
            "numero_richieste:Q",
            title="Numero di richieste"
        )
    ]
).properties(
    height=250
)

st.altair_chart(
    grafico_categorie,
    use_container_width=True
)

st.subheader("Andamento delle richieste nel tempo")

# Raggruppa le richieste per mese
andamento = (
    filtrato.groupby(filtrato["data_richiesta"].dt.to_period("M"))
    .size()
    .rename("Numero richieste")
)

# Nomi dei mesi in italiano
mesi_italiani = {
    1: "Gennaio",
    2: "Febbraio",
    3: "Marzo",
    4: "Aprile",
    5: "Maggio",
    6: "Giugno",
    7: "Luglio",
    8: "Agosto",
    9: "Settembre",
    10: "Ottobre",
    11: "Novembre",
    12: "Dicembre"
}

# Visualizza i mesi in italiano
andamento.index = [
    f"{mesi_italiani[data.month]} {data.year}"
    for data in andamento.index
]

andamento_df = andamento.rename_axis("Mese").reset_index()
# Mantiene i mesi in ordine cronologico
ordine_mesi = [
    f"{mesi_italiani[mese]} {anno}"
    for anno, mese in sorted({
        (periodo.year, periodo.month)
        for periodo in filtrato["data_richiesta"].dt.to_period("M")
    })
]

andamento_df["Mese"] = pd.Categorical(
    andamento_df["Mese"],
    categories=ordine_mesi,
    ordered=True
)

andamento_df = andamento_df.sort_values("Mese")

grafico_andamento = alt.Chart(andamento_df).mark_line(
    point=True
).encode(
    x=alt.X(
        "Mese:N",
        title="Mese",
        sort=ordine_mesi
    ),
    y=alt.Y(
        "Numero richieste:Q",
        title="Numero di richieste"
    ),
    tooltip=[
        alt.Tooltip("Mese:N", title="Mese"),
        alt.Tooltip(
            "Numero richieste:Q",
            title="Numero di richieste"
        )
    ]
).properties(height=300)

st.altair_chart(grafico_andamento, use_container_width=True)


st.subheader("Dati delle richieste")

filtrato = filtrato.sort_values(
    by=["data_richiesta", "id_richiesta"],
    ascending=[True, True]
).copy()

filtrato["numero_visualizzato"] = range(1, len(filtrato) + 1)

filtrato = filtrato.sort_values(
    by=["data_richiesta", "id_richiesta"],
    ascending=[False, False]
).copy()

tabella = filtrato[
    [
        "numero_visualizzato",
        "nome_cliente",
        "data_richiesta",
        "area_geografica",
        "stato",
        "durata_minuti",
        "incasso_euro"
    ]
].copy()
tabella["nome_cliente"] = tabella["nome_cliente"].str.replace("_", " ", regex=False)

tabella["data_richiesta"] = pd.to_datetime(
    tabella["data_richiesta"]
).dt.strftime("%d/%m/%Y")

tabella["incasso_euro"] = tabella["incasso_euro"].apply(
    lambda x: f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    if pd.notna(x) else "Nessuna"
)

tabella = tabella.rename(columns={
    "numero_visualizzato": "N° richiesta",
    "nome_cliente": "Cliente",
    "data_richiesta": "Data Richiesta",
    "area_geografica": "Area Geografica",
    "stato": "Stato",
    "durata_minuti": "Durata (minuti)",
    "incasso_euro": "Incasso (euro)"
})
# Visualizza le durate come numeri interi
tabella["Durata (minuti)"] = tabella["Durata (minuti)"].apply(
    lambda x: str(int(x)) if pd.notna(x) else "Nessuna"
)
tabella = tabella.fillna("Nessuna")

st.dataframe(
    tabella,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Prototipo dimostrativo con dati sintetici e fittizi, "
    "creati esclusivamente a scopo didattico."
)
