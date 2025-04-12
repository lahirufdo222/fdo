import streamlit as st
import re
import math

# ----- Calcolo dei prezzi -----

def arrotonda_intero_con_00(valore: float) -> str:
    """Arrotonda all'intero e aggiunge ',00'."""
    intero = int(math.floor(valore + 0.5))
    return f"{intero},00"

def arrotonda_intero_senza_00(valore: float) -> str:
    """Arrotonda all'intero senza decimali."""
    intero = int(math.floor(valore + 0.5))
    return f"{intero}"

def arrotonda_due_decimali(valore: float) -> str:
    """Arrotonda a due decimali, con virgola."""
    dec = math.floor(valore * 100 + 0.5) / 100
    return f"{dec:.2f}".replace('.', ',')

def elabora_prezzo(match, percentuale: float, formato: str) -> str:
    """Converte un prezzo '€ 577,00' con la percentuale scelta, arrotondando."""
    testo_originale = match.group(0)
    prezzo_str = testo_originale.replace('€', '').strip().replace(' ', '')
    normalizzato = prezzo_str.replace(',', '.')
    try:
        prezzo_iniziale = float(normalizzato)
    except ValueError:
        return testo_originale

    nuovo_prezzo = prezzo_iniziale * (1 + percentuale / 100.0)
    if formato == "Intero con ,00":
        finale = arrotonda_intero_con_00(nuovo_prezzo)
    elif formato == "Intero senza ,00":
        finale = arrotonda_intero_senza_00(nuovo_prezzo)
    else:
        finale = arrotonda_due_decimali(nuovo_prezzo)

    return f"€ {finale}"

def applica_percentuale_testo(testo: str, percentuale: float, formato: str) -> str:
    """Applica la variazione ai prezzi '€ XXX,XX' o '€XXX.XX' all'interno del testo."""
    pattern = re.compile(r"€\s*[0-9\s]+[.,][0-9]{2}")
    return pattern.sub(lambda m: elabora_prezzo(m, percentuale, formato), testo)

# ----- Configurazione pagina e tema -----
st.set_page_config(
    page_title="Strumento Online di Variazione dei Prezzi",
    page_icon="💶",
    layout="centered"
)

# CSS personalizzato per tema scuro con accenti colorati
st.markdown("""
<style>
/* Sfondo scuro con gradiente */
body {
    background: linear-gradient(160deg, #14213d 0%, #1d2a4a 100%) !important;
    color: #e0e0e0 !important;
}
/* Colore principale (verde/blu) */
.btn-main-color {
    background-color: #18a999 !important;
    border-color: #18a999 !important;
    color: white !important;
    font-weight: bold !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 8px !important;
    margin: 0.3rem !important;
}
.btn-main-color:hover {
    background-color: #159c8c !important;
    border-color: #159c8c !important;
}

/* Titolo */
h1, h2, h3, h4 {
    color: #f4f4f4 !important;
}

/* Caselle di testo e aree di testo */
section > div:not(.element-container) > div.stTextArea, .stTextInput {
    background-color: #22314b !important;
    color: #ffffff !important;
    border: 1px solid #18a999 !important;
    border-radius: 6px !important;
}

/* Selettori radio, number input e file uploader */
.stRadio > label, .stNumberInput > label, .stFileUploader > label {
    color: #d2d2d2 !important;
    font-weight: 500 !important;
}
.stRadio div[data-baseweb="radio"] > div {
    color: #ffffff !important;
}
.css-19nf2c5.e1xhbmpj2 {  /* label di radio */
    color: #ffffff !important;
}
.css-eh5xgm { /* number input */
    background-color: #22314b !important;
    border: 1px solid #18a999 !important;
    color: #ffffff !important;
}
/* ComboBox / select (Streamlit < 1.23 non lo ha di default, 
   ma in st.radio puoi avere st.selectbox) */

/* Pulsanti (versioni base) */
.css-1cxtc89.e8zbici2 {
    background-color: #18a999 !important;
    border-color: #18a999 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
.css-1cxtc89.e8zbici2:hover {
    background-color: #159c8c !important;
    border-color: #159c8c !important;
}
/* TextArea scuro */
textarea {
    background-color: #1d2a4a !important;
    color: #ffffff !important;
    border: 1px solid #18a999 !important;
    border-radius: 6px !important;
}

/* Riduce la larghezza massima dei container per layout centrato */
main .block-container {
    max-width: 700px !important;
    margin: auto !important;
    padding-top: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ----- Titolo -----
st.title("💻 Strumento Online di Variazione dei Prezzi (Dark Edition)")

st.markdown("""
**Carica un file di testo** (da Desktop o altrove) che contiene prezzi in formato “€ 577,00”, 
oppure incolla il tuo testo manualmente.  
Poi imposta la **variazione percentuale** e scegli il **formato** desiderato.
""")

# ----- Scelta caricamento file / testo manuale -----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Carica File di Testo")
    file_txt = st.file_uploader("Seleziona un file .txt", type=["txt"])

with col2:
    st.subheader("Oppure incolla manualmente:")
    testo_incollato = st.text_area("Testo Originale", height=200)

# Determina il testo originale (o dal file o dall’area)
testo_originale = ""
if file_txt is not None:
    testo_originale = file_txt.read().decode("utf-8", errors="ignore")
elif testo_incollato.strip():
    testo_originale = testo_incollato

# ----- Configurazione parametri -----
st.subheader("Impostazioni di Variazione")

percentuale = st.number_input(
    "Variazione Percentuale (%)",
    value=2.0, step=0.1, format="%.2f"
)

formato_opzioni = ["Intero con ,00", "Intero senza ,00", "Due decimali"]
formato = st.radio("Formato Prezzo", formato_opzioni)

# ----- Applica variazione -----
if st.button("🚀 Applica Variazione", key="apply_button"):
    if not testo_originale.strip():
        st.error("Nessun testo da elaborare. Carica un file o incolla manualmente.")
    else:
        risultato = applica_percentuale_testo(testo_originale, percentuale, formato)
        st.subheader("Testo Modificato")
        st.text_area("Risultato:", value=risultato, height=300)

st.info("© 2023 - Esempio tool web con tema scuro, Streamlit e variazione prezzi.")
