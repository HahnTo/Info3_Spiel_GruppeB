# Info3_Spiel – Monster Jump

### Ein Studienprojekt von Tobias Hahn, Lutz Morath und Jonas Uzelac

---

## Spielbeschreibung

**Monster Jump** ist ein 2D Platformer, bei dem zwei Spieler entweder an einer Tastatur oder im Multiplayer gemeinsam spielen.

Ziel ist es, kooperativ einen Ausweg aus dem Level zu finden, indem Rätsel gelöst und Hindernisse überwunden werden.

---

## Steuerung

- **Spieler 1:** WAD Tasten  
- **Spieler 2:** Pfeiltasten  

---

## Ziel des Spiels

Um ein Level zu beenden, müssen **beide Spieler gleichzeitig auf der selben oder zwei unterschiedlichen Flaggen stehen**.

---

## Gameplay-Elemente

- Einige Blöcke sind **verschiebbar**
- Andere Blöcke lassen sich über **Buttons bewegen**
- **Stacheln** beenden den Run

---

## Multiplayer

Für den Online Multiplayer gilt:

- Ein Spieler hostet einen Server
- Der zweite Spieler tritt über die **lokale IP-Adresse** des Hosts bei

---

## Level

- 3 lokale Level
- 1 Multiplayer Level 

---

## Installation & Voraussetzungen

Benötigt werden:

- Python 3.10 oder neuer
- Pakete:
  - `pygame`
  - `pytmx`

Installation:

```bash

git clone https://github.com/HahnTo/Info3_Spiel_GruppeB.git
cd Info3_Spiel_GruppeB

pip install -r requirements.txt
```

---
 
## Spiel starten
 
```bash
python -m src.gamecontroller
```

## Projektstruktur
 
```text
.
├── Dokumentation.pdf
├── README.md
├── requirements.txt
├── src/
│   ├── gamecontroller.py      # Einstiegspunkt, Spielschleife, Kollisionen, Zustandswechsel
│   ├── gamestatemanager.py    # Verwaltung des aktuellen Spielzustands
│   ├── config.py              # Konstanten (Fenstergröße, FPS, Pfade), lokale IP
│   ├── player.py              # Spieler: Physik, Animation, Netzwerk-Interpolation
│   ├── obstacle.py            # Hindernisse (Plattformen, Buttons, Stacheln, Flagge, …)
│   ├── levelloader.py         # Erzeugt Hindernisse aus den TMX-Maps
│   ├── inputhandler.py        # Tastatureingaben für Spiel und Menüs
│   ├── inputfield.py          # Eingabefeld (IP-Adresse)
│   ├── button.py              # Menü-Button
│   ├── spritesheet.py         # Ausschneiden von Animationsframes
│   ├── states/
│   │   ├── state.py           # Basisklasse für Zustände
│   │   ├── level.py           # Spielzustand: Level, Timer, Netzwerk-Sync
│   │   ├── menus/             # Start-, Level-, Multiplayer-, End- und Pausemenü
│   │   └── loadings/          # Warte- und Verbindungsbildschirm
│   ├── server/
│   │   ├── server.py          # TCP-Server
│   │   └── networkclient.py   # TCP-Client
│   ├── assets/                # Level (map_1–map_4.tmx), Tilesets (.tsx) und Schriftart
│   └── graphics/              # Grafiken (Karte, Spielfiguren)
└── tests/                     # pytest-Tests
```
---

**Viel Spaß beim Spielen wünschen Tobias, Lutz und Jonas!**
