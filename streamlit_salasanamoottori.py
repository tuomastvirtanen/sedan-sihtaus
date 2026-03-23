# Streamlit-web-versio Kotuksen sanalistaa hyödyntävästä salasanamoottorista
# Sisältää: Salasana-generaattorin, Tunniste-tilan ja Sananmuunnos-koneen.
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
    # Kryptografisesti vahva generaattori
    cryptogen = random.SystemRandom()
    for _ in range(n):
        if len(sanalista) >= sanojen_lkm:
            valitut = cryptogen.sample(sanalista, sanojen_lkm)
        else:
            valitut = [cryptogen.choice(sanalista) for _ in range(sanojen_lkm)]
        lauseet.append("-".join(valitut).lower())
    return lauseet


def tee_sananmuunnos(sana1, sana2):
    """Suorittaa klassisen suomalaisen sananmuunnoksen."""

    def halkaise(sana):
        vokaalit = "aeiouyäö"
        for i, kirjain in enumerate(sana.lower()):
            if kirjain in vokaalit:
                return sana[: i + 1], sana[i + 1 :]
        return sana, ""

    alku1, loppu1 = halkaise(sana1)
    alku2, loppu2 = halkaise(sana2)
    return (alku2 + loppu1).lower(), (alku1 + loppu2).lower()

def arvo_numerot(lkm):
    """Arpoo lkm satunnaista numeroa 0-9 väliltä."""
    cryptogen = random.SystemRandom()
    return [cryptogen.randint(0, 9) for _ in range(lkm)]


# --- Käyttöliittymä (UI) ---

st.header("🔐 Salasanamoottori")

# Sivupalkki asetuksille
with st.sidebar:
    st.header("⚙️ Asetukset")

    skandit_input = st.radio(
        "Sallitaanko skandit (å, ä, ö)?", ("Ei (oletus)", "Kyllä"), index=0
    )
    salli_skandit = skandit_input == "Kyllä"

    oletus_lkm = 4 if salli_skandit else 5
    sanojen_lkm = st.slider("Sanojen määrä", 3, 12, oletus_lkm)

    with st.expander("Sanan pituus"):
        min_p = st.number_input("Min", 3, 20, 6)
        max_p = st.number_input("Max", min_p, 30, 11)

    with st.expander("Vaikeusasteen rajat (0-100)"):
        min_vk = st.slider("Alaraja", 0, 100, 0)
        max_vk = st.slider("Yläraja", 0, 100, 100)

    st.markdown("---")
    with st.expander("ℹ️ Mikä on vaikeusaste?"):
        st.write(
            "Pisteitä lisäävät sanan pituus, harvinaiset kirjaimet ja konsonanttiyhdistelmät."
        )

    st.markdown("---")
    st.markdown("### 🔗 Lähdekoodi")
    st.markdown(
        "[GitHub: sedan-sihtaus](https://github.com/kayttajanimi/sedan-sihtaus)"
    )
    st.caption("Sovellus on täysin palvelimeton; tietoja ei tallenneta.")

# 1. Lue sanalista
raakasanalista = lue_sanalista_tiedostosta(
    "kotus_sanat.txt", min_p, max_p, salli_skandit
)

if raakasanalista:
    sanalista = [
        s for s in raakasanalista if min_vk <= laske_vaikeuskerroin(s) <= max_vk
    ]

    if not sanalista:
        st.error("Ei sanoja valituilla rajoilla.")
        st.stop()

    # --- Välilehdet ---
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🚀 Generaattori", "🗣️ Tunniste-tila", "🤪 Muunnos-kone", "🎲 Luvut"]
    )

    with tab1:
        entropia = laske_entropia(len(sanalista), sanojen_lkm)
        vahvuus, ikoni = arvioi_vahvuus(entropia)
        st.info(
            f"Avaruus: **{len(sanalista)}** | Vahvuus: **{int(entropia)} b** ({vahvuus} {ikoni})"
        )

        if st.button("Generoi 10 ehdotusta", type="primary", key="gen_salalause"):
            ehdotukset = generoi_salalauseet(sanalista, sanojen_lkm, 10)
            st.write("---")
            for e in ehdotukset:
                cols = st.columns([4, 1])
                cols[0].code(e, language=None)
                cols[1].caption(f"{len(e)} merk.")

    with tab2:
        # Laajennetaan pituushaitaria vähäsen (3-7 merkkiä)
        vaikeat_foneettiset = set("bcfgqwxzåäö")
        tunniste_lista = [
            s
            for s in sanalista
            if 3 <= len(s) <= 7 and not any(c in vaikeat_foneettiset for c in s.lower())
        ]

        if len(tunniste_lista) < 15:
            st.warning(
                "Liian vähän vaihtelua tunnisteille. Laske vaikeusastetta tai salli skandit."
            )
        else:
            t_lkm = st.slider("Tunnisteen sanojen määrä", 2, 5, 3)

            if st.button("Generoi 10 tunnistetta", key="gen_tunniste"):
                # Käytetään SystemRandomia
                cryptogen = random.SystemRandom()
                tunnisteet = []

                for _ in range(10):
                    # Valitaan sanat siten, että pituudet vaihtelevat
                    valitut = cryptogen.sample(tunniste_lista, t_lkm)
                    tunnisteet.append("-".join(valitut).lower())

                st.write("---")
                for t in tunnisteet:
                    # Nyt pituudet vaihtelevat, esim. 'talo-vene-muki' vs 'tie-auto-lasi'
                    st.success(f"**{t}**")
                    st.caption(f"Pituus: {len(t)} merkkiä")

    with tab3:
        st.subheader("Sananmuunnos-kone")
        st.write(
            "Etsii sanalistasta pareja, joiden muunnos muodostaa oikeita suomen kielen sanoja."
        )

        # Luodaan set-rakenne nopeaa hakua varten (jos sitä ei ole jo tehty)
        sanakirja_setti = set(s.lower() for s in raakasanalista)
        # Rajataan lista lyhyisiin perussanoihin, jotta haku on mielekäs
        muunnos_lista = [s for s in raakasanalista if 3 <= len(s) <= 9]

        if st.button("Etsi aitoja sananmuunnoksia"):
            cryptogen = random.SystemRandom()
            st.write("---")
            loytynyt = 0
            yritykset = 0

            # Yritetään löytää 10 aitoa muunnosta (rajoitetaan yritykset jumiutumisen estämiseksi)
            while loytynyt < 10 and yritykset < 5000:
                yritykset += 1
                s1, s2 = cryptogen.sample(muunnos_lista, 2)
                m1, m2 = tee_sananmuunnos(s1, s2)

                # Tarkistetaan löytyvätkö molemmat muunnokset sanakirjasta
                if m1 in sanakirja_setti and m2 in sanakirja_setti:
                    # Estetään itsestäänselvyydet (jos sanat eivät muuttuneet)
                    if m1 != s1:
                        st.write(f"✅ **{s1} {s2}** ➜  `{m1} {m2}`")
                        loytynyt += 1

            if loytynyt == 0:
                st.warning(
                    "Aitoja muunnoksia ei löytynyt näillä asetuksilla. Kokeile uudestaan!"
                )
            else:
                st.caption(f"Etsitty {yritykset} parin joukosta.")

    with tab4:
        st.subheader("Tunnusluku-kone")
        st.write(
            "Nämä sovelutuvat vaikkapa PIN-koodiksi."
        )

        # Lisätään valitsin pituudelle
        n_pituus = st.slider("Numeroiden määrä", 4, 16, 6)

        if st.button("Arvo uusi luku", key="gen_luku"):
            uusi_luku = "".join(str(n) for n in arvo_numerot(n_pituus))
            st.code(uusi_luku, language=None)
        else:
            # Näytetään oletusluku heti kättelyssä
            oletus_luku = "".join(str(n) for n in arvo_numerot(n_pituus))
            st.code(oletus_luku, language=None)

        if st.button("Arvo uusi luku"):
            lukusarja = arvo_numerot(6) 

        st.code("".join(str(n) for n in lukusarja), language=None)

st.markdown("---")
st.markdown("© TV 2026-03-22 | Data: Kotus")
