# streamlit_app.py
# Salasanamoottorin Web-käyttöliittymä
# Ajo: streamlit run streamlit_app.py
# TV - 2026-03-22

import streamlit as st
import logic  # Tuodaan itse tehty logiikkamoduuli

# --- Sivun konfiguraatio ---
st.set_page_config(page_title="Salasanamoottori", page_icon="🔐", layout="centered")

# --- Välimuistitetut latausfunktiot UI-tasolla ---
@st.cache_data
def hae_sanalista_kayttöön():
    """Hakee raakalistan verkosta ja pitää sen välimuistissa."""
    # Ensisijaisesti verkosta, varalla paikallinen tiedosto
    lista = logic.lue_sanalista_verkosta()
    if not lista:
        lista = logic.lue_sanalista_tiedostosta("kotus_sanat.txt")
    return lista

# --- Käyttöliittymän rakentaminen ---

st.header("🔐 Salasanamoottori")

# Sivupalkki asetuksille
with st.sidebar:
    st.header("⚙️ Asetukset")
    skandit_input = st.radio("Sallitaanko skandit (å, ä, ö)?", ("Ei (oletus)", "Kyllä"), index=0)
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
    st.markdown("### 🔗 Lähdekoodi")
    st.markdown("[GitHub: sedan-sihtaus](https://github.com/tuomastvirtanen/sedan-sihtaus)")
    st.caption("Sovellus on palvelimeton; tietoja ei tallenneta.")

# 1. Hae ja suodata sanalista
raakalista = hae_sanalista_kayttöön()

if raakalista:
    sanalista = logic.suodata_sanalista(raakalista, min_p, max_p, salli_skandit, min_vk, max_vk)

    if not sanalista:
        st.error("Ei sanoja valituilla rajoilla.")
        st.stop()

    # --- Välilehdet ---
    tab1, tab2, tab3, tab4, tabo0 = st.tabs(
        ["🚀 Generaattori", "🗣️ Tunniste-tila", "🤪 Muunnos-kone", "🎲 Luvut", "📖 Ohjeet"]
    )

    with tab1:
        entropia = logic.laske_entropia(len(sanalista), sanojen_lkm)
        vahvuus, ikoni = logic.arvioi_vahvuus(entropia)
        st.info(f"Avaruus: **{len(sanalista)}** | Vahvuus: **{int(entropia)} b** ({vahvuus} {ikoni})")

        if st.button("Generoi 10 ehdotusta", type="primary", key="gen_salalause"):
            ehdotukset = logic.generoi_salalauseet(sanalista, sanojen_lkm, 10)
            st.write("---")
            for e in ehdotukset:
                cols = st.columns([4, 1])
                cols[0].code(e, language=None)
                cols[1].caption(f"{len(e)} merk.")

    with tab2:
        vaikeat_foneettiset = set("bcfgqwxzåäö")
        tunniste_lista = [s for s in sanalista if 3 <= len(s) <= 7 and not any(c in vaikeat_foneettiset for c in s.lower())]

        if len(tunniste_lista) < 15:
            st.warning("Liian vähän vaihtelua tunnisteille. Laske vaikeusastetta tai salli skandit.")
        else:
            t_lkm = st.slider("Tunnisteen sanojen määrä", 2, 5, 3)
            if st.button("Generoi 10 tunnistetta", key="gen_tunniste"):
                tunnisteet = logic.generoi_salalauseet(tunniste_lista, t_lkm, 10)
                st.write("---")
                for t in tunnisteet:
                    st.success(f"**{t}**")
                    st.caption(f"Pituus: {len(t)} merkkiä")

    with tab3:
        st.subheader("Sananmuunnos-kone")
        sanakirja_setti = set(s.split('\t')[0].lower() for s in raakalista if s.strip())
        muunnos_lista = [s for s in sanalista if 3 <= len(s) <= 9]

        if st.button("Etsi aitoja sananmuunnoksia", key="gen_muunnos"):
            st.write("---")
            loytynyt, yritykset = 0, 0
            while loytynyt < 10 and yritykset < 5000:
                yritykset += 1
                s1, s2 = logic.random.sample(muunnos_lista, 2)
                m1, m2 = logic.tee_sananmuunnos(s1, s2)
                if m1 in sanakirja_setti and m2 in sanakirja_setti and m1 != s1:
                    st.write(f"✅ **{s1} {s2}** ➜  `{m1} {m2}`")
                    loytynyt += 1
            st.caption(f"Etsitty {yritykset} parin joukosta.")

    with tab4:
        st.subheader("Tunnusluku-kone")
        n_pituus = st.slider("Numeroiden määrä", 4, 12, 6, key="n_slider")
        
        # Arvonta-logiikka
        if st.button("Arvo uusi luku", key="gen_luku"):
            luku = "".join(str(n) for n in logic.arvo_numerot(n_pituus))
            st.code(luku, language=None)
        else:
            luku = "".join(str(n) for n in logic.arvo_numerot(n_pituus))
            st.code(luku, language=None)

    with tab0:
        st.subheader("Tietoa ohjelmasta")
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.info("README.md tiedostoa ei löytynyt. Katso ohjeet GitHubista.")

st.markdown("---")
st.markdown("© TV 2026-03-23 | Data: Kotus")