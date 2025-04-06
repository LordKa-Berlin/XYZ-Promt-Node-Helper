# Dateiname: XYPScript-Promptliste
# Version: V1.22
# Datum: 2025-04-06
# Uhrzeit: 15:05
# Dateispeichername: XYPScript-Promptliste-V1-22

import tkinter as tk
from tkinter import messagebox
import os
import json
import pyperclip

VERSION = "V1.22"
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

# GUI TOP ------------------------------------------------------------
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

# Eingabe-Frame ------------------------------------------------------
entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Bezeichner:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)
tk.Label(entry_frame, text="SCRIPT-XYZ-Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)

# Button-Frame --------------------------------------------------------
btn_frame = tk.Frame(entry_frame, bg="#1F1F1F")
btn_frame.grid(row=0, column=4, columnspan=3, padx=5)

# Funktionen --------------------------------------------------------
def insert_clipboard():
    try:
        content = pyperclip.paste()
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", content)
        status_var.set("Inhalt eingefügt")
    except:
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
        for entry in data:
            if entry['bezeichner'].lower() == bez.lower() and entry['prompt'].lower() == prompt.lower():
                status_var.set("Duplikat – nicht hinzugefügt")
                return
        data.append({"bezeichner": bez, "prompt": prompt})
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        update_list()
        status_var.set("Eintrag hinzugefügt – nicht gespeichert")
        save_required = True

def copy_master_prompt():
    for entry in data:
        if entry['prompt']:
            first_word = entry['prompt'].split(',')[0].strip()
            pyperclip.copy(first_word)
            status_var.set("Master Prompt kopiert")
            return

def save_data():
    global save_required
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    status_var.set("Liste gespeichert ✓")
    save_required = False

def delete_selected():
    global save_required
    to_delete = [i for i, var in enumerate(checkbox_vars) if var.get()]
    if to_delete:
        if messagebox.askyesno("Löschen", f"{len(to_delete)} Einträge wirklich löschen?"):
            for index in sorted(to_delete, reverse=True):
                del data[index]
            save_required = True
            status_var.set("Einträge gelöscht – nicht gespeichert")
            update_list()

def toggle_all():
    global all_selected
    all_selected = not all_selected
    for var in checkbox_vars:
        var.set(all_selected)
    toggle_button.config(text="Alle entfernen" if all_selected else "Alle markieren")

def on_close():
    if save_required:
        if messagebox.askyesno("Speichern", "Liste wurde geändert. Jetzt speichern?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Buttons
toggle_button = tk.Button(btn_frame, text="Alle entfernen", command=toggle_all, bg="#FFA500", fg="#000000")
toggle_button.pack(side="left", padx=2)
tk.Button(btn_frame, text="Übernehmen", command=add_entry, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Einfügen", command=insert_clipboard, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Speichern", command=save_data, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Löschen", command=delete_selected, bg="red", fg="#FFFFFF").pack(side="left", padx=2)

# Canvas + Scrollbars ---------------------------------------------
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

# Update List -----------------------------------------------------
def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()

    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]

    for idx, entry in enumerate(data):
        prompt = entry['prompt']
        search = f"{entry['bezeichner']} {prompt}".lower()
        if terms:
            if all_words_var.get():
                if not all(term in search for term in terms):
                    continue
            else:
                if not any(term in search for term in terms):
                    continue

        row = tk.Frame(scrollable_frame, bg="#1F1F1F", relief="solid", bd=1)
        row.pack(fill="x", padx=5, pady=2, anchor="w")

        if ansicht_var.get() == "bearbeiten":
            var = tk.BooleanVar()
            cb = tk.Checkbutton(row, variable=var, bg="#1F1F1F")
            cb.pack(side="left")
            checkbox_vars.append(var)

            bez_entry = tk.Entry(row, width=20, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            bez_entry.insert(0, entry['bezeichner'])
            bez_entry.pack(side="left", padx=(10, 5))

            prompt_entry = tk.Entry(row, width=150, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
            prompt_entry.insert(0, insert_linebreaks(entry['prompt']))
            prompt_entry.pack(side="left")
        else:
            var = tk.BooleanVar(value=True)
            checkbox_vars.append(var)
            cb = tk.Checkbutton(row, variable=var, bg="#1F1F1F")
            cb.pack(side="left")

            def make_copy_fn(entry=entry):
                def copy_selected():
                    prompt_words = [w.strip() for w in entry['prompt'].split(',') if w.strip()]
                    pyperclip.copy(", ".join(prompt_words))
                    status_var.set(f"Prompt von '{entry['bezeichner']}' kopiert")
                return copy_selected

            bez_btn = tk.Button(row, text=entry['bezeichner'], bg="#333333", fg="#FFA500", font=("Arial", 10, "bold"),
                                command=make_copy_fn(entry))
            bez_btn.pack(side="left", padx=(5, 10))

            wrapped_prompt = insert_linebreaks(entry['prompt'])
            prompt_words = wrapped_prompt.split("\n")
            for line in prompt_words:
                label = tk.Label(row, text=line, bg="#1F1F1F", fg="#FFA500", anchor="w", justify="left")
                label.pack(side="top", anchor="w")

update_list()
root.mainloop()