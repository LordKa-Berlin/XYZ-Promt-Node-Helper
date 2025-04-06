# Dateiname: XYPScript-Promptliste
# Version: V30
# Datum: 2025-04-06
# Uhrzeit: 17:05
# Dateispeichername: XYPScriptPromptListe.json

import tkinter as tk
from tkinter import messagebox
import os
import json
import pyperclip
import uuid

VERSION = "V30"
DATA_FILE = "XYPScriptPromptListe.json"

# Daten laden
data = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
# Jedem Eintrag wird eine eindeutige ID zugewiesen (falls noch nicht vorhanden)
for entry in data:
    if "id" not in entry:
        entry["id"] = str(uuid.uuid4())

# Globale Zustands-Dictionaries für den Anzeige‑Modus:
# Für den Bezeichner-Button: 0 = aktiv, 1 = deaktiviert, 2 = zum Löschen markiert
row_bez_state = {}
# Für die einzelnen Wert-Buttons (Liste, gleiche Reihenfolge wie beim Split des Prompts)
row_value_states = {}

root = tk.Tk()
root.title("XYPScript-Promptliste")
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1600, screen_width)}x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False

# Listen und Widget-Sammlungen für den Bearbeiten‑Modus
checkbox_vars = []  # Checkbuttons pro Zeile
edit_widgets = []   # Liste von Dictionaries mit Referenzen zu den Editier-Widgets (Bezeichner und Prompt)

# Hilfsfunktion: Aktualisiert das Aussehen eines Buttons anhand eines Zustands (Anzeige‑Modus)
def update_button_appearance(btn, state):
    if state == 0:  # aktiv
        btn.config(bg="#FFA500", fg="#000000")  # Orange, schwarze Schrift
    elif state == 1:  # deaktiviert
        btn.config(bg="#1F1F1F", fg="#D3D3D3")    # Formularhintergrund, hellgraue Schrift
    elif state == 2:  # zum Löschen markiert
        btn.config(bg="#FF0000", fg="#FFFFFF")      # Rot, weiße Schrift

# Zeilenumbruchfunktion: Fügt nach ca. 130 Zeichen einen Umbruch ein
def insert_linebreaks(text, limit=130):
    parts = [p.strip() for p in text.split(",") if p.strip()]
    lines = []
    current = ""
    for part in parts:
        if len(current) + len(part) + 2 > limit:
            lines.append(current)
            current = part
        else:
            if current:
                current += ", " + part
            else:
                current = part
    if current:
        lines.append(current)
    return "\n".join(lines)

# ----------------- Funktionen für Eingabe, Speichern, Löschen -----------------

def add_entry():
    global save_required
    bez = bezeichner_var.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if bez and prompt:
        # Duplikatprüfung
        for entry in data:
            if entry["bezeichner"].lower() == bez.lower() and entry["prompt"].lower() == prompt.lower():
                status_var.set("Duplikat – nicht hinzugefügt")
                return
        new_entry = {"id": str(uuid.uuid4()), "bezeichner": bez, "prompt": prompt}
        data.append(new_entry)
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        status_var.set("Eintrag hinzugefügt – nicht gespeichert")
        save_required = True
        update_list()

def save_data():
    global save_required, edit_widgets
    # Im Bearbeiten‑Modus werden zuerst alle Änderungen aus den Widgets übernommen.
    if ansicht_var.get() == "bearbeiten":
        for widget in edit_widgets:
            idx = widget["index"]
            new_bez = widget["bez_widget"].get().strip()
            new_prompt_raw = widget["prompt_widget"].get("1.0", tk.END).strip()
            prompt_parts = [p.strip() for p in new_prompt_raw.replace("\n", " ").split(",") if p.strip()]
            normalized_prompt = ", ".join(prompt_parts)
            data[idx]["bezeichner"] = new_bez
            data[idx]["prompt"] = normalized_prompt
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    status_var.set("Liste gespeichert ✓")
    save_required = False
    update_list()

# Löschen-Funktion:
# Im Anzeige‑Modus werden komplette Zeilen gelöscht, wenn der Bezeichner-Button oder einzelne Werte (Button) markiert sind.
def delete_marked():
    global save_required, data, row_bez_state, row_value_states
    entries_to_delete = []
    entries_to_update = []
    message_lines = []
    for entry in data:
        eid = entry["id"]
        # Ganze Zeile löschen, wenn der Bezeichner im Anzeige‑Modus markiert ist (State 2)
        if row_bez_state.get(eid, 0) == 2:
            entries_to_delete.append(entry)
            message_lines.append(f"{entry['bezeichner']}: gesamter Eintrag")
        else:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            states = row_value_states.get(eid, [0]*len(values))
            marked = [values[i] for i, st in enumerate(states) if st == 2]
            if marked:
                message_lines.append(f"{entry['bezeichner']}: {', '.join(marked)}")
                new_values = [values[i] for i, st in enumerate(states) if st != 2]
                new_prompt = ", ".join(new_values)
                entries_to_update.append((entry, new_prompt))
    if not message_lines:
        status_var.set("Keine Einträge zum Löschen markiert")
        return
    msg = "Folgende Einträge/Teile werden gelöscht:\n" + "\n".join(message_lines) + "\n\nWirklich löschen?"
    ans = messagebox.askyesnocancel("Löschen bestätigen", msg)
    if ans is True:
        for entry in entries_to_delete:
            data.remove(entry)
            eid = entry["id"]
            if eid in row_bez_state: del row_bez_state[eid]
            if eid in row_value_states: del row_value_states[eid]
        for entry, new_prompt in entries_to_update:
            entry["prompt"] = new_prompt
            eid = entry["id"]
            values = [v.strip() for v in new_prompt.split(",") if v.strip()]
            row_value_states[eid] = [0]*len(values)
            row_bez_state[eid] = 0
        save_required = True
        status_var.set("Markierte Einträge aktualisiert/gelöscht – nicht gespeichert")
        update_list()
    elif ans is False:
        status_var.set("Löschvorgang abgebrochen (Nein)")
    else:
        status_var.set("Löschvorgang abgebrochen (Abbrechen)")

# Im Anzeige‑Modus: Kopiert aus einer Zeile alle aktiven (State 0) Wert-Buttons in die Zwischenablage.
def copy_master_prompt_from_row(eid):
    for entry in data:
        if entry["id"] == eid:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            states = row_value_states.get(eid, [0]*len(values))
            active_values = [values[i] for i, st in enumerate(states) if st == 0]
            if active_values:
                result = ", ".join(active_values)
                pyperclip.copy(result)
                status_var.set(f"Inhalt von '{entry['bezeichner']}' kopiert")
            break

# ----------------- Event-Handler für Anzeige-Modus -----------------

# Bezeichner-Button (Anzeige): Einzelklick kopiert alle aktiven Werte, Doppelklick markiert die gesamte Zeile
def bezeichner_single_click(event, eid):
    copy_master_prompt_from_row(eid)

def bezeichner_double_click(event, eid):
    row_bez_state[eid] = 2
    # Alle zugehörigen Werte ebenfalls auf "zum Löschen" (State 2) setzen
    for entry in data:
        if entry["id"] == eid:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            row_value_states[eid] = [2]*len(values)
            break
    update_list()

# Wert-Button (Anzeige): Einzelklick schaltet von aktiv (0) zu deaktiviert (1), Doppelklick: Toggle zwischen aktiv (0) und Löschmarkiert (2)
def value_single_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states) and states[index] == 0:
        states[index] = 1
        row_value_states[eid] = states
        update_button_appearance(btn, 1)

def value_double_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states):
        if states[index] == 2:
            states[index] = 0
        else:
            states[index] = 2
        row_value_states[eid] = states
        update_button_appearance(btn, states[index])

# ----------------- Event-Handler für Bearbeiten-Modus -----------------
# Im Bearbeiten‑Modus werden die Einträge als Editierfelder dargestellt.
# Für jede Zeile: Checkbutton, Bezeichner-Eintrag (mit grau hinterlegt/orange Schrift) und Prompt-Textfeld.
def create_bearbeiten_row(row_frame, entry, idx):
    eid = entry["id"]
    var = tk.BooleanVar()
    cb = tk.Checkbutton(row_frame, variable=var, bg="#1F1F1F")
    cb.pack(side="left")
    checkbox_vars.append(var)
    # Bezeichner-Eintrag: Grau hinterlegt, orange Schrift
    bez_entry = tk.Entry(row_frame, width=20, bg="gray", fg="#FFA500", insertbackground="#FFA500")
    bez_entry.insert(0, entry["bezeichner"])
    bez_entry.pack(side="left", padx=(10, 5))
    # Prompt-Textfeld (mehrzeilig) – Zeilenumbruch erhalten
    prompt_widget = tk.Text(row_frame, height=3, width=100, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
    formatted_prompt = insert_linebreaks(entry["prompt"])
    prompt_widget.insert("1.0", formatted_prompt)
    prompt_widget.pack(side="left")
    # Speichere die Widget-Referenzen, damit beim Speichern die Änderungen übernommen werden.
    edit_widgets.append({
        "index": idx,
        "bez_widget": bez_entry,
        "prompt_widget": prompt_widget
    })

# ----------------- GUI Aufbau -----------------

# Header (Top Bar)
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

# Eingabebereich (Frame 2)
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)
tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)
btn_frame = tk.Frame(entry_frame, bg="#1F1F1F")
btn_frame.grid(row=0, column=4, columnspan=3, padx=5)

tk.Button(btn_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Einfügen", command=lambda: (prompt_text.delete("1.0", tk.END), prompt_text.insert("1.0", pyperclip.paste())), bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Speichern", command=save_data, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Löschen", command=delete_marked, bg="red", fg="#FFFFFF").pack(side="left", padx=2)

# Filter & Ansicht (Frame 3)
second_frame = tk.Frame(root, bg="#1F1F1F")
second_frame.pack(fill="x", pady=5)
ansicht_var = tk.StringVar(value="anzeige")
tk.Label(second_frame, text="Ansicht:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(10,2))
tk.Radiobutton(second_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")
tk.Radiobutton(second_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")
filter_var = tk.StringVar()
tk.Label(second_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(20,2))
filter_entry = tk.Entry(second_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left")
filter_var.trace_add("write", lambda *args: update_list())
tk.Button(second_frame, text="Copy Master", command=lambda: None, bg="#FFA500", fg="#000000").pack(side="right", padx=5)

# Listendarstellung (Frame 4)
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg="#1F1F1F", highlightthickness=0)
scrollbar_y = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollbar_x = tk.Scrollbar(list_frame, orient="horizontal", command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg="#1F1F1F")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
canvas.pack(side="left", fill="both", expand=True)
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")

# ----------------- Update der Listendarstellung -----------------
def update_list():
    # Leere die bisherige Darstellung
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    # Leere Sammlungen für den Bearbeiten‑Modus
    del checkbox_vars[:]  
    del edit_widgets[:]
    global row_bez_state, row_value_states
    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]
    row_added = False
    for idx, entry in enumerate(data):
        combined = f"{entry['bezeichner']} {entry['prompt']}".lower()
        if terms and not any(term in combined for term in terms):
            continue
        row_added = True
        eid = entry["id"]
        # Für Anzeige-Modus: initialisiere Zustände, falls noch nicht vorhanden
        if eid not in row_bez_state:
            row_bez_state[eid] = 0
        values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
        if eid not in row_value_states:
            row_value_states[eid] = [0] * len(values)
        # Erstelle einen Rahmen für die Zeile
        row_frame = tk.Frame(scrollable_frame, bg="#1F1F1F", relief="solid", bd=1)
        row_frame.pack(fill="x", padx=5, pady=2, anchor="w")
        if ansicht_var.get() == "bearbeiten":
            # Bearbeiten-Modus: Checkbutton, Bezeichner-Eintrag (grau/orange) und Prompt-Textfeld
            create_bearbeiten_row(row_frame, entry, idx)
        else:
            # Anzeige-Modus: Bezeichner-Button und für jeden Wert einen eigenen Button
            bez_btn = tk.Button(row_frame, text=entry["bezeichner"], anchor="w", justify="left", padx=5, pady=2)
            update_button_appearance(bez_btn, row_bez_state[eid])
            bez_btn.pack(side="left")
            bez_btn.bind("<Button-1>", lambda e, eid=eid: bezeichner_single_click(e, eid))
            bez_btn.bind("<Double-Button-1>", lambda e, eid=eid: bezeichner_double_click(e, eid))
            for i, val in enumerate(values):
                val_text = insert_linebreaks(val)
                val_btn = tk.Button(row_frame, text=val_text, anchor="w", justify="left", wraplength=300)
                state = row_value_states[eid][i]
                update_button_appearance(val_btn, state)
                val_btn.pack(side="left", padx=2, pady=2)
                val_btn.bind("<Button-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_single_click(eid, idx, btn))
                val_btn.bind("<Double-Button-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_double_click(eid, idx, btn))
    if not row_added:
        label = tk.Label(scrollable_frame, text="Keine Einträge vorhanden", bg="#1F1F1F", fg="#FFA500")
        label.pack(padx=5, pady=5)

# Schließen-Handler
def on_close():
    if save_required:
        if messagebox.askyesno("Speichern", "Liste wurde geändert. Jetzt speichern?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_list()
root.mainloop()
