# Dateiname: XYPScript-Promptliste
# Version: V28
# Datum: 2025-04-06
# Uhrzeit: 17:05
# Dateispeichername: XYPScriptPromptListe.json

import tkinter as tk
from tkinter import messagebox
import os
import json
import pyperclip

VERSION = "V28"
DATA_FILE = "XYPScriptPromptListe.json"  # Fester Dateiname ohne Versionsnummer
data = []
checkbox_vars = []    # Wird im Bearbeiten-Modus genutzt
edit_widgets = []     # Wird im Bearbeiten-Modus genutzt
# Globales Dictionary zur Speicherung des Zustands jedes Eintrags im Anzeige-Modus.
# Der Schlüssel ist ein Tupel (bezeichner, prompt) und der Wert ist der Zustand:
# 0 = aktiv (Standard: oranger Hintergrund, schwarze Schrift)
# 1 = deaktiviert (Hintergrund: Formularhintergrund, Text: hellgrau)
# 2 = zum Löschen markiert (Hintergrund: rot, Text: weiß)
button_states = {}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

root = tk.Tk()
root.title("XYPScript-Promptliste")
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1600, screen_width)}x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False
all_selected = True

# Funktion zum Aktualisieren des Button-Aussehens anhand des Zustands
def update_button_appearance(btn, state):
    if state == 0:  # aktiv
        btn.config(bg="#FFA500", fg="#000000")  # Orange, schwarze Schrift
    elif state == 1:  # deaktiviert
        # Hintergrund: wie Formularhintergrund, hier "#1F1F1F", Schrift: hellgrau
        btn.config(bg="#1F1F1F", fg="#D3D3D3")
    elif state == 2:  # zum Löschen markiert
        btn.config(bg="#FF0000", fg="#FFFFFF")  # Rot, weiße Schrift

# GUI TOP (Header) ------------------------------------------------------------
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

# Eingabebereich (Frame 2 – jetzt vor dem Filterbereich) ---------------------
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

def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", content)
        status_var.set("Inhalt eingefügt")
    except Exception as e:
        status_var.set("Fehler beim Einfügen")

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

def add_entry():
    global save_required
    bez = bezeichner_var.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if bez and prompt:
        # Duplikatprüfung
        for entry in data:
            if entry['bezeichner'].lower() == bez.lower() and entry['prompt'].lower() == prompt.lower():
                status_var.set("Duplikat – nicht hinzugefügt")
                return
        data.append({"bezeichner": bez, "prompt": prompt})
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        status_var.set("Eintrag hinzugefügt – nicht gespeichert")
        save_required = True
        update_list()

def save_data():
    global save_required, edit_widgets
    # Im Bearbeiten-Modus werden Änderungen aus den Editier-Widgets übernommen
    if ansicht_var.get() == "bearbeiten":
        for widget in edit_widgets:
            idx = widget["index"]
            new_bez = widget["bezeichner_widget"].get().strip()
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

def delete_selected():
    global save_required
    # Erstelle eine Liste aller Einträge, die im Anzeige-Modus als "zum Löschen markiert" (state 2) gelten.
    to_delete = []
    for entry in data:
        key = (entry["bezeichner"], entry["prompt"])
        if button_states.get(key, 0) == 2:
            to_delete.append(entry["bezeichner"])
    if not to_delete:
        status_var.set("Keine Einträge zum Löschen markiert")
        return

    # Sicherheitsabfrage mit Anzeige der markierten Einträge
    msg = "Folgende Einträge werden gelöscht:\n\n" + "\n".join(to_delete) + "\n\nWirklich löschen?"
    # Verwende askyesnocancel (True = Ja, False = Nein, None = Abbrechen)
    ans = messagebox.askyesnocancel("Löschen bestätigen", msg)
    if ans is True:
        # Lösche alle Einträge, die den Zustand 2 haben
        data[:] = [entry for entry in data if button_states.get((entry["bezeichner"], entry["prompt"]), 0) != 2]
        # Entferne die entsprechenden Schlüssel aus button_states
        for key in list(button_states.keys()):
            if button_states[key] == 2:
                del button_states[key]
        save_required = True
        status_var.set("Markierte Einträge gelöscht – nicht gespeichert")
        update_list()
    elif ans is False:
        status_var.set("Löschvorgang abgebrochen (Nein)")
    else:
        status_var.set("Löschvorgang abgebrochen (Abbrechen)")

def copy_master_prompt():
    # Kopiert den ersten Prompt-Wert des ersten Eintrags, falls vorhanden
    if data:
        entry = data[0]
        if entry['prompt']:
            first_word = entry['prompt'].split(',')[0].strip()
            pyperclip.copy(first_word)
            status_var.set("Master Prompt kopiert")

def toggle_all():
    # Im Bearbeiten-Modus genutzt – hier nicht mehr relevant für Anzeige-Modus
    pass

def on_close():
    if save_required:
        if messagebox.askyesno("Speichern", "Liste wurde geändert. Jetzt speichern?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

tk.Button(btn_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Speichern", command=save_data, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Löschen", command=delete_selected, bg="red", fg="#FFFFFF").pack(side="left", padx=2)

# Filter- & Ansichtsfunktionen (Frame 3 – unter dem Eingabebereich) -----------
second_frame = tk.Frame(root, bg="#1F1F1F")
second_frame.pack(fill="x", pady=5)

ansicht_var = tk.StringVar(value="anzeige")
tk.Label(second_frame, text="Ansicht:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(10, 2))
tk.Radiobutton(second_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")
tk.Radiobutton(second_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")

filter_var = tk.StringVar()
tk.Label(second_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(20, 2))
filter_entry = tk.Entry(second_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left")
filter_var.trace_add("write", lambda *args: update_list())

tk.Button(second_frame, text="Copy Master", command=copy_master_prompt, bg="#FFA500", fg="#000000").pack(side="right", padx=5)

# Listendarstellung (Frame 4) ---------------------------------------------------
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

# Update List: Anzeige- und Bearbeiten-Modus -------------------------------------
def update_list():
    global edit_widgets
    # Lösche alle Widgets in der Liste
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    edit_widgets = []
    
    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]
    row_added = False

    for entry in data:
        # Kombiniere Bezeichner und Prompt (in Kleinbuchstaben) zur Filterung
        combined = f"{entry['bezeichner']} {entry['prompt']}".lower()
        if terms:
            if not any(term in combined for term in terms):
                continue
        
        row_added = True
        # Schlüssel zur Identifikation des Eintrags in button_states
        key = (entry["bezeichner"], entry["prompt"])
        # Standardzustand ist 0, falls noch nicht gesetzt
        state = button_states.get(key, 0)
        button_states[key] = state

        if ansicht_var.get() == "bearbeiten":
            # Im Bearbeiten-Modus wie bisher:
            row = tk.Frame(scrollable_frame, bg="#1F1F1F", relief="solid", bd=1)
            row.pack(fill="x", padx=5, pady=2, anchor="w")
            
            var = tk.BooleanVar()
            cb = tk.Checkbutton(row, variable=var, bg="#1F1F1F")
            cb.pack(side="left")
            checkbox_vars.append(var)

            bez_entry = tk.Entry(row, width=20, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            bez_entry.insert(0, entry['bezeichner'])
            bez_entry.pack(side="left", padx=(10, 5))

            prompt_text_widget = tk.Text(row, height=3, width=100, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            formatted_prompt = insert_linebreaks(entry['prompt'])
            prompt_text_widget.insert("1.0", formatted_prompt)
            prompt_text_widget.pack(side="left")

            edit_widgets.append({
                "index": data.index(entry),
                "bezeichner_widget": bez_entry,
                "prompt_widget": prompt_text_widget
            })
        else:
            # Im Anzeige-Modus: Jeder Eintrag wird als anklickbarer Button dargestellt.
            # Der Button zeigt den Bezeichner und den formatierten Prompt (mit Zeilenumbruch) an.
            btn_text = f"{entry['bezeichner']}\n{insert_linebreaks(entry['prompt'])}"
            btn = tk.Button(scrollable_frame, text=btn_text, justify="left", anchor="w", wraplength=1000)
            # Setze das Aussehen des Buttons anhand des Zustands
            update_button_appearance(btn, state)
            btn.pack(fill="x", padx=5, pady=2, anchor="w")

            # Definiere das Verhalten bei Klick:
            # Einzelklick: Wenn Zustand 0 (aktiv) wird zu 1 (deaktiviert)
            def on_single_click(event, key=key):
                current = button_states.get(key, 0)
                if current == 0:
                    button_states[key] = 1
                    update_button_appearance(event.widget, 1)
                # Falls bereits 2 (zum Löschen markiert) – tue nichts.
            btn.bind("<Button-1>", on_single_click)

            # Doppelklick: Wenn Zustand 1 (deaktiviert) wird zu 2 (zum Löschen markiert)
            def on_double_click(event, key=key):
                current = button_states.get(key, 0)
                if current == 1:
                    button_states[key] = 2
                    update_button_appearance(event.widget, 2)
            btn.bind("<Double-Button-1>", on_double_click)

    if not row_added:
        label = tk.Label(scrollable_frame, text="Keine Einträge vorhanden", bg="#1F1F1F", fg="#FFA500")
        label.pack(padx=5, pady=5)

update_list()
root.mainloop()

# Git-Anweisungen:
# git add XYPScript-Promptliste.py
# git commit -m "Version V28: Anzeigeeinträge als anklickbare Buttons mit Zustandswechsel (aktiv, deaktiviert, löschmarkiert) implementiert"
# git push
