# Streamlit-web-versio Kotuksen sanalistaa hyödyntävästä salasanamoottorista
# TV - 2026-03-22

import math
import os
import random

import streamlit as st

# --- Sivun konfiguraatio ---
st.set_page_config(page_title="Salasanamoottori", page_icon="🔐", layout="centered")

# --- Funktiot ---


@st.cache_data
def lue_sanalista_tiedostosta(tiedostonimi, min_len, max_len, salli_skandit):
    """Lukee sanalistan paikallisesta tiedostosta ja suodattaa pituuden sekä skandien mukaan."""
    hakusanat = []
    skandit_set = set("åäöÅÄÖ")

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, tiedostonimi)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for rivi in f:
                osat = rivi.strip().split("\t")
                if not osat:
                    continue
                sana = osat[0]
                if not (min_len <= len(sana) <= max_len):
                    continue
                if not salli_skandit and any(c in skandit_set for c in sana):
                    continue
                if not sana.isalpha():
                    continue
                hakusanat.append(sana)
    except Exception as e:
        st.error(f"Virhe tiedoston luvussa: {e}")
        return None
    return hakusanat


def laske_entropia(sanalista_koko, sanojen_maara):
    if sanalista_koko <= 0 or sanojen_maara <= 0:
        return 0
    return math.log2(sanalista_koko**sanojen_maara)


def arvioi_vahvuus(entropia):
    if entropia < 45:
        return "Heikko", "🔴"
    if entropia < 60:
        return "Kohtalainen", "🟠"
    if entropia < 80:
        return "Vahva", "🟢"
    if entropia < 128:
        return "Erit. vahva", "🔵"
    return "AES-taso (murtamaton)", "⭐"


def laske_vaikeuskerroin(sana):
    """Laskee sanan vaikeuden 0-100 välillä suodatusta varten."""
    score = len(sana) * 2
    if len(sana) > 12:
        score += 15
    harvinaiset = set("bcfgqwxzå")
    loytyneet_harvinaiset = [c for c in sana.lower() if c in harvinaiset]
    score += len(loytyneet_harvinaiset) * 10
    uniikit_merkit = len(set(sana))
    if len(sana) > 0:
        score += (uniikit_merkit / len(sana)) * 20
    vokaalit = set("aeiouyäö")
    perakkaiset_konsonantit = 0
    max_perakkaiset = 0
    for char in sana.lower():
        if char.isalpha() and char not in vokaalit:
            perakkaiset_konsonantit += 1
            max_perakkaiset = max(max_perakkaiset, perakkaiset_konsonantit)
        else:
            perakkaiset_konsonantit = 0
    score += max_perakkaiset * 5
    return round(min(score, 100))


def generoi_salalauseet(sanalista, sanojen_lkm, n=1):
    lauseet = []
    for _ in range(n):
        if len(sanalista) >= sanojen_lkm:
            valitut = random.sample(sanalista, sanojen_lkm)
        else:
            valitut = [random.choice(sanalista) for _ in range(sanojen_lkm)]
        lauseet.append("-".join(valitut).lower())
    return lauseet


# --- Käyttöliittymä (UI) ---

st.header("🔐 Salasana-moottori")
st.write("Generoi turvallisia salalauseita suoraan selaimessa.")

# Sivupalkki asetuksille
with st.sidebar:
    st.header("⚙️ Asetukset")

    skandit_input = st.radio(
        "Sallitaanko skandit (å, ä, ö)?", ("Ei (oletus)", "Kyllä"), index=0
    )
    salli_skandit = skandit_input == "Kyllä"

    oletus_lkm = 4 if salli_skandit else 5
    sanojen_lkm = st.slider("Sanojen määrä", 2, 12, oletus_lkm)

    with st.expander("Sanan pituus"):
        min_p = st.number_input("Min", 3, 20, 6)
        max_p = st.number_input("Max", min_p, 30, 11)

    with st.expander("Vaikeusasteen rajat (0-100)"):
        min_vk = st.slider("Alaraja", 0, 100, 0)
        max_vk = st.slider("Yläraja", 0, 100, 100)

    st.markdown("---")
    with st.expander("ℹ️ Mikä on vaikeusaste?"):
        st.write("""
        Vaikeusaste (0–100) arvioi lauseen kirjoittamista ja muistamista. 
        Pisteitä lisäävät:
        * Sanan pituus
        * Harvinaiset kirjaimet (b, f, g, q, w, x, z, å)
        * Peräkkäiset konsonantit
        * Uniikkien merkkien määrä
        """)

    st.markdown("---")
    st.markdown("### 🔗 Lähdekoodi")
    st.markdown(
        "[GitHub: sedan-sihtaus](https://github.com/tuomastvirtanen/sedan-sihtaus)"
    )
    st.caption("Sovellus ei tallenna tai lähetä generoituja salalauseita.")

# 1. Lue sanalista tiedostosta
raakasanalista = lue_sanalista_tiedostosta(
    "kotus_sanat.txt", min_p, max_p, salli_skandit
)

if raakasanalista:
    # 2. Suodata vaikeusasteen mukaan (vaikuttaa entropiaan ja sanavalintoihin)
    sanalista = [
        s for s in raakasanalista if min_vk <= laske_vaikeuskerroin(s) <= max_vk
    ]

    if not sanalista:
        st.error(f"Ei sanoja vaikeusrajoilla {min_vk}-{max_vk}.")
        st.stop()

    # 3. Tunniste-tila suodatus
    vaikeat_foneettiset = set("bcfgqwxzåäö")
    tunniste_lista = [
        s
        for s in sanalista
        if 4 <= len(s) <= 6 and not any(c in vaikeat_foneettiset for c in s.lower())
    ]

    # --- Välilehdet ---
    tab1, tab2 = st.tabs(["🚀 Generaattori", "🗣️ Tunniste-tila"])

    with tab1:
        entropia = laske_entropia(len(sanalista), sanojen_lkm)
        vahvuus, ikoni = arvioi_vahvuus(entropia)

        st.info(
            f"Avaruus: **{len(sanalista)}** | Vahvuus: **{int(entropia)} b** ({vahvuus} {ikoni})"
        )

        if st.button("Generoi 10 ehdotusta", type="primary"):
            ehdotukset = generoi_salalauseet(sanalista, sanojen_lkm, 10)
            st.write("---")
            for e in ehdotukset:
                cols = st.columns([4, 1])
                cols[0].code(e, language=None)
                # Näytetään vain pituus tuloksissa selkeyden vuoksi
                cols[1].caption(f"{len(e)} merk.")

    with tab2:
        if len(tunniste_lista) < 10:
            st.warning("Liian vähän sanoja tunnisteille näillä rajoilla.")
        else:
            t_sanojen_lkm = st.slider("Tunnisteen sanojen määrä", 2, 5, 3)
            t_entropia = laske_entropia(len(tunniste_lista), t_sanojen_lkm)
            vahvuus_t, ikoni_t = arvioi_vahvuus(t_entropia)

            st.info(
                f"Tunniste-tila ({t_sanojen_lkm} sanaa). Vahvuus: **{int(t_entropia)} b** ({vahvuus_t} {ikoni_t})"
            )

            if st.button("Generoi 10 tunnistetta"):
                tunnisteet = generoi_salalauseet(tunniste_lista, t_sanojen_lkm, 10)
                st.write("---")
                for t in tunnisteet:
                    st.success(f"**{t}**")

st.markdown("---")
st.markdown("© TV 2026-03-22 | Data: Kotus")
