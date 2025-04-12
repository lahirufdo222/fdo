import streamlit as st
import math
import re

# Funzioni per il calcolo dei prezzi

def arrotonda_intero_con_00(valore: float) -> str:
    """
    Arrotonda all'intero (round half-up) e restituisce una stringa con ",00".
    Es.: 577 * 1.02 = 588.54 → 589 → "589,00"
    """
    intero = int(math.floor(valore + 0.5))
    return f"{intero},00"

def arrotonda_intero_senza_00(valore: float) -> str:
    """
    Arrotonda all'intero (round half-up) e restituisce la stringa senza decimali.
    Es.: 577 * 1.02 → 589 → "589"
    """
    intero = int(math.floor(valore + 0.5))
    return f"{intero}"

def arrotonda_due_decimali(valore: float) -> str:
    """
    Arrotonda a due decimali (round half-up) e restituisce la stringa con virgola.
    Es.: 577 * 1.02 = 588.54 → "588,54"
    """
    dec = math.floor(valore * 100 + 0.5) / 100
    return f"{dec:.2f}".replace('.', ',')

def elabora_prezzo(match, percentuale: float, formato: str) -> str:
    """
    Elabora un prezzo trovato nel testo nel formato "€ 577,00" e lo aggiorna
    applicando la variazione percentuale, arrotondando secondo il formato scelto.
    """
    testo_originale = match.group(0)
    # Rimuove "€" e spazi e normalizza il separatore decimale
    prezzo_str = testo_originale.replace('€', '').strip().replace(' ', '')
    normalizzato = prezzo_str.replace(',', '.')
    try:
        prezzo_iniziale = float(normalizzato)
    except ValueError:
        return testo_originale

    nuovo_prezzo = prezzo_iniziale * (1 + percentuale / 100.0)
    if formato == "Intero con ,00":
        risultato = arrotonda_intero_con_00(nuovo_prezzo)
    elif formato == "Intero senza ,00":
        risultato = arrotonda_intero_senza_00(nuovo_prezzo)
    else:  # "Due decimali"
        risultato = arrotonda_due_decimali(nuovo_prezzo)
    return f"€ {risultato}"

def applica_percentuale_testo(testo: str, percentuale: float, formato: str) -> str:
    """
    Cerca nel testo i prezzi nel formato "€ xxx,xx" (o "€xxx.xx") e li sostituisce
    col nuovo prezzo aggiornato.
    """
    pattern = re.compile(r"€\s*[0-9\s]+[.,][0-9]{2}")
    return pattern.sub(lambda m: elabora_prezzo(m, percentuale, formato), testo)

# --- Interfaccia Streamlit ---

st.set_page_config(page_title="Strumento Variazione Prezzi", page_icon="💶", layout="centered")

st.title("🔧 Strumento Online di Variazione dei Prezzi")
st.markdown(
    """
    Inserisci il **testo** contenente i prezzi (es. "€ 577,00"), 
    imposta la **variazione percentuale** (può essere positiva o negativa)
    e **scegli il formato** di arrotondamento.
    
    **Opzioni di arrotondamento:**
    - **Intero con ,00:** arrotonda all'intero e mostra sempre ",00" (es. "589,00")
    - **Intero senza ,00:** arrotonda all'intero senza decimali (es. "589")
    - **Due decimali:** arrotonda a due decimali (es. "588,54")
    """
)

# Input per il testo originale
testo_originale = st.text_area("Testo Originale", height=300)

# Input per la variazione percentuale
percentuale = st.number_input("Variazione Percentuale (%)", value=2.0, step=0.1, format="%.2f")

# Scelta del formato di arrotondamento tramite radio button
formato = st.radio("Formato Prezzo", ("Intero con ,00", "Intero senza ,00", "Due decimali"))

# Pulsante per eseguire la modifica
if st.button("🚀 Applica Variazione"):
    if not testo_originale.strip():
        st.error("Inserisci del testo per elaborare i prezzi!")
    else:
        risultato = applica_percentuale_testo(testo_originale, percentuale, formato)
        st.text_area("Testo Modificato", value=risultato, height=300)
