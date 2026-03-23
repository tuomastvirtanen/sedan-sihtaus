# logic.py
# Salasanamoottorin ydinlogiikka: matemaattiset funktiot ja sanalistan käsittely.
# Ei sisällä käyttöliittymäkoodeja.
# TV - 2026-03-22

import math
import random
import urllib.request
import os

def lue_sanalista_verkosta(url="https://kaino.kotus.fi/lataa/nykysuomensanalista2024.txt"):
    """Lataa tuoreimman sanalistan suoraan Kotuksen palvelimelta."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Virhe verkkolatauksessa: {e}")
        return None

def lue_sanalista_tiedostosta(tiedostonimi):
    """Lukee sanalistan paikallisesta tiedostosta (esim. varajärjestelmä)."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, tiedostonimi)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        print(f"Virhe tiedoston luvussa: {e}")
        return None

def suodata_sanalista(raakalista, min_len, max_len, salli_skandit, min_vk=0, max_vk=100):
    """Suodattaa sanalistan annettujen kriteerien mukaan."""
    hakusanat = []
    skandit_set = set("åäöÅÄÖ")
    
    for rivi in raakalista:
        osat = rivi.strip().split("\t")
        if not osat: continue
        
        sana = osat[0]
        if not (min_len <= len(sana) <= max_len): continue
        if not salli_skandit and any(c in skandit_set for c in sana): continue
        if not sana.isalpha(): continue
        
        # Tarkistetaan vaikeuskerroin
        vk = laske_vaikeuskerroin(sana)
        if not (min_vk <= vk <= max_vk): continue
        
        hakusanat.append(sana)
    return hakusanat

def laske_entropia(sanalista_koko, sanojen_maara):
    """Laskee teoreettisen entropian (bitit)."""
    if sanalista_koko <= 0 or sanojen_maara <= 0:
        return 0
    return math.log2(sanalista_koko**sanojen_maara)

def arvioi_vahvuus(entropia):
    """Palauttaa sanallisen arvion ja ikonin vahvuudesta."""
    if entropia < 45: return "Heikko", "🔴"
    if entropia < 60: return "Kohtalainen", "🟠"
    if entropia < 80: return "Vahva", "🟢"
    if entropia < 128: return "Erit. vahva", "🔵"
    return "AES-taso (murtamaton)", "⭐"

def laske_vaikeuskerroin(sana):
    """Laskee sanan vaikeuden 0-100 välillä."""
    score = len(sana) * 2
    if len(sana) > 12: score += 15
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
    """Luo n kpl salalauseita käyttäen SystemRandomia."""
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

def arvo_numerot(lkm):
    """Arpoo lkm satunnaista numeroa."""
    cryptogen = random.SystemRandom()
    return [cryptogen.randint(0, 9) for _ in range(lkm)]