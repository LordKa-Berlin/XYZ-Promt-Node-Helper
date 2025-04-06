# Dateiname: XYPScript-Promptliste
# Version: V1.3
# Datum: 2025-04-05
# Uhrzeit: 17:30
# Dateispeichername: XYPScript-Promptliste-V1-3
# Beschreibung: GUI zur Eingabe, Anzeige, Filterung und Bearbeitung von Bezeichnern mit zugehörigen Prompts. Speicherung im JSON-Format,
# Editierbarkeit, Filterfunktion, Copy in Zwischenablage (nur Prompt oder nur Master-Wert), Mehrfachlöschung mit Sicherheitsabfrage,
# Always on Top, Statusanzeige, Versionsanzeige im UI, einheitliches Farbschema.

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
VERSION = "V1.3"

# JSON-Dateipfad
DATA_FILE = "XYPScriptPromptListe.json"

# Daten laden
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

# Daten speichern
status_var = None

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if status_var:
        status_var.set("Daten gespeichert.")

# Hauptfenster
root = tk.Tk()
root.title("XYPScript-Promptliste")
root.geometry("1600x600")
root.configure(bg="#1F1F1F")

# Top Bar mit Version & Always-on-Top
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x", pady=(5, 0))

version_label = tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500")
version_label.pack(side="right", padx=10)

always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)

# Eingabe-Frame
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")

# Statusanzeige in der Mitte
status_var = tk.StringVar()
status_label = tk.Label(entry_frame, textvariable=status_var, bg="#1F1F1F", fg="#FFA500")
status_label.grid(row=1, column=0, columnspan=5)

# Funktion für Bezeichnerliste
bezeichner_liste = sorted(list(set([item['bezeichner'] for item in data])))

# Bezeichner Combobox
bezeichner_var = tk.StringVar()
tk.Label(entry_frame, text="Bezeichner:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=0, sticky="e")
bezeichner_combo = ttk.Combobox(entry_frame, textvariable=bezeichner_var, values=bezeichner_liste, width=30)
bezeichner_combo.grid(row=0, column=1, padx=5)
bezeichner_combo.configure(background="#000000", foreground="#FFA500")

# Prompt (mehrzeilig mit sichtbarem Cursor)
tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=2, sticky="e")
prompt_entry = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_entry.grid(row=0, column=3, padx=5)

# Eintrag übernehmen
def add_entry():
    bez = bezeichner_var.get().strip()
    prompt = prompt_entry.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])  # Einheitliches Leerzeichen nach Komma
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
    status_var.set("Eintrag gespeichert.")

tk.Button(entry_frame, text="Übernehmen", bg="#FFA500", fg="#000000", command=add_entry).grid(row=0, column=4, padx=10)

# Filter
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=10, fill="x")

# Master Prompt Button (links)
def copy_master_prompt():
    try:
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        entry = listbox.get(index)
        prompt = entry.split(": ", 1)[1]
        first = prompt.split(",")[0].strip()
        pyperclip.copy(first)
        status_var.set("Master Prompt kopiert: " + first)
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

tk.Button(filter_frame, text="Master Prompt", command=copy_master_prompt, bg="#FFA500", fg="#000000").pack(side="left", padx=10)

# Filter Eingabefeld mit sichtbarem Cursor
filter_label = tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500")
filter_label.pack(side="left")

filter_entry = tk.Entry(filter_frame, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left", padx=5)

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

# Buttongruppe
button_frame = tk.Frame(filter_frame, bg="#1F1F1F")
button_frame.pack(side="left", padx=10)

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
        status_var.set("Prompt kopiert.")
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
    status_var.set("Eintrag gelöscht.")

copy_button = tk.Button(button_frame, text="Copy", command=copy_prompt, bg="#FFA500", fg="#000000")
copy_button.pack(side="left", padx=5)

delete_button = tk.Button(button_frame, text="Löschen", command=delete_selected, bg="#1F1F1F", fg="red")
delete_button.pack(side="left", padx=5)

# Filter automatisch anwenden
filter_entry.bind("<KeyRelease>", lambda e: update_list())

# Listbox mit Scrollbar
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, width=120, height=10, bg="#000000", fg="#FFA500", selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

update_list()

root.mainloop()
