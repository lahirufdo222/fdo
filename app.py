import streamlit as st
import re
import math

# Funzioni di arrotondamento e formattazione
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
    prezzo_str = match.group(0).replace('€', '').strip().replace(' ', '')
    normalizzato = prezzo_str.replace(',', '.')
    try:
        prezzo_iniziale = float(normalizzato)
    except ValueError:
        return match.group(0)
    nuovo_prezzo = prezzo_iniziale * (1 + percentuale / 100.0)
    if formato == "Intero con ,00":
        risultato = arrotonda_intero_con_00(nuovo_prezzo)
    elif formato == "Intero senza ,00":
        risultato = arrotonda_intero_senza_00(nuovo_prezzo)
    else:
        risultato = arrotonda_due_decimali(nuovo_prezzo)
    return f"€ {risultato}"

def applica_percentuale_testo(testo: str, percentuale: float, formato: str) -> str:
    pattern = re.compile(r"€\s*[0-9\s]+[.,][0-9]{2}")
    return pattern.sub(lambda m: elabora_prezzo(m, percentuale, formato), testo)

# Configurazione pagina
st.set_page_config(page_title="Strumento Variazione Prezzi", page_icon="💶", layout="centered")

# Titolo principale
st.title("Strumento Variazione Prezzi")

# Input: testo contenente i prezzi
testo_originale = st.text_area("Testo", height=250)

# Input: variazione percentuale
percentuale = st.number_input("Percentuale (%)", value=2.0, step=0.1, format="%.2f")

# Input: formato di arrotondamento
formato = st.radio("Formato", ("Intero con ,00", "Intero senza ,00", "Due decimali"))

# Pulsante per applicare la variazione
if st.button("Applica"):
    if not testo_originale.strip():
        st.error("Inserisci del testo con i prezzi!")
    else:
        risultato = applica_percentuale_testo(testo_originale, percentuale, formato)
        st.text_area("Risultato", value=risultato, height=250)
