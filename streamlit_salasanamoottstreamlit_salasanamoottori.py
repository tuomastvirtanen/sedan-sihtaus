# Streamlit-web-versio Kotuksen sanalistaa hyödyntävästä salasanamoottorista
# TV - 2026-03-22

import streamlit as st
import math
import random
import urllib.request

# --- Sivun konfiguraatio ---
st.set_page_config(page_title="Salasanamoottori", page_icon="🔐")

# --- Funktiot (pääosin samat kuin komentoriviversiossa) ---

@st.cache_data(show_spinner="Ladataan sanalistaa Kotuksesta...")
def lue_sanalista_verkosta(url, min_pituus, max_pituus, salli_skandit):
    """Lataa sanalistan Kotuksen palvelimelta ja suodattaa sen. Välimuistitetaan."""
    hakusanat = []
    skandit = set("åäöÅÄÖ")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = response.read().decode("utf-8")
            for rivi in data.splitlines():
                osat = rivi.strip().split("\t")
                if not osat:
                    continue
                sana = osat[0]
                if not (min_pituus <= len(sana) <= max_pituus):
                    continue
                if not salli_skandit and any(c in skandit for c in sana):
                    continue
                if not sana.isalpha():
                    continue
                hakusanat.append(sana)
    except Exception as e:
        st.error(f"Virhe sanalistan latauksessa: {e}")
        return None
    return hakusanat

def laske_entropia(sanalista_koko, sanojen_maara):
    if sanalista_koko <= 0 or sanojen_maara <= 0:
        return 0
    return math.log2(sanalista_koko**sanojen_maara)

def arvioi_vahvuus(entropia):
    if entropia < 45: return "Heikko", "🔴"
    if entropia < 60: return "Kohtalainen", "🟠"
    if entropia < 80: return "Vahva", "🟢"
    if entropia < 128: return "Erit. vahva", "🔵"
    return "AES-taso (murtamaton)", "⭐"

def laske_vaikeuskerroin(sana):
    """Sama algoritmi kuin komentoriviversiossa."""
    score = len(sana) * 2
    if len(sana) > 12: score += 15
    harvinaiset = set("bcfgqwxzå")
    loytyneet_harvinaiset = [c for c in sana.lower() if c in harvinaiset]
    score += len(loytyneet_harvinaiset) * 10
    uniikit_merkit = len(set(sana))
    if len(sana) > 0: score += (uniikit_merkit / len(sana)) * 20
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

st.title("🔐 Salasanamoottori")
st.write("Generoi turvallisia ja muistettavia salalauseita Kotuksen nykysuomen sanalistan avulla.")

# Sivupalkki asetuksille (Sidebar)
with st.sidebar:
    st.header("⚙️ Asetukset")
    
    # Skandit ja dynaaminen sanojen määrä -suositus
    skandit_input = st.radio("Sallitaanko skandit (å, ä, ö)?", ("Ei (oletus)", "Kyllä"), index=0)
    skandit = skandit_input == "Kyllä"
    suositus_lkm = 4 if skandit else 5

    sanojen_lkm = st.slider("Sanojen määrä lauseessa", min_value=3, max_value=12, value=suositus_lkm)
    
    # Sanan pituusrajat (Expander)
    with st.expander("Sanan pituusrajat"):
        min_p = st.number_input("Lyhyin sana", min_value=3, max_value=20, value=6)
        max_p = st.number_input("Pisin sana", min_value=min_p, max_value=30, value=11)

    # Vaikeusasteen suodatus (Expander)
    with st.expander("Vaikeusasteen suodatus (0-100)"):
        min_vk = st.slider("Vaikeusasteen alaraja", 0, 100, 0)
        max_vk = st.slider("Vaikeusasteen yläraja", 0, 100, 100)
    
    # Haetaan ja suodatetaan data
    url = "https://kaino.kotus.fi/lataa/nykysuomensanalista2024.txt"
    raakasanalista = lue_sanalista_verkosta(url, min_p, max_p, skandit)

    if not raakasanalista:
        st.stop() # Lopetetaan suoritus jos dataa ei saada

    # Suodatetaan lista vaikeusasteen mukaan
    sanalista = [s for s in raakasanalista if min_vk <= laske_vaikeuskerroin(s) <= max_vk]
    
    if not sanalista:
        st.error(f"Sanalista on tyhjä annetuilla vaikeusrajoilla ({min_vk}-{max_vk}).")
        st.stop()

    # Tunniste-tilan suodatus (Foneettisesti selkeät sanat)
    vaikeat_foneettisesti = set("bcfgqwxzåäö")
    tunniste_lista = [
        s for s in sanalista 
        if 4 <= len(s) <= 6 and not any(c in vaikeat_foneettisesti for c in s.lower())
    ]

# --- Pääalueen toiminnallisuus ---

tab1, tab2 = st.tabs(["🚀 Generaattori", "🗣️ Tunniste-tila (3 sanaa)"])

# Tabi 1: Perusgeneraattori
with tab1:
    entropia = laske_entropia(len(sanalista), sanojen_lkm)
    vahvuus_teksti, ikoni = arvioi_vahvuus(entropia)

    # Info-laatikko tilastoista
    st.info(f"Sana-avaruus: **{len(sanalista)}** sanaa | Vahvuus: **{int(entropia)}** bittiä | Arvio: **{vahvuus_teksti} {ikoni}**")

    # Generoi-painike
    if st.button("Generoi 10 ehdotusta", type="primary"):
        ehdotukset = generoi_salalauseet(sanalista, sanojen_lkm, n=10)
        
        st.write("---")
        for i, ehdotus in enumerate(ehdotukset):
            sanat = ehdotus.split("-")
            vk = sum(laske_vaikeuskerroin(s) for s in sanat) / len(sanat)
            
            col1, col2 = st.columns([4, 1])
            with col1:
                # Koodi-blokki, josta salalause on helppo kopioida puhelimella
                st.code(ehdotus, language=None)
            with col2:
                # Näytetään vaikeusaste ja pituus
                st.caption(f"Vaikeus: {round(vk)} | {len(ehdotus)} merk.")

# Tabi 2: Tunniste-tila
with tab2:
    if len(tunniste_lista) < 10:
        st.warning(f"Tunniste-tilaan sopivia sanoja ei löytynyt vaikeusrajojen ({min_vk}-{max_vk}) puitteissa.")
    else:
        t_entropia = laske_entropia(len(tunniste_lista), 3)
        st.info(f"Tunniste-tila käyttää 3 selkeää sanaa ({len(tunniste_lista)} sanan avaruudesta). Vahvuus: **{int(t_entropia)}** bittiä.")
        
        if st.button("Generoi 10 tunnistetta"):
            tunnisteet = generoi_salalauseet(tunniste_lista, 3, n=10)
            
            st.write("---")
            for i, tunniste in enumerate(tunnisteet):
                # Tunnisteet ovat lyhyitä, ei tarvita code-blokkia, st.success näyttää ne tyylikkäästi
                st.success(f"**{tunniste}**")

# --- Alatunniste ---
st.markdown("---")
st.markdown("© TV 2026-03-22 | Data: Kotimaisten kielten keskus")
