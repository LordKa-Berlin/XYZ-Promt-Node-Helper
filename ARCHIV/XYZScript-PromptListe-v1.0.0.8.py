# Dateiname: XYPScript-Promptliste
# Version: V1.8
# Datum: 2025-04-05
# Uhrzeit: 19:30
# Dateispeichername: XYPScript-Promptliste-V1-8
# Beschreibung: Zwei umschaltbare Ansichten für Prompt-Listen: Anzeige (Checkbox pro Wort) und Bearbeitung (direkt editierbar).
# Zeilen können in Bearbeitungsmodus über Checkbox markiert und über den zentralen Löschen-Button gelöscht werden. Zeilenfarbmarkierung inklusive.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip

VERSION = "V1.8"
DATA_FILE = "XYPScriptPromptListe.json"
data = []
checkbox_vars = []
edit_vars = []

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
top_bar.pack(fill="x")
status_label = tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500")
status_label.pack(side="left", padx=10)

always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
version_label = tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500")
version_label.pack(side="right", padx=10)

# Ansichtsauswahl
ansicht_var = tk.StringVar(value="anzeige")
view_frame = tk.Frame(root, bg="#1F1F1F")
view_frame.pack(fill="x")
tk.Radiobutton(view_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left", padx=5)
tk.Radiobutton(view_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")

# Eingabefeld
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)

tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)

def add_entry():
    bez = bezeichner_var.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if bez and prompt:
        data.append({"bezeichner": bez, "prompt": prompt})
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        update_list()
        status_var.set("Eintrag hinzugefügt")

def delete_marked():
    global data
    if messagebox.askyesno("Löschen", "Markierte Einträge wirklich löschen?"):
        new_data = []
        for i, entry in enumerate(data):
            if ansicht_var.get() == "bearbeiten" and checkbox_vars[i].get():
                continue
            new_data.append(entry)
        data = new_data
        update_list()
        status_var.set("Markierte Einträge gelöscht")

# Button-Leiste
tk.Button(entry_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").grid(row=0, column=4, padx=5)
tk.Button(entry_frame, text="Löschen", command=delete_marked, bg="#FFA500", fg="#000000").grid(row=0, column=5)

# Listenanzeige
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg="#1F1F1F")
scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1F1F1F")

scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    edit_vars.clear()
    for i, item in enumerate(data):
        row = tk.Frame(scrollable_frame, bg="#1F1F1F")
        row.pack(fill="x", pady=1, padx=5, anchor="w")

        if ansicht_var.get() == "bearbeiten":
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(row, variable=var, bg="#1F1F1F")
            checkbox.grid(row=0, column=0)
            checkbox_vars.append(var)

            bezeichner_edit = tk.Entry(row, width=20, bg="#000000", fg="#FFA500")
            bezeichner_edit.insert(0, item['bezeichner'])
            bezeichner_edit.grid(row=0, column=1, padx=5)

            prompt_edit = tk.Entry(row, width=80, bg="#000000", fg="#FFA500")
            prompt_edit.insert(0, item['prompt'])
            prompt_edit.grid(row=0, column=2, padx=5)

            edit_vars.append((bezeichner_edit, prompt_edit))

            def on_change_color(var=var, frame=row):
                if var.get():
                    frame.configure(bg="#802020")
                else:
                    frame.configure(bg="#1F1F1F")

            var.trace_add("write", lambda *_: on_change_color())

        else:
            tk.Label(row, text=item['bezeichner']+":", fg="#FFA500", bg="#1F1F1F", font=("Arial", 10, "bold")).pack(side="left", padx=(5, 5))
            for part in item['prompt'].split(","):
                part = part.strip()
                cb_var = tk.BooleanVar(value=True)
                cb = tk.Checkbutton(row, text=part, variable=cb_var, bg="#1F1F1F", fg="#FFA500",
                                    selectcolor="#1F1F1F", activebackground="#1F1F1F")
                cb.pack(side="left")

update_list()
root.mainloop()
