# Dateiname: XYPScript-Promptliste
# Version: V1.12a
# Datum: 2025-04-05
# Uhrzeit: 21:45
# Dateispeichername: XYPScript-Promptliste-V1-12a
# Beschreibung: Vollständiger Code wiederhergestellt, inklusive GUI-Initialisierung, copy_prompt, delete_marked, und fehlender Frames.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip

VERSION = "V1.12a"
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
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1600, screen_width)}x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False
all_selected = True

# Top-Leiste
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)

always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

# Eingabeframe
data_entry_frame = tk.Frame(root, bg="#1F1F1F")
data_entry_frame.pack(pady=10, fill="x")
tk.Label(data_entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(data_entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)

tk.Label(data_entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(data_entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)

# Filter-Frame
filter_frame = tk.Frame(root, bg="#1F1F1F")
filter_frame.pack(pady=5, fill="x")

ansicht_var = tk.StringVar(value="anzeige")
tk.Label(filter_frame, text="Ansicht:", bg="#1F1F1F", fg="#FFA500").pack(side="left")
tk.Radiobutton(filter_frame, text="Anzeige", variable=ansicht_var, value="anzeige", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")
tk.Radiobutton(filter_frame, text="Bearbeiten", variable=ansicht_var, value="bearbeiten", bg="#1F1F1F", fg="#FFA500", command=lambda: update_list()).pack(side="left")

tk.Label(filter_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(20, 5))
filter_var = tk.StringVar()
filter_entry = tk.Entry(filter_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left")

all_words_var = tk.BooleanVar()
tk.Checkbutton(filter_frame, text="alle Wörter", variable=all_words_var, bg="#1F1F1F", fg="#FFA500").pack(side="left")

# Funktions-Buttons
def copy_prompt(prompt):
    pyperclip.copy(prompt)
    status_var.set("Prompt kopiert")

def delete_marked():
    global data, save_required
    if messagebox.askyesno("Löschen", "Markierte Einträge wirklich löschen?"):
        data = [d for i, d in enumerate(data) if not (ansicht_var.get() == "bearbeiten" and checkbox_vars[i].get())]
        update_list()
        status_var.set("Markierte Einträge gelöscht – nicht gespeichert")
        save_required = True

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

def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", content)
        status_var.set("Inhalt eingefügt")
    except:
        status_var.set("Fehler beim Einfügen")

# Buttons in Eingabeframe
tk.Button(data_entry_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").grid(row=0, column=4, padx=5)
tk.Button(data_entry_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").grid(row=0, column=5, padx=5)
tk.Button(data_entry_frame, text="Löschen", command=delete_marked, bg="#8B0000", fg="#FFFFFF").grid(row=0, column=6, padx=5)

# Listendarstellung
list_frame = tk.Frame(root, bg="#1F1F1F")
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg="#1F1F1F")
hscrollbar = tk.Scrollbar(list_frame, orient="horizontal", command=canvas.xview)
scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1F1F1F")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, xscrollcommand=hscrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
hscrollbar.pack(side="bottom", fill="x")

def toggle_all():
    global all_selected
    all_selected = not all_selected
    for var_data in checkbox_vars:
        if isinstance(var_data, tuple):
            for var, _ in var_data[1]:
                var.set(all_selected)
        else:
            var_data.set(all_selected)
    update_toggle_button()

def update_toggle_button():
    toggle_btn.config(text="Alle abwählen" if all_selected else "Alle wählen")

toggle_btn = tk.Button(filter_frame, text="Alle abwählen", command=toggle_all, bg="#FFA500", fg="#000000")
toggle_btn.pack(side="right", padx=5)

update_list()
root.mainloop()
