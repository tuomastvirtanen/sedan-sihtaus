# ohjelma lukee kotimaisten kielenten keskuksen julkaisemaa sanalistaa
# Sanatietue koostuu seuraavista tiedoista: 1) hakusana, 2) homonymia, 3) sanaluokka ja 4) taivutus.
# stv9 - 2026-03-21

# /// script
# dependencies = [
#   "pyperclip",
# ]
# ///

import random
import math
import pyperclip

def lue_sanalista(tiedostonimi, min_pituus, max_pituus, salli_skandit):
    hakusanat = []
    skandit = set("åäöÅÄÖ")
    try:
        with open(tiedostonimi, 'r', encoding='utf-8') as f:
            for rivi in f:
                osat = rivi.strip().split('\t')
                if not osat: continue
                sana = osat[0]
                if not (min_pituus <= len(sana) <= max_pituus): continue
                if not salli_skandit and any(c in skandit for c in sana): continue
                if not sana.isalpha(): continue
                hakusanat.append(sana)
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa {tiedostonimi} ei löydy.")
    return hakusanat

def laske_entropia(sanalista_koko, sanojen_maara):
    if sanalista_koko <= 0 or sanojen_maara <= 0: return 0
    return math.log2(sanalista_koko ** sanojen_maara)

def arvioi_vahvuus(entropia):
    if entropia < 45: return "Heikko"
    if entropia < 60: return "Kohtalainen"
    if entropia < 80: return "Vahva"
    return "Erit. vahva"

def generoi_salalause(sanalista, sanojen_lkm):
    if len(sanalista) >= sanojen_lkm:
        valitut = random.sample(sanalista, sanojen_lkm)
    else:
        valitut = [random.choice(sanalista) for _ in range(sanojen_lkm)]
    return "-".join(valitut).lower()

def main():
    tiedostonimi = r"C:\Users\stv9\Downloads\nykysuomensanalista2024.txt"
    print("\n--- SALALAUSEGENERAATTORI ---")
    
    # Asetukset
    skandit = input("Sallitaanko skandit (å, ä, ö)? (k/e): ").lower() == 'k'
    oletus_lkm = 5 if not skandit else 4
    
    try:
        min_p = int(input("Lyhyin sana (oletus 6): ") or "6")
        max_p = int(input("Pisin sana (oletus 11): ") or "11")
        sanojen_lkm = int(input(f"Sanojen määrä (suositus {oletus_lkm}): ") or str(oletus_lkm))
    except ValueError:
        min_p, max_p, sanojen_lkm = 6, 11, oletus_lkm

    sanalista = lue_sanalista(tiedostonimi, min_p, max_p, skandit)
    if not sanalista:
        print("Sanalista on tyhjä suodatusten jälkeen.")
        return

    entropia = laske_entropia(len(sanalista), sanojen_lkm)
    vahvuus_teksti = arvioi_vahvuus(entropia)

    tila = input("\nHaluatko (1) yksittäisiä ehdotuksia vai (2) listan 15 vaihtoehdosta? (1/2): ")

    if tila == "2":
        ehdotukset = [generoi_salalause(sanalista, sanojen_lkm) for _ in range(15)]
        
        # Lasketaan dynaaminen leveys pisimmän lauseen mukaan
        pisin_lause = max(len(e) for e in ehdotukset)
        sarake_leveys = max(50, pisin_lause + 2)
        
        # Otsikkorivin ja taulukon muotoilu
        otsikko = f"{'Nro':<4} | {'Salalause':<{sarake_leveys}} | {'Merkkejä':<8} | {'Bitit':<6} | {'Vahvuus'}"
        koko_leveys = len(otsikko) + 2
        
        print("\n" + "=" * koko_leveys)
        print(otsikko)
        print("-" * koko_leveys)
        
        for i, ehdotus in enumerate(ehdotukset, 1):
            pituus = len(ehdotus)
            print(f"{i:>2}.  | {ehdotus:<{sarake_leveys}} | {pituus:>3} m    | {int(entropia):>3} b  | {vahvuus_teksti}")
        
        print("=" * koko_leveys)
                
        valinta = input("\nValitse numero (1-15) kopioitavaksi tai 'e' poistuaksesi: ")
        if valinta.isdigit() and 1 <= int(valinta) <= 15:
            valittu_passu = ehdotukset[int(valinta)-1]
            pyperclip.copy(valittu_passu)
            print(f"\n*** '{valittu_passu}' kopioitu leikepöydälle! ***")
    else:
        while True:
            passu = generoi_salalause(sanalista, sanojen_lkm)
            print(f"\nEhdotus: {passu}")
            print(f"Vahvuus: {vahvuus_teksti} ({int(entropia)} bittiä)")
            if input("Kelpaako ja kopioidaanko? (k/e): ").lower() == 'k':
                pyperclip.copy(passu)
                print("\n*** Kopioitu leikepöydälle! ***")
                break

if __name__ == "__main__":
    main()