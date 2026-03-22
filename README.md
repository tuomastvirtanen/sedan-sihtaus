# 🔐 Sedan-sihtaus: Salalausegeneraattori

Tämä on Python-pohjainen työkalu vahvojen, suomenkielisten salalauseiden generointiin. Ohjelma hyödyntää Kotuksen nykysuomen sanalistaa ja tarjoaa matemaattisesti perustellun arvion salasanan murtovarmuudesta (entropia).

## 🌍 Selainversio
Sovellus on ajettavissa suoraan selaimessa (myös mobiilissa):
👉 **[salasanamoottori.streamlit.app](https://salasanamoottori.streamlit.app)**

---

## ✨ Ominaisuudet
* **Dynaaminen sanasto**: Hyödyntää Kotuksen nykysuomen sanalistaa (sisältää n. 94 000 sanaa).
* **Tunniste-tila (🗣️)**: Generoi foneettisesti selkeitä ja lyhyitä sanoja (2–5 kpl), jotka on helppo sanoa ääneen.
* **Vaikeusasteen hienosäätö**: Suodata sanoja kirjoitus- ja ääntämisvaikeuden perusteella (0–100).
* **Entropialaskenta**: Laskee teoreettisen bitin määrän (esim. 128 bittiä vastaa AES-standardin perustasoa).
* **Moderni teknologia**: Selainversio toteutettu Streamlitillä, CLI-versio optimoitu `uv`-työkalulle.
* **Sananmuunnokset**: Ensimmäinen kehitysversio sananmuunnoskoneesta, molempien sanojen tulee löytyä Kotus-sanastosta. 
---

## 📊 Mitä bitit tarkoittavat käytännössä?

Entropia kuvaa sitä, kuinka monta kertaa hyökkääjän on keskimäärin kokeiltava eri vaihtoehtoja ennen kuin salasana murtuu.

| Entropia (bittiä) | Vastaa suunnilleen... | Turvataso (Offline-hyökkäys) |
| :--- | :--- | :--- |
| **~20–30 b** | 5 satunnaista merkkiä tai 1 yleinen sana | **Heikko:** Murtuu sekunneissa millä tahansa laitteella. |
| **~45 b** | 8 merkkiä (pieniä/isoja/numeroita) | **Rajatapaus:** Murtuu tunneissa tehokkaalla näytönohjaimella. |
| **~60 b** | **4 suomenkielistä sanaa** | **Vahva:** Vaatii jo huomattavaa laskentatehoa ja aikaa. |
| **~80 b** | **5–6 suomenkielistä sanaa** | **Sotilastaso:** Murtaminen on käytännössä mahdotonta ilman supertietokonetta. |
| **128 b+** | **8–10 suomenkielistä sanaa** | **AES-taso:** Matemaattisesti murtamaton universumin eliniän aikana. |



---

## 🛠️ Paikallinen käyttö (CLI)

Ohjelma on optimoitu käytettäväksi [uv](https://github.com/astral-sh/uv)-työkalulla.

### Ajo komennolla:
```bash
uv run salasanamoottori.py
```

```mermaid
graph TD
    subgraph "Salasanan Entropia vs. Brute-force Aika"
        A[Aika murtaa] -->|Log asteikko| B{ }
        B --> |1 m| C1[40b: Sekunteja]
        B --> |1 v| C2[55b: Vuosia]
        B --> |1000 v| C3[70b: Vuosituhansia]
        B --> |1 mrd v| C4[90b: Ikuisuus]
        B --> |Universumin ikä| C5[128b: Mahdoton]
        
        X[Entropia] -->|bittiä| D1(20)
        D1 -->|45| D2(Suositus min)
        D2 -->|60| D3(Vahva)
        D3 -->|80| D4(Sotilastaso)
        D4 -->|128| D5(AES)
    
        P20( ) -- Heikko --> P45( )
        P45( ) -- Kohtalainen --> P60( )
        P60( ) -- Vahva --> P80( )
        P80( ) -- Erit. vahva --> P128( )
    end
    
    style A fill:#fff,stroke:#fff;
    style X fill:#fff,stroke:#fff;
    style P20 fill:#f00,stroke:#f00;
    style P45 fill:#ff0,stroke:#ff0;
    style P60 fill:#0f0,stroke:#0f0;
    style P80 fill:#00f,stroke:#00f;
    style P128 fill:#808,stroke:#808;
```
