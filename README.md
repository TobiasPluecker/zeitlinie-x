# Zeitlinie X | Geschichte (@zeitlinie_x)

> **Automatisiertes Produktions-Repository für alternative Geschichts-Videos im 9:16 TikTok- & Shorts-Format.**

Dieses Repository dient als zentraler Hub für Skripte, Bild-/Video-Prompts, visuelle Styleguides und programmierbare Animations-Engines (Karten, Overlays, Effekte). Es ist modular aufgebaut, damit mehrere KI-Agenten und menschliche Editoren nahtlos zusammenarbeiten können.

---

## 📁 Repository-Struktur

```
zeitlinie-x/
├── .gitignore
├── README.md
├── STYLEGUIDE.md               # Visuelles & akustisches Designsystem (Farben, Schrift, Rhythmus)
│
├── episodes/                   # Alle Video-Episoden (nummeriert)
│   └── ep01_dunkirk_1940/
│       ├── meta.yaml           # Titel, TikTok-Captions, Hashtags, Status
│       ├── script_de.md        # Deutsches Sprecherskript mit Regieanweisungen
│       ├── script_en.md        # Englische Adaption (für internationalen Kanal)
│       ├── prompts.json        # Szenengenaue KI-Prompts (Midjourney, Flux, Kling, Runway)
│       └── assets/             # Generierte Karteneffekte, Grafiken & Overlays
│
├── engine/                     # Python-Engines zur programmierbaren Asset-Erstellung
│   ├── map_animator.py         # Erzeugt animierte, taktische 9:16 Front- und Kesselkarten
│   └── ...
│
└── templates/                  # Vorlagen für zukünftige Episoden
```

---

## 🚀 Workflow für neue Episoden (Multi-Agent Setup)

1. **Agent 1 (Researcher / Historian):**
   - Identifiziert den historischen Wendepunkt ("What if?").
   - Prüft historische Plausibilität & Kettenreaktion.
2. **Agent 2 (Scriptwriter):**
   - Erstellt `script_de.md` nach der TikTok-Retentions-Formel (Hook < 3s, Wende bei 12s, Call-to-Action am Ende).
   - Erstellt `script_en.md` für die spätere internationale Zweitverwertung.
3. **Agent 3 (Prompt Engineer & Visuals):**
   - Schreibt szenengenaue Bild- & Motion-Prompts in `prompts.json`.
4. **Agent 4 (Code Engine / Animation):**
   - Erzeugt animierte Truppenkarten & Grafiken via `engine/map_animator.py`.

---

## 🛠 Voraussetzungen
- Python 3.10+
- `matplotlib`, `imageio`, `Pillow`, `numpy`
