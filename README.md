
# Sedan-sihtaus: Salalausegeneraattori

Täm on Python-pohjainen työkalu vahvojen, suomenkielisten salalauseiden generointiin. Ohjelma hyödyntää Kotuksen nykysuomen sanalistaa ja laskee jokaiselle lauseelle teoreettisen entropian (bitit).

## Ominaisuudet
* **Dynaaminen sanasto**: Suodattaa sanat pituuden ja skandien mukaan.
* **Entropialaskenta**: Arvioi salasanan vahvuuden (Heikko -> Erit. vahva).
* **Leikepöytätuki**: Kopioi valitun salalauseen automaattisesti (`pyperclip`).
* **Dynaaminen muotoilu**: Tulostaa 15 vaihtoehdon listan siistissä taulukossa merkkimäärien kera.

## Käyttnotto (uv)

Ohjelma on optimoitu käytettäväksi [uv](https://github.com/astral-sh/uv)-työkalulla, joka hoitaa riippuvuudet automaattisesti eristetyssä ympäristössä.

### Ajo komennolla:
```bash
uv run salasanamoottori.py
