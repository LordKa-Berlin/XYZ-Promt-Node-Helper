# Dateiname: XYPScript-Promptliste
# Version: V1.4
# Datum: 2025-04-05
# Uhrzeit: 17:50
# Dateispeichername: XYPScript-Promptliste-V1-4
# Beschreibung: GUI zur Verwaltung von Prompt-Texten mit Bezeichnern. Funktionen: Duplikatprüfung, Einfügen aus Zwischenablage, Copy Prompt / Master Prompt,
# Statusanzeige, Listenbearbeitung mit Speicherschutz, Always on Top, farblich hervorgehobene Statusmeldungen, JSON-Speicherung, Filter, Editierbarkeit.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip
import sys

try:
    import pyperclip
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

VERSION = "V1.4"
DATA_FILE = "XYPScriptPromptListe.json"
data = []
changed_entries = []
save_required = False

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

# Hauptfenster
root = tk.Tk()
root.title("XYPScript-Promptliste")
root.geometry("1600x600")
root.configure(bg="#1F1F1F")

# Statusvariable
status_var = tk.StringVar()

# Top-Leiste
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x", pady=(5, 0))

status_label = tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500", anchor="w")
status_label.pack(side="left", padx=10)

always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)

version_label = tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500")
version_label.pack(side="right", padx=10)

# Eingabeframe
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")

bezeichner_liste = sorted(list(set([item['bezeichner'] for item in data])))

bezeichner_var = tk.StringVar()
tk.Label(entry_frame, text="Bezeichner:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=0, sticky="e")
bezeichner_combo = ttk.Combobox(entry_frame, textvariable=bezeichner_var, values=bezeichner_liste, width=30)
bezeichner_combo.grid(row=0, column=1, padx=5)
bezeichner_combo.configure(background="#000000", foreground="#FFA500")

# Prompt-Feld
prompt_entry = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_entry.grid(row=0, column=3, padx=5)

# Daten speichern

def save_data():
    global save_required, changed_entries
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    status_label.config(bg="#2F2F2F")
    status_var.set(f"Gespeichert: {len(changed_entries)} Änderungen")
    save_required = False
    changed_entries = []

# Eintrag übernehmen

def add_entry():
    global save_required
    bez = bezeichner_var.get().strip()
    prompt = prompt_entry.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if not bez or not prompt:
        messagebox.showwarning("Fehler", "Bezeichner und Prompt dürfen nicht leer sein.")
        return
    if len(bez) > 50 or len(prompt) > 500:
        messagebox.showwarning("Zu lang", "Bezeichner max 50 Zeichen, Prompt max 500 Zeichen.")
        return
    if any(d['bezeichner'] == bez and d['prompt'] == prompt for d in data):
        status_var.set("Eintrag bereits vorhanden.")
        return
    data.append({"bezeichner": bez, "prompt": prompt})
    changed_entries.append(f"{bez}: {prompt}")
    bezeichner_combo.set("")
    prompt_entry.delete("1.0", tk.END)
    update_list()
    bezeichner_combo['values'] = sorted(list(set([item['bezeichner'] for item in data])))
    status_label.config(bg="#1F1F1F")
    status_var.set("Eintrag übernommen – nicht gespeichert!")
    global save_required
    save_required = True

# Einfügen aus Zwischenablage

def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_entry.delete("1.0", tk.END)
        prompt_entry.insert("1.0", content)
        status_var.set("Aus Zwischenablage eingefügt.")
    except:
        status_var.set("Fehler beim Einfügen.")

tk.Button(entry_frame, text="Übernehmen", bg="#FFA500", fg="#000000", command=add_entry).grid(row=0, column=4, padx=5)
tk.Button(entry_frame, text="Einfügen", bg="#FFA500", fg="#000000", command=insert_clipboard).grid(row=0, column=5, padx=5)

# Filterbereich
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=10, fill="x")

def copy_master_prompt():
    try:
        index = listbox.curselection()[0]
        prompt = listbox.get(index).split(": ", 1)[1]
        pyperclip.copy(prompt.split(",")[0].strip())
        status_var.set("Master Prompt kopiert.")
    except:
        status_var.set("Keine Auswahl.")

tk.Button(filter_frame, text="Master Prompt", command=copy_master_prompt, bg="#FFA500", fg="#000000").pack(side="left", padx=5)

def copy_prompt():
    try:
        index = listbox.curselection()[0]
        prompt = listbox.get(index).split(": ", 1)[1]
        pyperclip.copy(prompt)
        status_var.set("Prompt kopiert.")
    except:
        status_var.set("Keine Auswahl.")

tk.Button(filter_frame, text="Copy Prompt", command=copy_prompt, bg="#FFA500", fg="#000000").pack(side="left", padx=5)

# Filter Eingabe
filter_label = tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500")
filter_label.pack(side="left")
filter_entry = tk.Entry(filter_frame, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left", padx=5)
all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

# Listbox & Funktionen
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
listbox = tk.Listbox(list_frame, width=120, height=10, bg="#000000", fg="#FFA500", selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

# Button-Leiste
button_frame = tk.Frame(filter_frame, bg="#1F1F1F")
button_frame.pack(side="right", padx=10)

def delete_selected():
    global save_required
    sel = listbox.curselection()
    if not sel:
        return
    if messagebox.askyesno("Löschen", "Ausgewählte Einträge wirklich löschen?"):
        for i in reversed(sel):
            eintrag = listbox.get(i)
            bez, prompt = eintrag.split(": ", 1)
            data[:] = [item for item in data if not (item['bezeichner'] == bez and item['prompt'] == prompt)]
            changed_entries.append(f"GELÖSCHT: {bez}: {prompt}")
        update_list()
        status_var.set("Eintrag(e) gelöscht – nicht gespeichert!")
        save_required = True

tk.Button(button_frame, text="Löschen", command=delete_selected, bg="#1F1F1F", fg="red").pack(side="left", padx=5)

# Liste speichern
save_button = tk.Button(button_frame, text="Liste speichern", command=save_data, bg="#FFA500", fg="#000000")
save_button.pack(side="left", padx=5)

# Filterfunktion

def update_list():
    listbox.delete(0, tk.END)
    terms = [t.strip().lower() for t in filter_entry.get().split(",") if t.strip()]
    for item in data:
        full = f"{item['bezeichner']}: {item['prompt']}"
        hit = False
        if terms:
            search = f"{item['bezeichner']} {item['prompt']}".lower()
            if all_words_var.get():
                hit = all(term in search for term in terms)
            else:
                hit = any(term in search for term in terms)
        else:
            hit = True
        if hit:
            listbox.insert(tk.END, full)

filter_entry.bind("<KeyRelease>", lambda e: update_list())

# Warnung beim Schließen

def on_close():
    if save_required:
        if messagebox.askyesno("Nicht gespeichert", f"{len(changed_entries)} Änderungen noch nicht gespeichert. Jetzt speichern?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_list()
root.mainloop()
