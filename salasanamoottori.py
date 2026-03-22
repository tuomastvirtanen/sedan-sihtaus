# ohjelma lukee kotimaisten kielenten keskuksen julkaisemaa sanalistaa
# Sanatietue koostuu seuraavista tiedoista: 1) hakusana, 2) homonymia, 3) sanaluokka ja 4) taivutus.
# TV - 2026-03-22

# /// script
# dependencies = [
#   "pyperclip",
# ]
# ///

import math  # laskentaan
import random  # arvontaan
import sys  # ohjelman hallittu lopetus
import urllib.request  # jotta luetaan tietoja netistä

import pyperclip  # kopio leikepöydälle


def lue_sanalista_verkosta(url, min_pituus, max_pituus, salli_skandit):
    """Lataa sanalistan suoraan Kotuksen palvelimelta ja suodattaa sen."""
    hakusanat = []
    skandit = set("åäöÅÄÖ")

    try:
        print(f"Ladataan sanalistaa osoitteesta: {url}...")
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
        print(f"\nVirhe sanalistan latauksessa: {e}")
        return None

    return hakusanat


def laske_entropia(sanalista_koko, sanojen_maara):
    if sanalista_koko <= 0 or sanojen_maara <= 0:
        return 0
    return math.log2(sanalista_koko**sanojen_maara)


def arvioi_vahvuus(entropia):
    if entropia < 45:
        return "Heikko"
    if entropia < 60:
        return "Kohtalainen"
    if entropia < 80:
        return "Vahva"
    return "Erit. vahva"


def arvioi_vaikeus(pisteet):
    """Palauttaa vaikeuden pyöristettynä numerona 1-100."""
    return round(pisteet)


def laske_vaikeuskerroin(sana):
    score = 0
    score += len(sana) * 2
    if len(sana) > 12:
        score += 15

    harvinaiset = set("bcfgqwxzå")
    loytyneet_harvinaiset = [c for c in sana.lower() if c in harvinaiset]
    score += len(loytyneet_harvinaiset) * 10

    uniikit_merkit = len(set(sana))
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


def generoi_salalause(sanalista, sanojen_lkm):
    if len(sanalista) >= sanojen_lkm:
        valitut = random.sample(sanalista, sanojen_lkm)
    else:
        valitut = [random.choice(sanalista) for _ in range(sanojen_lkm)]
    return "-".join(valitut).lower()


def main():
    url = "https://kaino.kotus.fi/lataa/nykysuomensanalista2024.txt"

    print("\n" + "=" * 35)
    print("      SALALAUSEGENERAATTORI")
    print("=" * 35)

    skandit = input("Sallitaanko skandit (å, ä, ö)? (k/(e)): ").lower() == "k"
    oletus_lkm = 4 if skandit else 5

    try:
        min_p = int(input("Lyhyin sanan pituus (6): ") or "6")
        max_p = int(input("Pisin sanan pituus (11): ") or "11")
        sanojen_lkm = int(input(f"Sanojen määrä ({oletus_lkm}): ") or str(oletus_lkm))

        # UUSI: Vaikeusasteen rajat
        min_vk = int(input("Vaikeusasteen alaraja (0): ") or "0")
        max_vk = int(input("Vaikeusasteen yläraja (100): ") or "100")

    except ValueError:
        print("Virheellinen syöte, käytetään oletusarvoja.")
        min_p, max_p, sanojen_lkm = 6, 11, oletus_lkm
        min_vk, max_vk = 0, 100

    # Haetaan data
    raakasanalista = lue_sanalista_verkosta(url, min_p, max_p, skandit)

    if not raakasanalista:
        print("Sanalistaa ei voitu ladata.")
        sys.exit(1)

    # Suodatetaan lista vaikeusasteen mukaan
    sanalista = [
        s for s in raakasanalista if min_vk <= laske_vaikeuskerroin(s) <= max_vk
    ]

    if not sanalista:
        print(f"Sanalista on tyhjä annetuilla vaikeusrajoilla ({min_vk}-{max_vk}).")
        sys.exit(1)

    entropia = laske_entropia(len(sanalista), sanojen_lkm)
    vahvuus_teksti = arvioi_vahvuus(entropia)

    print(f"\nSana-avaruus: {len(sanalista)} sanaa.")
    print(f"Teoreettinen vahvuus: {int(entropia)} bittiä ({vahvuus_teksti}).")

    print("\nValitse tila:")
    print("(1) Yksittäinen ehdotus")
    print("(2) Lista 15 vaihtoehtoa")
    print("(3) Tunniste (ääneen lausuttava, 3 sanaa)")
    tila = input("\nSyötä tila (1/2/3): ")

    match tila:
        case "2":
            ehdotukset = [generoi_salalause(sanalista, sanojen_lkm) for _ in range(15)]
            pisin_lause_len = max(len(e) for e in ehdotukset)
            sarake_leveys = max(50, pisin_lause_len + 2)

            otsikko = (
                f"{'Nro':<4} | {'Salalause':<{sarake_leveys}} | {'Pituus':<10} | "
                f"{'Bitit':<8} | {'Vahvuus':<12} | {'Vaikeus'}"
            )

            print("\n" + "=" * len(otsikko))
            print(otsikko)
            print("-" * len(otsikko))

            for i, ehdotus in enumerate(ehdotukset, 1):
                sanat = ehdotus.split("-")
                vk = sum(laske_vaikeuskerroin(s) for s in sanat) / len(sanat)
                print(
                    f"{i:>2}.  | {ehdotus:<{sarake_leveys}} | {len(ehdotus):>3} merk. | "
                    f"{int(entropia):>3} b    | {vahvuus_teksti:<12} | {arvioi_vaikeus(vk)}"
                )
            print("=" * len(otsikko))

            valinta = input("\nKopioi numero (1-15) tai 'e' (exit): ")
            if valinta.isdigit() and 1 <= int(valinta) <= 15:
                valittu = ehdotukset[int(valinta) - 1]
                pyperclip.copy(valittu)
                print(f"\n*** '{valittu}' kopioitu! ***")

        case "3":
            # Tunniste-tila: Foneettisesti selkeät sanat (sisältää oman suodatuksen)
            vaikeat = set("bcfgqwxzåäö")
            tunniste_lista = [
                s
                for s in sanalista  # Käyttää jo valmiiksi vaikeussuodatettua listaa
                if 4 <= len(s) <= 6 and not any(c in vaikeat for c in s.lower())
            ]
            if len(tunniste_lista) < 10:
                print(
                    "Tunniste-tilaan sopivia sanoja ei löytynyt vaikeusrajojen puitteissa."
                )
                sys.exit(1)

            t_entropia = laske_entropia(len(tunniste_lista), 3)
            ehdotukset = [generoi_salalause(tunniste_lista, 3) for _ in range(15)]

            print("\n--- LUODAAN 15 TUNNISTETTA (Ääneen lausuttavat) ---")
            otsikko = f"{'Nro':<4} | {'Tunniste':<30} | {'Vahvuus':<10} | {'Vaikeus'}"
            print("-" * len(otsikko))

            for i, ehdotus in enumerate(ehdotukset, 1):
                sanat = ehdotus.split("-")
                vk = sum(laske_vaikeuskerroin(s) for s in sanat) / 3
                print(
                    f"{i:>2}.  | {ehdotus:<30} | {int(t_entropia):>2} bittiä | {arvioi_vaikeus(vk)}"
                )
            print("-" * len(otsikko))

        case _:
            while True:
                salalause = generoi_salalause(sanalista, sanojen_lkm)
                sanat = salalause.split("-")
                vk = sum(laske_vaikeuskerroin(s) for s in sanat) / len(sanat)

                print(f"\nEhdotus: {salalause}")
                print(
                    f"Vahvuus: {int(entropia)} b ({vahvuus_teksti}) | Vaikeus: {arvioi_vaikeus(vk)}"
                )

                vastaus = input("\nKelpaako? (k/e/[uusi]): ").lower() or "uusi"

                if vastaus == "k":
                    pyperclip.copy(salalause)
                    print("\n*** Kopioitu! ***")
                    break
                elif vastaus == "e":
                    print("\nPoistutaan kopioimatta.")
                    break


if __name__ == "__main__":
    main()
