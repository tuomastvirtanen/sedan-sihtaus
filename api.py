# sedan-sihtaus API - FastAPI-pohjainen rajapinta salalausegeneraattorille
# tv - 2026-03-22

from fastapi import FastAPI, Query
import logic

app = FastAPI(title="Salasanamoottori API", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Tervetuloa Salasanamoottori API:in"}

@app.get("/generoi")
def generoi(maara: int = 10, sanoja: int = 5, skandit: bool = False):
    raakalista = logic.lue_sanalista_verkosta() or logic.lue_sanalista_tiedostosta("kotus_sanat.txt")
    sanalista = logic.suodata_sanalista(raakalista, 6, 12, skandit)
    ehdotukset = logic.generoi_salalauseet(sanalista, sanoja, maara)
    return {"tyyppi": "salalause", "tulokset": ehdotukset}

@app.get("/pin")
def hae_pin(pituus: int = Query(4, ge=4, le=12)):
    luku = "".join(str(n) for n in logic.arvo_numerot(pituus))
    return {"tyyppi": "pin", "tulos": luku}

@app.get("/muunnos")
def hae_muunnos(lkm: int = 5):
    # Tähän logic.py:n sananmuunnoslogiikka JSON-muodossa
    # (Voit siirtää main.py:ssä olevan loopin logic.py:hyn funktioksi, 
    # jolloin API voi kutsua sitä yhdellä rivillä)
    return {"message": "Sananmuunnosrajapinta valmiina"}