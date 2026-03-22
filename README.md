# Sedan-sihtaus: Salalausegeneraattori

Tämä on Python-pohjainen työkalu vahvojen, suomenkielisten salalauseiden generointiin. Ohjelma hyödyntää Kotuksen nykysuomen sanalistaa ja laskee jokaiselle lauseelle teoreettisen entropian (bitit).

## Ominaisuudet
* **Dynaaminen sanasto**: Lataa sanalistan suoraan Kotuksen palvelimelta ja suodattaa sanat pituuden mukaan.
* **Entropialaskenta**: Arvioi salasanan vahvuuden (Heikko -> Erit. vahva).
* **Leikepöytätuki**: Kopioi valitun salalauseen automaattisesti (`pyperclip`).
* **Dynaaminen muotoilu**: Tulostaa 15 vaihtoehdon listan siistissä taulukossa.

## Käyttöönotto (uv)

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
        
        P98(Sinun 98b) -.-> P80
    end
    
    style A fill:#fff,stroke:#fff;
    style X fill:#fff,stroke:#fff;
    style P20 fill:#f00,stroke:#f00;
    style P45 fill:#ff0,stroke:#ff0;
    style P60 fill:#0f0,stroke:#0f0;
    style P80 fill:#00f,stroke:#00f;
    style P128 fill:#808,stroke:#808;
    style P98 fill:#0ff,stroke:#000,stroke-width:2px,stroke-dasharray: 5 5;
```
