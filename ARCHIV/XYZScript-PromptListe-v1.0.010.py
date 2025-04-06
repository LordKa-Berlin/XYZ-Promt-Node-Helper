# Dateiname: XYPScript-Promptliste
# Version: V1.11
# Datum: 2025-04-05
# Uhrzeit: 21:00
# Dateispeichername: XYPScript-Promptliste-V1-11
# Beschreibung: Bezeichner in Anzeige-Ansicht als Buttons, Filterfunktion repariert, Bezeichner-Feld als Pulldown-Menü, Eingabe- und Filterbereich getauscht.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip

VERSION = "V1.11"
DATA_FILE = "XYPScriptPromptListe.json"
data = []
checkbox_vars = []
edit_vars = []
selected_row_index = None

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

root = tk.Tk()
root.title("XYPScript-Promptliste")
root.geometry("1600x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False

# Top-Leiste
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
status_label = tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500")
status_label.pack(side="left", padx=10)

always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
version_label = tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500")
version_label.pack(side="right", padx=10)

# Eingabe
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_combo = ttk.Combobox(entry_frame, textvariable=bezeichner_var, width=30)
bezeichner_combo.grid(row=0, column=1, padx=5)
bezeichner_combo.configure(background="#000000", foreground="#FFA500")

tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)

def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", content)
        status_var.set("Inhalt eingefügt")
    except:
        status_var.set("Fehler beim Einfügen")

def add_entry():
    global save_required
    bez = bezeichner_var.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if bez and prompt:
        data.append({"bezeichner": bez, "prompt": prompt})
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        update_list()
        status_var.set("Eintrag hinzugefügt – nicht gespeichert")
        save_required = True

        # Bezeichnerliste aktualisieren
        bezeichner_combo['values'] = sorted(list(set(d['bezeichner'] for d in data)))

def save_list():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    status_var.set("Liste gespeichert")
    global save_required
    save_required = False

def delete_marked():
    global data, save_required
    if messagebox.askyesno("Löschen", "Markierte Einträge wirklich löschen?"):
        data = [d for i, d in enumerate(data) if not (ansicht_var.get() == "bearbeiten" and checkbox_vars[i].get())]
        update_list()
        status_var.set("Markierte Einträge gelöscht – nicht gespeichert")
        save_required = True

# Ansichtsauswahl + Filterzeile
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=5, fill="x")

ansicht_var = tk.StringVar(value="anzeige")
tk.Label(filter_frame, text="Ansicht:", bg="#1F1F1F", fg="#FFA500").pack(side="left")
tk.Radiobutton(filter_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")
tk.Radiobutton(filter_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")

def copy_prompt(prompt):
    pyperclip.copy(prompt)
    status_var.set("Prompt kopiert")

tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(20, 5))
filter_var = tk.StringVar()
filter_entry = tk.Entry(filter_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left")

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

# Buttonreihe
tk.Button(entry_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").grid(row=0, column=4, padx=5)
tk.Button(entry_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").grid(row=0, column=5, padx=5)
tk.Button(entry_frame, text="Löschen", command=delete_marked, bg="#FFA500", fg="#000000").grid(row=0, column=6, padx=5)
tk.Button(entry_frame, text="Liste speichern", command=save_list, bg="#FFA500", fg="#000000").grid(row=0, column=7, padx=5)

# Listendarstellung
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg="#1F1F1F")
scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1F1F1F")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    edit_vars.clear()
    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]
    for i, item in enumerate(data):
        prompt = item['prompt']
        search = f"{item['bezeichner']} {prompt}".lower()
        if terms:
            if all_words_var.get():
                if not all(term in search for term in terms):
                    continue
            else:
                if not any(term in search for term in terms):
                    continue

        row = tk.Frame(scrollable_frame, bg="#1F1F1F")
        row.pack(fill="x", pady=1, padx=5, anchor="w")

        if ansicht_var.get() == "bearbeiten":
            var = tk.BooleanVar()
            cb = tk.Checkbutton(row, variable=var, bg="#1F1F1F")
            cb.grid(row=0, column=0)
            checkbox_vars.append(var)

            bez = tk.Entry(row, width=20, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            bez.insert(0, item['bezeichner'])
            bez.grid(row=0, column=1, padx=5)

            prm = tk.Entry(row, width=160, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            prm.insert(0, item['prompt'])
            prm.grid(row=0, column=2, padx=5)
            edit_vars.append((bez, prm))
        else:
            bez_btn = tk.Button(row, text=item['bezeichner'], fg="#FFA500", bg="#333333", font=("Arial", 10, "bold"),
                                command=lambda p=prompt: copy_prompt(p))
            bez_btn.pack(side="left", padx=(5, 10))
            for part in prompt.split(","):
                part = part.strip()
                var = tk.BooleanVar(value=True)
                cb = tk.Checkbutton(row, text=part, variable=var, bg="#1F1F1F", fg="#FFA500",
                                    selectcolor="#1F1F1F", activebackground="#1F1F1F")
                cb.pack(side="left")
                checkbox_vars.append((item['bezeichner'], [(var, part)]))

update_list()
root.mainloop()