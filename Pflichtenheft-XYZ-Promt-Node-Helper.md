Natürlich! Hier ist das vollständige **Pflichtenheft für „XYPScript-Promptliste“** in Listenform – basierend auf deinem ursprünglichen Pflichtenheft, den erweiterten Anforderungen im Verlauf und allen Nachträgen:

---

## ✅ **Pflichtenheft: XYPScript-Promptliste (Stand V1.24)**

---

### 🧩 **Allgemeine Anforderungen**

- [x] **Header mit:**
  - Dateiname
  - Version (Variable `VERSION`)
  - Datum
  - Uhrzeit
  - Dateispeichername (mit `-` statt Punkt)
- [x] **Versionsanzeige im GUI** (rechts oben, dezent)
- [x] **Farbdesign:**
  - Hintergrundfarbe Formular: `#1F1F1F`
  - Buttonfarbe: `#FFA500`
  - Button-Schrift: `#000000`
  - Label-/Textfarbe: `#FFA500`
  - Textfeld-Hintergrund: `#000000`
- [x] **„Always on Top“ Funktion:** Checkbox oben rechts, **standardmäßig aus** (False)
- [x] Git-Anweisungen am Ende jedes vollständigen Scripts (commitfähig)

---

### 📥 **Eingabebereich**

- [x] Eingabefeld „Bezeichner“
- [x] Mehrzeiliges Eingabefeld für „Prompt“ (SCRIPT-XYZ-Prompt)
- [x] Button „Einfügen“: Inhalt aus Zwischenablage in Prompt-Feld
- [x] Button „Übernehmen“: Neuen Eintrag in die Liste übernehmen
- [x] Automatische Normalisierung der Prompts (Leerzeichen nach Komma)
- [x] Duplikatprüfung: Kein Eintrag bei gleicher Kombination Bezeichner + Prompt
- [x] Statusmeldung bei Duplikat

---

### 🔍 **Filter- & Ansichtsfunktionen**

- [x] Radiobuttons: Anzeige-Modus / Bearbeiten-Modus
- [x] Textfeld „Filter“
- [x] Checkbox „alle Wörter“ (filtert streng nach AND/OR)
- [x] Filter reagiert automatisch bei Eingabe
- [x] Filter bezieht sich auf Bezeichner + Prompt
- [x] Filterfeld über der Liste im GUI

---

### 🧾 **Listendarstellung**

#### Anzeige-Modus:
- [x] Checkbox pro Eintrag (zum Markieren)
- [x] Button mit Bezeichner:
  - [x] Kopiert Prompt-Wörter korrekt (nicht immer letzter!)
- [x] Prompt wird zeilenweise dargestellt mit:
  - [x] **Zeilenumbruch bei 130 Zeichen**
  - [x] **Kein** Trennzeichen „|“ mehr zwischen Wörtern

#### Bearbeiten-Modus:
- [x] Editierbares Feld für Bezeichner
- [x] Editierbares Feld für Prompt
- [ ] (offen) **Bearbeitete Inhalte werden gespeichert**
- [x] Checkbox zur Löschmarkierung

---

### ⚙️ **Buttons & Funktionen**

- [x] „Copy Master“: kopiert das **erste Prompt-Wort**
- [x] „Speichern“: speichert JSON-Datei
- [x] „Löschen“: löscht markierte Einträge nach Sicherheitsabfrage
- [x] „Alle abwählen“ / „Alle markieren“: Toggle-Button für Checkboxen
- [x] Hinweis (Statuszeile) bei jeder Aktion

---

### 🖱️ **Canvas / Anzeige**

- [x] Canvas mit dynamischem Inhalt
- [x] Vertikale Scrollbar
- [x] Horizontale Scrollbar (bei Bedarf)
- [x] Mausrad-Steuerung (MouseWheel-Support)
- [x] Rahmen (relief=solid) zwischen Einträgen
- [x] Responsive Layout (1600px Maximalbreite)

---

### 💾 **Speicher- und Schließlogik**

- [x] Speicherung beim Klick auf „Speichern“
- [x] Sicherheitsabfrage beim Schließen, wenn Änderungen nicht gespeichert
- [x] Eintrag wird nur gespeichert, wenn geändert

---

### ❓ Noch offen / Optional

- [ ] Bearbeitete Zeilen im **Bearbeiten-Modus speichern**
- [ ] Export-Funktion (z. B. `.txt`, `.csv`)
- [ ] Import externer JSON/CSV-Dateien
- [ ] Mehrsprachigkeit (DE/EN)

---

