# Dateiname: XYPScript-Promptliste
# Version: V1.1
# Datum: 2025-04-05
# Uhrzeit: 17:00
# Dateispeichername: XYPScript-Promptliste-V1-1
# Beschreibung: GUI zur Eingabe, Anzeige, Filterung und Bearbeitung von Bezeichnern mit zugehörigen Prompts. Speicherung im JSON-Format,
# Editierbarkeit, Filterfunktion, Copy in Zwischenablage (nur Prompt), Mehrfachlöschung mit Sicherheitsabfrage, Always on Top, Version sichtbar.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip
import sys

# Automatische Installation von pyperclip falls nicht vorhanden
try:
    import pyperclip
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

# Version
VERSION = "V1.1"

# JSON-Dateipfad
DATA_FILE = "XYPScriptPromptListe.json"

# Daten laden
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# Daten speichern
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Hauptfenster
root = tk.Tk()
root.title("XYPScript-Promptliste")
root.geometry("1600x600")
root.configure(bg="#1F1F1F")

# Always on Top Checkbox
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(anchor="ne", padx=10, pady=5)

# Versionsanzeige
version_label = tk.Label(root, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500", anchor="e")
version_label.pack(anchor="ne", padx=10)

# Eingabe-Frame
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10)

# Funktion für Bezeichnerliste
bezeichner_liste = sorted(list(set([item['bezeichner'] for item in data])))

# Bezeichner Combobox
tk.Label(entry_frame, text="Bezeichner:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=0, sticky="e")
bezeichner_var = tk.StringVar()
bezeichner_combo = ttk.Combobox(entry_frame, textvariable=bezeichner_var, values=bezeichner_liste, width=30)
bezeichner_combo.grid(row=0, column=1, padx=5)
bezeichner_combo.bind('<KeyRelease>', lambda e: bezeichner_combo.event_generate('<Down>'))

# Prompt (mehrzeilig)
tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=2, sticky="e")
prompt_entry = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500")
prompt_entry.grid(row=0, column=3, padx=5)

# Eintrag übernehmen

def add_entry():
    bez = bezeichner_var.get().strip()
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if not bez or not prompt:
        messagebox.showwarning("Fehler", "Bezeichner und Prompt dürfen nicht leer sein.")
        return
    if len(bez) > 50 or len(prompt) > 500:
        messagebox.showwarning("Zu lang", "Bezeichner max 50 Zeichen, Prompt max 500 Zeichen.")
        return
    data.append({"bezeichner": bez, "prompt": prompt})
    save_data()
    bezeichner_combo.set("")
    prompt_entry.delete("1.0", tk.END)
    update_list()
    bezeichner_combo['values'] = sorted(list(set([item['bezeichner'] for item in data])))

tk.Button(entry_frame, text="Übernehmen", bg="#FFA500", fg="#000000", command=add_entry).grid(row=0, column=4, padx=10)

# Filter
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=10)

filter_label = tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500")
filter_label.grid(row=0, column=0, sticky="e")

filter_entry = tk.Entry(filter_frame, width=50, bg="#000000", fg="#FFA500")
filter_entry.grid(row=0, column=1, padx=5)

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)

# Listbox mit Scrollbar
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, width=120, height=10, bg="#000000", fg="#FFA500", selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

# Filterfunktion

def update_list():
    listbox.delete(0, tk.END)
    terms = [t.strip().lower() for t in filter_entry.get().split(",") if t.strip()]
    for item in data:
        combined = f"{item['bezeichner']}: {item['prompt']}"
        hit = False
        if terms:
            values = f"{item['bezeichner']} {item['prompt']}".lower()
            if all_words_var.get():
                hit = all(term in values for term in terms)
            else:
                hit = any(term in values for term in terms)
        else:
            hit = True
        if hit:
            listbox.insert(tk.END, combined)

update_list()

# Copy-Funktion

def copy_prompt():
    try:
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        entry = listbox.get(index)
        prompt = entry.split(": ", 1)[1]
        pyperclip.copy(prompt)
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

# Delete-Funktion

def delete_selected():
    selection = listbox.curselection()
    if not selection:
        return
    if not messagebox.askyesno("Sicher?", "Markierte Einträge wirklich löschen?"):
        return
    selected_texts = [listbox.get(i) for i in selection]
    for text in selected_texts:
        bez, prompt = text.split(": ", 1)
        data[:] = [item for item in data if not (item['bezeichner'] == bez and item['prompt'] == prompt)]
    save_data()
    update_list()
    bezeichner_combo['values'] = sorted(list(set([item['bezeichner'] for item in data])))

# Buttons Copy und Löschen
button_frame = tk.Frame(filter_frame, bg="#1F1F1F")
button_frame.grid(row=0, column=3, padx=10)

copy_button = tk.Button(button_frame, text="Copy", command=copy_prompt, bg="#FFA500", fg="#000000")
copy_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Löschen", command=delete_selected, bg="#1F1F1F", fg="red")
delete_button.pack(side="left", padx=5)

# Filter automatisch anwenden
filter_entry.bind("<KeyRelease>", lambda e: update_list())

root.mainloop()
