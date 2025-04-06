# Dateiname: XYPScript-Promptliste
# Version: V29
# Datum: 2025-04-06
# Uhrzeit: 17:05
# Dateispeichername: XYPScriptPromptListe.json

import tkinter as tk
from tkinter import messagebox
import os
import json
import pyperclip
import uuid

VERSION = "V29"
DATA_FILE = "XYPScriptPromptListe.json"

# Daten laden
data = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
# Für jeden Eintrag wird eine eindeutige ID generiert (falls noch nicht vorhanden)
for entry in data:
    if "id" not in entry:
        entry["id"] = str(uuid.uuid4())

# Globale Zustands-Dictionaries (pro Zeile, identifiziert über entry["id"]):
# Für den Bezeichner-Button: 0 = aktiv, 1 = deaktiviert, 2 = zum Löschen markiert
row_bez_state = {}   
# Für die einzelnen Werte (Liste, gleiche Reihenfolge wie beim Split des Prompts)
row_value_states = {}  

root = tk.Tk()
root.title("XYPScript-Promptliste")
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1600, screen_width)}x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False

# Hilfsfunktion: Setzt die optische Darstellung eines Buttons anhand des Zustands.
def update_button_appearance(btn, state):
    if state == 0:  # aktiv
        btn.config(bg="#FFA500", fg="#000000")
    elif state == 1:  # deaktiviert
        btn.config(bg="#1F1F1F", fg="#D3D3D3")
    elif state == 2:  # zum Löschen markiert
        btn.config(bg="#FF0000", fg="#FFFFFF")

# Zeilenumbruchfunktion: Teilt einen Text (mit Komma getrennt) so, dass nach ca. 130 Zeichen ein Umbruch erfolgt.
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

# Eingabe-Funktionen (analog zu früheren Versionen)
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
    global save_required
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    status_var.set("Liste gespeichert ✓")
    save_required = False
    update_list()

# Löschen-Funktion:
# - Falls der Bezeichner (der ganze Eintrag) markiert ist (State 2), wird der gesamte Eintrag gelöscht.
# - Ansonsten: Es werden nur die Werte entfernt, die zum Löschen markiert sind.
def delete_marked():
    global save_required, data, row_bez_state, row_value_states
    entries_to_delete = []
    entries_to_update = []  # Liste von (entry, neuer Prompt) für Teillöschungen
    message_lines = []
    for entry in data:
        eid = entry["id"]
        # Ganze Zeile löschen, wenn der Bezeichner markiert ist.
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

# Kopiert den Inhalt aller aktiven (State 0) Wert-Buttons der Zeile in die Zwischenablage.
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

# Event-Handler für den Bezeichner-Button:
def bezeichner_single_click(event, eid):
    copy_master_prompt_from_row(eid)

def bezeichner_double_click(event, eid):
    # Markiere den Bezeichner und alle zugehörigen Wert-Buttons als "zum Löschen" (State 2)
    row_bez_state[eid] = 2
    values = None
    for entry in data:
        if entry["id"] == eid:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            break
    if values is not None:
        row_value_states[eid] = [2]*len(values)
    update_list()

# Event-Handler für die Wert-Buttons:
def value_single_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states) and states[index] == 0:
        states[index] = 1
        row_value_states[eid] = states
        update_button_appearance(btn, 1)

def value_double_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states):
        # Falls bereits zum Löschen markiert, wieder aktivieren; sonst als zum Löschen markieren.
        if states[index] == 2:
            states[index] = 0
        else:
            states[index] = 2
        row_value_states[eid] = states
        update_button_appearance(btn, states[index])

# GUI – Header
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

# Update der Listendarstellung im Anzeige-Modus
def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]
    row_added = False
    for entry in data:
        combined = f"{entry['bezeichner']} {entry['prompt']}".lower()
        if terms and not any(term in combined for term in terms):
            continue
        row_added = True
        eid = entry["id"]
        # Initialisiere Zustände, falls noch nicht vorhanden.
        if eid not in row_bez_state:
            row_bez_state[eid] = 0
        values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
        if eid not in row_value_states:
            row_value_states[eid] = [0] * len(values)
        # Zeilenrahmen
        row_frame = tk.Frame(scrollable_frame, bg="#1F1F1F", relief="solid", bd=1)
        row_frame.pack(fill="x", padx=5, pady=2, anchor="w")
        # Bezeichner-Button
        bez_btn = tk.Button(row_frame, text=entry["bezeichner"], anchor="w", justify="left")
        update_button_appearance(bez_btn, row_bez_state[eid])
        bez_btn.pack(side="left", padx=5, pady=2)
        bez_btn.bind("<Button-1>", lambda e, eid=eid: bezeichner_single_click(e, eid))
        bez_btn.bind("<Double-Button-1>", lambda e, eid=eid: bezeichner_double_click(e, eid))
        # Wert-Buttons
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
