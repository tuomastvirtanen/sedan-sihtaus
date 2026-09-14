# Sedan-sihtaus: salalausegeneraattori

Python-ohjelma suomenkielisten salalauseiden generointiin. Ohjelma käyttää Kotuksen nykysuomen sanalistaa ja laskee generoiduille salalauseille teoreettisen entropian sanaston koon ja tehtyjen valintojen perusteella.

Nimi **sedan-sihtaus** on ohjelman ensimmäisen kehitysversion ensimmäinen satunnaisesti generoitu sanapari.

## Selainversio

Ohjelmaa voi käyttää selaimessa:

**https://salasanamoottori.streamlit.app**

Selainkäyttöliittymä on toteutettu Streamlitillä.

---

## Toiminnot

* **Salalausegeneraattori**
  Generoi Kotuksen nykysuomen sanalistasta satunnaisia sanoja haluttuun entropiatasoon asti.

* **Tunniste-tila**
  Generoi 2–5 lyhyttä ja foneettisesti selkeää sanaa esimerkiksi suullisesti välitettäviksi tunnisteiksi.

* **Sanaston suodatus**
  Sanoja voidaan rajata kirjoitus- ja ääntämisvaikeuden perusteella asteikolla 0–100.

* **Entropialaskenta**
  Laskee generoidun salalauseen teoreettisen entropian bitteinä käytettävissä olevan sanaston ja satunnaisten valintojen määrän perusteella.

* **PIN-koodit**
  Generoi halutun pituisia satunnaisia numerokoodeja.

* **Sananmuunnokset**
  Kokeellinen toiminto kahden Kotuksen sanalistasta löytyvän sanan muuntamiseen.

---

## Entropia

Jos jokainen sana valitaan toisista valinnoista riippumatta ja tasaisesti sanastosta, yhden sanan tuottama entropia on

```text
log2(sanaston koko)
```

ja `n` sanan salalauseen entropia

```text
n × log2(sanaston koko)
```

Esimerkiksi 16 bitin entropia tarkoittaa noin `2^16` mahdollista yhdistelmää ja 64 bitin entropia noin `2^64` yhdistelmää.

Laskettu arvo kuvaa generaattorin tuottaman salalauseen **teoreettista entropiaa**. Se ei sellaisenaan kerro, kuinka kauan tietyn salasanan murtaminen kestää. Käytännön murtamisnopeuteen vaikuttavat muun muassa käytetty salasanatiiviste, sen asetukset, hyökkääjän käytettävissä oleva laskentateho sekä se, tietääkö hyökkääjä salasanan generointimenetelmän.

Entropialaskenta olettaa, että sanat on valittu ohjelman satunnaisgeneraattorilla. Käyttäjän itse valitsemaan tai muokkaamaan salalauseeseen samaa laskentaa ei voida suoraan soveltaa.

---

## Sanasto

Ohjelma käyttää **Kotuksen nykysuomen sanalistaa**, jossa on noin 94 000 hakusanaa.

Generoinnissa käytettävän sanaston koko voi olla tätä pienempi, jos sanoja suodatetaan esimerkiksi pituuden tai vaikeusasteen perusteella. Entropia lasketaan siitä sanajoukosta, josta satunnainen valinta todellisuudessa tehdään.

---

## Paikallinen käyttö

Ohjelmaa voi ajaa komentoriviltä Pythonilla. Projekti on määritetty toimimaan myös `uv`:n kanssa.

```bash
uv run salasanamoottori.py
```

Selainversio käyttää Streamlitiä.
