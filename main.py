# main.py
# Salasanamoottorin komentorivikäyttöliittymä (CLI)
# Ajo: uv run main.py tai python main.py
# TV - 2026-03-22
# main.py
# Salasanamoottorin komentorivikäyttöliittymä (CLI)
# Tukee suoria argumentteja ja interaktiivista tilaa.

import logic
import sys
import argparse

def tulosta_otsikko():
    print("\n" + "="*45)
    print("   🔐 CLI-SALASANAMOOTTORI")
    print("="*45)

def suorita_generointi(maara, sanoja, skandit, vaikeus_min=0, vaikeus_max=100):
    """Yleisfunktio generoinnin ajamiseen ja tulostamiseen."""
    raakalista = logic.lue_sanalista_verkosta() or logic.lue_sanalista_tiedostosta("kotus_sanat.txt")
    
    if not raakalista:
        print("❌ Virhe: Sanalistaa ei voitu ladata.")
        return

    sanalista = logic.suodata_sanalista(raakalista, 3, 12, skandit, vaikeus_min, vaikeus_max)
    ehdotukset = logic.generoi_salalauseet(sanalista, sanoja, maara)
    
    entropia = logic.laske_entropia(len(sanalista), sanoja)
    vahvuus, ikoni = logic.arvioi_vahvuus(entropia)

    print(f"\n--- {maara} ehdotusta ({int(entropia)} b, {vahvuus} {ikoni}) ---")
    for i, e in enumerate(ehdotukset, 1):
        print(f"{i:>2}. {e}")
    print("="*45 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Suomenkielinen salalausegeneraattori.")
    
    # Määritellään valinnaiset argumentit
    parser.add_argument("n", type=int, nargs="?", help="Sanojen määrä per lause (esim. 5)")
    parser.add_argument("-c", "--count", type=int, default=10, help="Generoitavien lauseiden määrä (oletus 10)")
    parser.add_argument("-s", "--skandit", action="store_true", help="Salli skandinaaviset merkit (å, ä, ö)")
    parser.add_argument("-p", "--pin", type=int, help="Generoi PIN-koodi annetulla pituudella")
    parser.add_argument("-m", "--muunnos", action="store_true", help="Etsi aitoja sananmuunnoksia")

    args = parser.parse_args()

    # 1. Jos käyttäjä haluaa PIN-koodin
    if args.pin:
        luku = "".join(str(n) for n in logic.arvo_numerot(args.pin))
        print(f"\n🎲 Arvottu PIN ({args.pin} numeroa):")
        print(f"👉 {luku}\n")
        return

    # 2. Jos käyttäjä haluaa sananmuunnoksia
    if args.muunnos:
        raakalista = logic.lue_sanalista_verkosta() or logic.lue_sanalista_tiedostosta("kotus_sanat.txt")
        sanakirja = set(s.split('\t')[0].lower() for s in raakalista if s.strip())
        muunnos_lista = [s.split('\t')[0].lower() for s in raakalista if 3 <= len(s.split('\t')[0]) <= 8]
        
        print("\n🤪 Etsitään aitoja sananmuunnoksia...")
        loytynyt = 0
        while loytynyt < 5:
            s1, s2 = logic.random.sample(muunnos_lista, 2)
            m1, m2 = logic.tee_sananmuunnos(s1, s2)
            if m1 in sanakirja and m2 in sanakirja and m1 != s1:
                print(f"✅ {s1} {s2} -> {m1} {m2}")
                loytynyt += 1
        return

    # 3. Jos annettiin sanojen määrä (suora ajo)
    if args.n:
        suorita_generointi(args.count, args.n, args.skandit)
        return

    # 4. Interaktiivinen tila (jos ei argumentteja)
    tulosta_otsikko()
    print("[1] 🚀 Generoi 10 vakio-salalausetta (5 sanaa, ei skandeja)")
    print("[2] 🗣️ Generoi 10 foneettista tunnistetta (3 lyhyttä sanaa)")
    print("[3] 🎲 Arvo 6-numeroinen PIN-koodi")
    print("[q] Lopeta")
    
    valinta = input("\nValitse toiminto: ").lower()

    if valinta == "1":
        suorita_generointi(10, 5, False)
    elif valinta == "2":
        # Foneettiset: lyhyet sanat, ei vaikeita merkkejä
        suorita_generointi(10, 3, False, vaikeus_max=40)
    elif valinta == "3":
        luku = "".join(str(n) for n in logic.arvo_numerot(6))
        print(f"\n🎲 PIN: {luku}\n")
    else:
        print("Heippa!")

if __name__ == "__main__":
    main()