# main.py
# Salasanamoottorin komentorivikäyttöliittymä (CLI)
# Ajo: uv run main.py tai python main.py
# TV - 2026-03-22

import logic
import sys

def main():
    print("\n" + "="*40)
    print("   NIGHT AGENT - SALALAUSEGENERAATTORI")
    print("="*40)

    # 1. Lataa sanalista (logic hoitaa verkon tai paikallisen)
    raakalista = logic.lue_sanalista_verkosta()
    if not raakalista:
        raakalista = logic.lue_sanalista_tiedostosta("kotus_sanat.txt")
    
    if not raakalista:
        print("Virhe: Sanalistaa ei voitu ladata. Tarkista yhteys.")
        sys.exit(1)

    # 2. Perusasetukset (nopeaan käyttöön oletukset)
    print("\n[1] Generoi 10 vakio-salalausetta (oletus)")
    print("[2] Generoi 10 tunnistetta (foneettisesti selkeät)")
    print("[3] Mukautettu generointi")
    
    valinta = input("\nValitse toiminto (1-3, oletus 1): ") or "1"

    if valinta == "1":
        sanalista = logic.suodata_sanalista(raakalista, 6, 11, False)
        ehdotukset = logic.generoi_salalauseet(sanalista, 5, 10)
    
    elif valinta == "2":
        vaikeat = set("bcfgqwxzåäö")
        sanalista = logic.suodata_sanalista(raakalista, 3, 7, False)
        tunniste_lista = [s for s in sanalista if not any(c in vaikeat for c in s.lower())]
        ehdotukset = logic.generoi_salalauseet(tunniste_lista, 3, 10)

    else:
        # Mukautetut syötteet
        skandit = input("Sallitaanko skandit (k/e): ").lower() == "k"
        lkm = int(input("Sanojen määrä (esim. 4-6): ") or "5")
        sanalista = logic.suodata_sanalista(raakalista, 5, 12, skandit)
        ehdotukset = logic.generoi_salalauseet(sanalista, lkm, 10)

    # 3. Tulostus
    entropia = logic.laske_entropia(len(sanalista), 5 if valinta != "3" else lkm)
    vahvuus, ikoni = logic.arvioi_vahvuus(entropia)

    print(f"\n--- Ehdotukset ({int(entropia)} b, {vahvuus} {ikoni}) ---")
    for i, e in enumerate(ehdotukset, 1):
        print(f"{i:>2}. {e}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()