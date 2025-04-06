# Dateiname: XYPScript-Promptliste
# Version: V1.9
# Datum: 2025-04-05
# Uhrzeit: 20:00
# Dateispeichername: XYPScript-Promptliste-V1-9
# Beschreibung: Zwei Ansichten (Anzeige & Bearbeiten) vollständig mit Buttons ergänzt: Copy Prompt, Master Prompt, Einfügen, Liste speichern, Filter, Mausrad-Scrolling.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip

VERSION = "V1.9"
DATA_FILE = "XYPScriptPromptListe.json"
data = []
checkbox_vars = []
edit_vars = []

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

# Ansichtsauswahl
ansicht_var = tk.StringVar(value="anzeige")
view_frame = tk.Frame(root, bg="#1F1F1F")
view_frame.pack(fill="x")
tk.Radiobutton(view_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left", padx=5)
tk.Radiobutton(view_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")

# Eingabefeld + Buttons
def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", content)
        status_var.set("Inhalt eingefügt")
    except:
        status_var.set("Fehler beim Einfügen")

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

tk.Button(entry_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").grid(row=0, column=4, padx=5)
tk.Button(entry_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").grid(row=0, column=5, padx=5)
tk.Button(entry_frame, text="Löschen", command=delete_marked, bg="#FFA500", fg="#000000").grid(row=0, column=6, padx=5)
tk.Button(entry_frame, text="Liste speichern", command=save_list, bg="#FFA500", fg="#000000").grid(row=0, column=7, padx=5)

# Filter
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=5, fill="x")
tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left")
filter_var = tk.StringVar()
filter_entry = tk.Entry(filter_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left", padx=5)

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

def copy_prompt():
    result = []
    for bez, parts in checkbox_vars:
        selected = [text for var, text in parts if var.get()]
        if selected:
            result.append(", ".join(selected))
    if result:
        pyperclip.copy("\n".join(result))
        status_var.set("Prompts kopiert")
    else:
        status_var.set("Keine Auswahl")

def copy_master_prompt():
    result = []
    for bez, parts in checkbox_vars:
        for var, text in parts:
            if var.get():
                result.append(text)
                break
    if result:
        pyperclip.copy("\n".join(result))
        status_var.set("Master Prompts kopiert")
    else:
        status_var.set("Keine Auswahl")

tk.Button(filter_frame, text="Master Prompt", command=copy_master_prompt, bg="#FFA500", fg="#000000").pack(side="right", padx=5)
tk.Button(filter_frame, text="Copy Prompt", command=copy_prompt, bg="#FFA500", fg="#000000").pack(side="right", padx=5)

# Liste anzeigen
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg="#1F1F1F")
scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1F1F1F")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Maus-Scrolling aktivieren
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
            parts_list = []
            for part in prompt.split(","):
                part = part.strip()
                var = tk.BooleanVar(value=True)
                cb = tk.Checkbutton(row, text=part, variable=var, bg="#1F1F1F", fg="#FFA500",
                                    selectcolor="#1F1F1F", activebackground="#1F1F1F")
                cb.pack(side="left")
                parts_list.append((var, part))
            checkbox_vars.append((item['bezeichner'], parts_list))

update_list()
root.mainloop()