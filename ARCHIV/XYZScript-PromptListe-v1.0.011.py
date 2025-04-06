# Dateiname: XYPScript-Promptliste
# Version: V1.12b
# Datum: 2025-04-05
# Uhrzeit: 22:00
# Dateispeichername: XYPScript-Promptliste-V1-12b
# Beschreibung: Vollständiger Update-Block (update_list) wiederhergestellt inkl. Bezeichner-Buttons, Checkboxen pro Wort, dynamische Breitenanpassung, Filterfunktion repariert.

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import pyperclip

VERSION = "V1.12b"
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

# --- GUI TOP ---
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

# --- Eingabe Frame ---
data_entry_frame = tk.Frame(root, bg="#1F1F1F")
data_entry_frame.pack(pady=10, fill="x")
tk.Label(data_entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(data_entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)

tk.Label(data_entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(data_entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
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

# --- Buttons ---
tk.Button(data_entry_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").grid(row=0, column=4, padx=5)
tk.Button(data_entry_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").grid(row=0, column=5, padx=5)
tk.Button(data_entry_frame, text="Löschen", command=delete_marked, bg="#8B0000", fg="#FFFFFF").grid(row=0, column=6, padx=5)

# --- Filter Frame ---
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

# --- Toggle Button ---
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

# --- Liste mit Scroll ---
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

# --- update_list ---
def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()
    edit_vars.clear()

    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]

    max_prompt_len = 0
    for item in data:
        prompt_len = len(item['prompt'])
        if prompt_len > max_prompt_len:
            max_prompt_len = prompt_len

    width_factor = min(max_prompt_len * 6 + 400, screen_width - 100)
    canvas.config(width=width_factor)

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
            parts_list = []
            for part in prompt.split(","):
                part = part.strip()
                var = tk.BooleanVar(value=True)
                cb = tk.Checkbutton(row, text=part, variable=var, bg="#1F1F1F", fg="#FFA500",
                                    selectcolor="#1F1F1F", activebackground="#1F1F1F")
                cb.pack(side="left")
                parts_list.append((var, part))
            checkbox_vars.append((item['bezeichner'], parts_list))
    update_toggle_button()

update_list()
root.mainloop()
