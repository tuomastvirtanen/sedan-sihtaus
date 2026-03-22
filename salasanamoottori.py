# Salasanamoottori - CLI-versio (Command Line Interface)
# Sisältää: Salasana-generaattorin, Tunniste-tilan ja Sananmuunnos-koneen.
# TV - 2026-03-22

import math
import os
import random
import sys

# --- Funktiot ---


def lue_sanalista_tiedostosta(tiedostonimi, min_len, max_len, salli_skandit):
    """Lukee sanalistan paikallisesta tiedostosta ja suodattaa pituuden sekä skandien mukaan."""
    hakusanat = []
    skandit_set = set("åäöÅÄÖ")

    # Etsitään tiedosto samasta kansiosta kuin skripti
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, tiedostonimi)

    if not os.path.exists(file_path):
        print(f"❌ Virhe: Tiedostoa '{tiedostonimi}' ei löydy polusta {current_dir}")
        return None

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
        print(f"❌ Virhe tiedoston luvussa: {e}")
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


# --- Pääohjelma ---


def main():
    print("🔐 SALASANAMOOTTORI CLI")
    print("-" * 30)

    # Asetukset (vastaavat Streamlitin sivupalkkia)
    salli_skandit = False
    sanojen_lkm = 5
    min_p, max_p = 6, 11
    min_vk, max_vk = 0, 100

    # 1. Lue sanalista
    raakasanalista = lue_sanalista_tiedostosta(
        "kotus_sanat.txt", min_p, max_p, salli_skandit
    )

    if not raakasanalista:
        sys.exit(1)

    sanalista = [
        s for s in raakasanalista if min_vk <= laske_vaikeuskerroin(s) <= max_vk
    ]

    if not sanalista:
        print("❌ Virhe: Sanalista on tyhjä annetuilla rajoilla.")
        sys.exit(1)

    while True:
        print("\nVALITSE TOIMINTO:")
        print("1. Generoi salalauseita")
        print("2. Tunniste-tila (helpot sanat)")
        print("3. Sananmuunnos-kone")
        print("4. Lopeta")

        valinta = input("\nSyötä numero (1-4): ")

        if valinta == "1":
            entropia = laske_entropia(len(sanalista), sanojen_lkm)
            vahvuus, ikoni = arvioi_vahvuus(entropia)
            print(
                f"\n📊 Avaruus: {len(sanalista)} sanaa | Vahvuus: {int(entropia)} b ({vahvuus} {ikoni})"
            )
            ehdotukset = generoi_salalauseet(sanalista, sanojen_lkm, 10)
            print("-" * 30)
            for e in ehdotukset:
                print(f"[{len(e):2} merk] {e}")

        elif valinta == "2":
            vaikeat_foneettiset = set("bcfgqwxzåäö")
            tunniste_lista = [
                s
                for s in sanalista
                if 4 <= len(s) <= 6
                and not any(c in vaikeat_foneettiset for c in s.lower())
            ]
            if len(tunniste_lista) < 10:
                print("⚠️ Liian vähän helppoja sanoja.")
            else:
                t_lkm = 3
                tunnisteet = generoi_salalauseet(tunniste_lista, t_lkm, 10)
                print("\n🗣️ TUNNISTEET:")
                for t in tunnisteet:
                    print(f" > {t}")

        elif valinta == "3":
            print("\n🤪 SANANMUUNNOS-KONE")
            sanakirja_setti = set(s.lower() for s in raakasanalista)
            muunnos_lista = [s for s in raakasanalista if 3 <= len(s) <= 9]
            cryptogen = random.SystemRandom()
            loytynyt = 0
            yritykset = 0

            while loytynyt < 10 and yritykset < 5000:
                yritykset += 1
                s1, s2 = cryptogen.sample(muunnos_lista, 2)
                m1, m2 = tee_sananmuunnos(s1, s2)
                if m1 in sanakirja_setti and m2 in sanakirja_setti and m1 != s1:
                    print(f"✅ {s1} {s2} ➜  {m1} {m2}")
                    loytynyt += 1
            if loytynyt == 0:
                print("⚠️ Aitoja muunnoksia ei löytynyt.")

        elif valinta == "4":
            print("Moi moi!")
            break
        else:
            print("Virheellinen valinta.")


if __name__ == "__main__":
    main()
