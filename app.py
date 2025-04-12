import streamlit as st
import re
import math

# -----------------------------
# Funzioni per calcolo prezzi
# -----------------------------
def arrotonda_intero_con_00(valore: float) -> str:
    intero = int(math.floor(valore + 0.5))
    return f"{intero},00"

def arrotonda_intero_senza_00(valore: float) -> str:
    intero = int(math.floor(valore + 0.5))
    return f"{intero}"

def arrotonda_due_decimali(valore: float) -> str:
    dec = math.floor(valore * 100 + 0.5) / 100
    return f"{dec:.2f}".replace('.', ',')

def elabora_prezzo(match, percentuale: float, formato: str) -> str:
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
    pattern = re.compile(r"€\s*[0-9\s]+[.,][0-9]{2}")
    return pattern.sub(lambda m: elabora_prezzo(m, percentuale, formato), testo)

# ------------------------------------------------
# Configurazione pagina e layout
# ------------------------------------------------
st.set_page_config(
    page_title="Strumento Online di Variazione dei Prezzi",
    page_icon="💶",
    layout="centered"
)

# ------------------------------------------------
# CSS personalizzato per un look più colorato
# ------------------------------------------------
st.markdown("""
<style>
/* Sfondo a gradiente multi-colore */
body {
    background: linear-gradient(130deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%) !important;
    color: #e0e0e0 !important;
    font-family: "Segoe UI", sans-serif !important;
}

/* Card container dei vari elementi */
main .block-container {
    max-width: 750px !important;
    padding: 2rem !important;
    background-color: rgba(0, 0, 0, 0.4) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 20px rgba(0,0,0,0.3) !important;
}

/* Titoli */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Sottotitoli e testo */
p, div, label {
    color: #eeeeee !important;
}

/* Pulsanti generici */
button, .stButton button {
    background-color: #1EB980 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    margin: 0.3rem !important;
}
button:hover, .stButton button:hover {
    background-color: #17a07a !important;
    border: none !important;
}

/* File Uploader e spazi */
.stFileUploader {
    background-color: rgba(255,255,255,0.1) !important;
    border: 1px solid #ffffff44 !important;
    border-radius: 8px !important;
}

/* Aree di testo e input scuri */
textarea, .stTextArea, .stTextInput, .stNumberInput input {
    background-color: #242424 !important;
    color: #fefefe !important;
    border: 1px solid #e6e6e6 !important;
    border-radius: 6px !important;
}

/* Radio e label */
.stRadio > label, .stRadio div[data-baseweb="radio"] > div {
    color: #fff !important;
    font-weight: 500 !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Titolo e descrizione
# ------------------------------------------------
st.title("🎨 Strumento Online di Variazione dei Prezzi (Ultra Color Edition)")
st.markdown("""
Benvenuto! Carica un **file di testo** (che contenga prezzi nel formato "€ 577,00") o **incolla manualmente** il testo nel riquadro apposito.  
Imposta la **variazione percentuale** (anche negativa, es. -5) e **seleziona il formato** di arrotondamento. Quindi, **clicca** su "Applica Variazione" per vedere il risultato.
""")

# ------------------------------------------------
# Layout: file uploader e testo incollato
# ------------------------------------------------
st.subheader("1. Carica File di Testo oppure incolla manualmente")
col1, col2 = st.columns(2)

with col1:
    file_txt = st.file_uploader("Scegli un file .txt", type=["txt"])

with col2:
    testo_incollato = st.text_area("Oppure incolla qui il testo:", height=200)

testo_originale = ""
if file_txt is not None:
    testo_originale = file_txt.read().decode("utf-8", errors="ignore")
elif testo_incollato.strip():
    testo_originale = testo_incollato

# ------------------------------------------------
# Parametri di variazione
# ------------------------------------------------
st.subheader("2. Imposta la Variazione e Formato")
percentuale = st.number_input("Variazione Percentuale (%)", value=2.0, step=0.1, format="%.2f")

formato_opzioni = ["Intero con ,00", "Intero senza ,00", "Due decimali"]
formato = st.radio("Seleziona Formato Prezzo:", formato_opzioni)

# ------------------------------------------------
# Applica la modifica
# ------------------------------------------------
st.subheader("3. Applica e Visualizza il Risultato")
if st.button("⚡ Applica Variazione"):
    if not testo_originale.strip():
        st.error("Non hai fornito alcun testo da elaborare. Carica un file o incolla manualmente!")
    else:
        testo_modificato = applica_percentuale_testo(testo_originale, percentuale, formato)
        st.success("Ecco il testo modificato:")
        st.text_area("Risultato:", value=testo_modificato, height=300)

st.markdown("<hr style='border-top: 2px solid #fff; margin: 2rem 0;'/>", unsafe_allow_html=True)
st.info("© 2023 - Demo con tema multicolore. Realizzato con ❤️ e Streamlit.")
