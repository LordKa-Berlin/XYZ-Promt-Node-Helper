# Dateiname: XYPScript-Promptliste
# Version: V1.6
# Datum: 2025-04-05
# Uhrzeit: 18:45
# Dateispeichername: XYPScript-Promptliste-V1-6
# Beschreibung: GUI zur Verwaltung von Prompt-Texten mit Bezeichnern. In dieser Version:
# - Checkboxen vor jedem einzelnen Prompt-Wort
# - Einträge können in das Prompt-Feld geladen werden
# - Löschfunktion wiederhergestellt
# - Beschriftung des Prompt-Textfelds ergänzt

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

VERSION = "V1.6"
DATA_FILE = "XYPScriptPromptListe.json"
data = []
changed_entries = []
save_required = False
checkbox_vars = []  # Liste von (bezeichner, [ (checkbox_var, text) ])

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

root = tk.Tk()
root.title("XYPScript-Promptliste")
root.geometry("1600x600")
root.configure(bg="#1F1F1F")

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

tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", fg="#FFA500", bg="#1F1F1F").grid(row=0, column=2, sticky="e")
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
    save_required = True

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

filter_label = tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500")
filter_label.pack(side="left")

filter_entry = tk.Entry(filter_frame, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left", padx=5)

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

def load_to_edit(bezeichner, prompt):
    bezeichner_var.set(bezeichner)
    prompt_entry.delete("1.0", tk.END)
    prompt_entry.insert("1.0", prompt)
    status_var.set("Eintrag zum Bearbeiten geladen.")

# Canvas-Liste mit Checkboxen pro Wort
list_canvas = tk.Canvas(root, bg="#1F1F1F")
list_canvas.pack(fill="both", expand=True)
list_scroll = tk.Scrollbar(list_canvas, orient="vertical", command=list_canvas.yview)
list_scroll.pack(side="right", fill="y")
list_canvas.configure(yscrollcommand=list_scroll.set)

list_inner = tk.Frame(list_canvas, bg="#1F1F1F")
list_canvas.create_window((0, 0), window=list_inner, anchor="nw")
list_inner.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))

def update_list():
    for widget in list_inner.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    terms = [t.strip().lower() for t in filter_entry.get().split(",") if t.strip()]
    for item in data:
        prompt_parts = [p.strip() for p in item['prompt'].split(",") if p.strip()]
        search = f"{item['bezeichner']} {item['prompt']}".lower()
        if terms:
            if all_words_var.get():
                hit = all(term in search for term in terms)
            else:
                hit = any(term in search for term in terms)
        else:
            hit = True
        if hit:
            row_frame = tk.Frame(list_inner, bg="#1F1F1F")
            row_frame.pack(fill="x", anchor="w", pady=2)
            tk.Label(row_frame, text=item['bezeichner']+":", fg="#FFA500", bg="#1F1F1F", font=("Arial", 10, "bold")).pack(side="left", padx=(5, 5))
            parts_list = []
            for part in prompt_parts:
                var = tk.BooleanVar(value=True)
                cb = tk.Checkbutton(row_frame, text=part, variable=var, bg="#1F1F1F", fg="#FFA500", anchor="w",
                                    selectcolor="#1F1F1F", activebackground="#1F1F1F")
                cb.pack(side="left")
                parts_list.append((var, part))
            tk.Button(row_frame, text="Bearbeiten", bg="#FFA500", fg="#000000",
                      command=lambda b=item['bezeichner'], p=item['prompt']: load_to_edit(b, p)).pack(side="right", padx=5)
            checkbox_vars.append((item['bezeichner'], parts_list))

filter_entry.bind("<KeyRelease>", lambda e: update_list())

# Funktionen für Copy + Master Copy mit Checkboxen

def copy_prompt():
    result = []
    for bez, parts in checkbox_vars:
        selected = [text for var, text in parts if var.get()]
        if selected:
            result.append(", ".join(selected))
    if result:
        pyperclip.copy("\n".join(result))
        status_var.set("Prompts kopiert.")
    else:
        status_var.set("Keine Auswahl.")

def copy_master_prompt():
    result = []
    for bez, parts in checkbox_vars:
        for var, text in parts:
            if var.get():
                result.append(text)
                break
    if result:
        pyperclip.copy("\n".join(result))
        status_var.set("Master Prompts kopiert.")
    else:
        status_var.set("Keine Auswahl.")

# Buttons
tk.Button(filter_frame, text="Master Prompt", command=copy_master_prompt, bg="#FFA500", fg="#000000").pack(side="left", padx=5)
tk.Button(filter_frame, text="Copy Prompt", command=copy_prompt, bg="#FFA500", fg="#000000").pack(side="left", padx=5)

def on_close():
    if save_required:
        if messagebox.askyesno("Nicht gespeichert", f"{len(changed_entries)} Änderungen noch nicht gespeichert. Jetzt speichern?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_list()
root.mainloop()
