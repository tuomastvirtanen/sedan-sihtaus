# ohjelma lukee kotimaisten kielenten keskuksen julkaisemaa sanalistaa
# Sanatietue koostuu seuraavista tiedoista: 1) hakusana, 2) homonymia, 3) sanaluokka ja 4) taivutus.
# TV - 2026-03-21

# /// script
# dependencies = [
#   "pyperclip",
# ]
# ///

import random
import math
import pyperclip
import urllib.request
import sys

def lue_sanalista_verkosta(url, min_pituus, max_pituus, salli_skandit):
    """Lataa sanalistan suoraan Kotuksen palvelimelta ja suodattaa sen."""
    hakusanat = []
    skandit = set("åäöÅÄÖ")
    
    try:
        print(f"Ladataan sanalistaa osoitteesta: {url}...")
        # Asetetaan User-Agent, jotta pyyntö näyttää selaimelta (hyvä tapa)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            # Kotuksen lista on UTF-8 muodossa
            data = response.read().decode('utf-8')
            
            for rivi in data.splitlines():
                osat = rivi.strip().split('\t')
                if not osat:
                    continue
                
                sana = osat[0]
                
                # Suodatukset
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
    # Kotuksen suora URL nykysuomen sanalistalle
    url = "https://kaino.kotus.fi/lataa/nykysuomensanalista2024.txt"
    
    print("\n" + "="*30)
    print("   SALALAUSEGENERAATTORI")
    print("="*30)
    
    # Asetusten kysely
    skandit = input("Sallitaanko skandit (å, ä, ö)? (k/e): ").lower() == 'k'
    
    # Dynaaminen suositus sanamäärälle
    oletus_lkm = 5 if not skandit else 4
    
    try:
        min_p = int(input("Lyhyin sanan pituus (oletus 6): ") or "6")
        max_p = int(input("Pisin sanan pituus (oletus 11): ") or "11")
        sanojen_lkm = int(input(f"Sanojen määrä lauseessa (suositus {oletus_lkm}): ") or str(oletus_lkm))
    except ValueError:
        print("Virheellinen syöte, käytetään oletusarvoja.")
        min_p, max_p, sanojen_lkm = 6, 11, oletus_lkm

    # Haetaan data
    sanalista = lue_sanalista_verkosta(url, min_p, max_p, skandit)
    
    if not sanalista:
        print("Sanalistaa ei voitu ladata. Tarkista verkkoyhteys.")
        sys.exit(1)

    entropia = laske_entropia(len(sanalista), sanojen_lkm)
    vahvuus_teksti = arvioi_vahvuus(entropia)

    print(f"\nSana-avaruus: {len(sanalista)} sanaa.")
    print(f"Teoreettinen vahvuus: {int(entropia)} bittiä ({vahvuus_teksti}).")

    tila = input("\nHaluatko (1) yksittäisiä ehdotuksia vai (2) listan 15 vaihtoehdosta? (1/2): ")

    if tila == "2":
        ehdotukset = [generoi_salalause(sanalista, sanojen_lkm) for _ in range(15)]
        
        # Lasketaan dynaaminen leveys pisimmän lauseen mukaan
        pisin_lause_len = max(len(e) for e in ehdotukset)
        sarake_leveys = max(50, pisin_lause_len + 2)
        
        otsikko = f"{'Nro':<4} | {'Salalause':<{sarake_leveys}} | {'Merkkejä':<9} | {'Bitit':<6} | {'Vahvuus'}"
        print("\n" + "=" * len(otsikko))
        print(otsikko)
        print("-" * len(otsikko))
        
        for i, ehdotus in enumerate(ehdotukset, 1):
            print(f"{i:>2}.  | {ehdotus:<{sarake_leveys}} | {len(ehdotus):>3} m     | {int(entropia):>3} b  | {vahvuus_teksti}")
        
        print("=" * len(otsikko))
        
        valinta = input("\nValitse numero (1-15) kopioitavaksi tai 'e' poistuaksesi: ")
        if valinta.isdigit() and 1 <= int(valinta) <= 15:
            valittu_salalause = ehdotukset[int(valinta)-1]
            pyperclip.copy(valittu_salalause)
            print(f"\n*** '{valittu_salalause}' kopioitu leikepöydälle! ***")
            
    else:
        while True:
            salalause = generoi_salalause(sanalista, sanojen_lkm)
            print(f"\nEhdotus: {salalause}")
            print(f"Pituus: {len(salalause)} merkkiä | Vahvuus: {int(entropia)} b ({vahvuus_teksti})")
            
            vastaus = input("\nKelpaako ja kopioidaanko leikepöydälle? (k/e/uusi): ").lower()
            if vastaus == 'k':
                pyperclip.copy(salalause)
                print("\n*** Kopioitu leikepöydälle! ***")
                break
            elif vastaus == 'e':
                break

if __name__ == "__main__":
    main()