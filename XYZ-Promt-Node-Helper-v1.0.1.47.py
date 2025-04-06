# Dateiname: XYZ-Promt-Node-Helper.py
# Version: V1.0.1.47
# Datum: 2025-04-06
# Uhrzeit: 17:05
# Dateispeichername: XYZ-Promt-Node-Helper.json

import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import pyperclip
import uuid
import shutil
import datetime
import time
import csv
import textwrap

VERSION = "V1.0.1.47"

# Ermittele das Verzeichnis des Skripts und arbeite relativ dazu:
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(script_dir, "XYZ-Promt-Node-Helper.json")
BACKUP_DIR = os.path.join(script_dir, "backup-XYZ-Promt-Node-Helper")

# Daten laden
data = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
for entry in data:
    if "id" not in entry:
        entry["id"] = str(uuid.uuid4())

# Globale Zustands-Dictionaries für den Anzeige‑Modus:
# row_bez_state: 0 = normal, 1 = disabled, 2 = marked for deletion
row_bez_state = {}
# row_value_states: in gleicher Reihenfolge wie beim Split des Prompts
row_value_states = {}

root = tk.Tk()
root.title("XYZ-Promt-Node-Helper")
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1800, screen_width)}x700")
root.configure(bg="#1F1F1F")

status_var = tk.StringVar()
save_required = False

# Modus (View oder Edit) – Initial im View-Modus
ansicht_var = tk.StringVar(value="view")

# Neuer Output-Modus: "comma" (Output 1) oder "line" (Output 2)
output_mode_var = tk.StringVar(value="comma")
output_mode_status_var = tk.StringVar()
def update_output_mode_status():
    if output_mode_var.get() == "comma":
        output_mode_status_var.set("Output Mode: comma separated")
    else:
        output_mode_status_var.set("Output Mode: line by line")
update_output_mode_status()

checkbox_vars = []  # für Edit-Modus
edit_widgets = []   # für Edit-Modus

# Neue Funktion: Zeilenumbruch in der Anzeige-Liste – wir verwenden textwrap.wrap
def insert_linebreaks_display(text, limit=130):
    wrapped_lines = textwrap.wrap(text, width=limit)
    return "\n".join(wrapped_lines)

# Ursprüngliche Funktion für den Zeilenumbruch (wird in der Edit-Ansicht verwendet)
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

# --- Backup-Funktionen ---
def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if os.path.exists(DATA_FILE):
        now = datetime.datetime.now()
        backup_filename = f"XYZ-Promt-Node-Helper.json-{now:%Y-%m-%d-%H-%M-%S}"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        shutil.copy(DATA_FILE, backup_path)
        cleanup_backups(BACKUP_DIR)
        status_var.set(status_var.get() + " Backup created.")

def cleanup_backups(backup_dir):
    files = []
    for f in os.listdir(backup_dir):
        if f.startswith("XYZ-Promt-Node-Helper.json-"):
            full_path = os.path.join(backup_dir, f)
            files.append((full_path, os.path.getmtime(full_path)))
    files.sort(key=lambda x: x[1], reverse=True)
    to_check = files[10:]
    now = time.time()
    thirty_days = 30 * 24 * 3600
    for full_path, mtime in to_check:
        if now - mtime > thirty_days:
            os.remove(full_path)

# --- Funktionen zur Aktualisierung der Button-Oberfläche ---
def update_button_appearance(btn, state, is_bez=False):
    if state == 0:  # normal
        if is_bez:
            btn.config(bg="#212121", fg="orange")
        else:
            btn.config(bg="#84672d", fg="#000000")
    elif state == 1:  # disabled
        if is_bez:
            btn.config(bg="#1F1F1F", fg="orange")
        else:
            btn.config(bg="#1F1F1F", fg="#D3D3D3")
    elif state == 2:  # marked for deletion
        btn.config(bg="#FF0000", fg="#FFFFFF")

# --- Funktionen für Eingabe, Speichern, Löschen ---
def get_unique_bezeichner(base):
    base_lower = base.lower()
    existing = {entry["bezeichner"].lower() for entry in data}
    if base_lower not in existing:
        return base
    i = 1
    while f"{base}-{i}".lower() in existing:
        i += 1
    return f"{base}-{i}"

def add_entry():
    global save_required
    label_text = bezeichner_var.get().strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    prompt = ", ".join([p.strip() for p in prompt.split(",") if p.strip()])
    if label_text and prompt:
        label_text = get_unique_bezeichner(label_text)
        for entry in data:
            if entry["bezeichner"].lower() == label_text.lower() and entry["prompt"].lower() == prompt.lower():
                status_var.set("Duplicate entry – not added")
                return
        new_entry = {"id": str(uuid.uuid4()), "bezeichner": label_text, "prompt": prompt}
        data.append(new_entry)
        bezeichner_var.set("")
        prompt_text.delete("1.0", tk.END)
        status_var.set("Entry added – not saved")
        save_required = True
        update_list()

def save_data():
    global save_required, edit_widgets
    if ansicht_var.get() == "edit":
        for widget in edit_widgets:
            idx = widget["index"]
            new_label = widget["bez_widget"].get().strip()
            new_prompt_raw = widget["prompt_widget"].get("1.0", tk.END).strip()
            prompt_parts = [p.strip() for p in new_prompt_raw.replace("\n", " ").split(",") if p.strip()]
            normalized_prompt = ", ".join(prompt_parts)
            new_label = get_unique_bezeichner(new_label)
            data[idx]["bezeichner"] = new_label
            data[idx]["prompt"] = normalized_prompt
    create_backup()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    status_var.set("List saved ✓")
    save_required = False
    update_list()

def delete_marked():
    global save_required, data, row_bez_state, row_value_states
    entries_to_delete = []
    entries_to_update = []
    message_lines = []
    for entry in data:
        eid = entry["id"]
        if row_bez_state.get(eid, 0) == 2:
            entries_to_delete.append(entry)
            message_lines.append(f"{entry['bezeichner']}: entire entry")
        else:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            states = row_value_states.get(eid, [0]*len(values))
            marked = [values[i] for i, st in enumerate(states) if st == 2]
            if marked:
                message_lines.append(f"{entry['bezeichner']}: {', '.join(marked)}")
                new_values = [values[i] for i, st in enumerate(states) if st != 2]
                new_prompt = ", ".join(new_values)
                entries_to_update.append((entry, new_prompt))
    if not message_lines:
        status_var.set("No entries marked for deletion")
        return
    msg = "The following entries/parts will be deleted:\n" + "\n".join(message_lines) + "\n\nReally delete?"
    ans = messagebox.askyesnocancel("Confirm Deletion", msg)
    if ans is True:
        for entry in entries_to_delete:
            data.remove(entry)
            eid = entry["id"]
            if eid in row_bez_state: del row_bez_state[eid]
            if eid in row_value_states: del row_value_states[eid]
        for entry, new_prompt in entries_to_update:
            entry["prompt"] = new_prompt
            eid = entry["id"]
            values = [v.strip() for v in new_prompt.split(",") if v.strip()]
            row_value_states[eid] = [0]*len(values)
            row_bez_state[eid] = 0
        save_required = True
        status_var.set("Marked entries updated/deleted – not saved")
        update_list()
    elif ans is False:
        status_var.set("Deletion cancelled (No)")
    else:
        status_var.set("Deletion cancelled (Cancel)")

def copy_master_prompt_from_row(eid):
    for entry in data:
        if entry["id"] == eid:
            values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
            states = row_value_states.get(eid, [0]*len(values))
            active_values = [values[i] for i, st in enumerate(states) if st == 0]
            if active_values:
                if output_mode_var.get() == "comma":
                    result = ", ".join(active_values)
                else:
                    result = "\n".join(active_values)
                pyperclip.copy(result)
                status_var.set(f"Content from '{entry['bezeichner']}' copied")
            break

# --- Event-Handler für den View-Modus ---
def bezeichner_single_click(event, eid):
    copy_master_prompt_from_row(eid)

def bezeichner_double_click(event, eid):
    if row_bez_state.get(eid, 0) == 2:
        row_bez_state[eid] = 0
        for entry in data:
            if entry["id"] == eid:
                values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
                row_value_states[eid] = [0]*len(values)
                break
    else:
        row_bez_state[eid] = 2
        for entry in data:
            if entry["id"] == eid:
                values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
                row_value_states[eid] = [2]*len(values)
                break
    update_list()

# --- Neue Funktionen für Long Press bei Wert‑Buttons ---
def value_button_press(event, eid, idx, btn):
    btn.long_press_triggered = False
    def long_press_action():
        btn.long_press_triggered = True
        text = btn.cget("text")
        pyperclip.copy(text)
        status_var.set(f"Long press: '{text}' copied")
    btn.after_id = btn.after(2000, long_press_action)

def value_button_release(event, eid, idx, btn):
    if hasattr(btn, "after_id"):
        btn.after_cancel(btn.after_id)
        del btn.after_id
    if getattr(btn, "long_press_triggered", False):
        btn.long_press_triggered = False
        return
    value_single_click(eid, idx, btn)

def value_single_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states):
        if states[index] == 0:
            states[index] = 1
        elif states[index] == 1:
            states[index] = 0
        row_value_states[eid] = states
        update_button_appearance(btn, states[index])

def value_double_click(eid, index, btn):
    states = row_value_states.get(eid, [])
    if index < len(states):
        if states[index] == 2:
            states[index] = 0
        else:
            states[index] = 2
        row_value_states[eid] = states
        update_button_appearance(btn, states[index])

# --- Event-Handler für den Edit-Modus ---
def create_bearbeiten_row(row_frame, entry, idx):
    eid = entry["id"]
    var = tk.BooleanVar()
    cb = tk.Checkbutton(row_frame, variable=var, bg="#1F1F1F")
    cb.pack(side="left")
    checkbox_vars.append(var)
    bez_entry = tk.Entry(row_frame, width=20, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
    bez_entry.insert(0, entry["bezeichner"])
    bez_entry.pack(side="left", padx=(10, 5))
    prompt_widget = tk.Text(row_frame, height=3, width=100, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
    # Im Edit-Modus wird der Text unverändert übernommen
    prompt_widget.insert("1.0", entry["prompt"])
    prompt_widget.pack(side="left")
    edit_widgets.append({
        "index": idx,
        "bez_widget": bez_entry,
        "prompt_widget": prompt_widget
    })

# --- Neuer Toggle‑Button für alle Wert‑Buttons im View-Modus ---
def toggle_all_values():
    global row_value_states
    all_active = True
    for states in row_value_states.values():
        if states and not all(st == 0 for st in states):
            all_active = False
            break
    new_state = 1 if all_active else 0
    for eid in row_value_states:
        row_value_states[eid] = [new_state] * len(row_value_states[eid])
    update_list()
    update_toggle_button_text()

def update_toggle_button_text():
    all_active = True
    for states in row_value_states.values():
        if states and not all(st == 0 for st in states):
            all_active = False
            break
    if all_active:
        toggle_values_btn.config(text="Deactivate All")
    else:
        toggle_values_btn.config(text="Activate All")

# --- Neuer Toggle‑Button für den Modus (View/Edit) ---
def toggle_mode():
    if ansicht_var.get() == "view":
        ansicht_var.set("edit")
        toggle_mode_btn.config(text="View")
    else:
        ansicht_var.set("view")
        toggle_mode_btn.config(text="Edit")
    update_list()

# --- Import-Funktion ---
def get_unique_bezeichner_for_import(base):
    return get_unique_bezeichner(base)

def import_csv_file(filename):
    imported_count = 0
    duplicate_count = 0
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                base = row[0].strip()
                if not base:
                    continue
                unique_bez = get_unique_bezeichner_for_import(base)
                values = [val.strip() for val in row[1:] if val.strip()]
                if not values:
                    continue
                prompt = ", ".join(values)
                duplicate = False
                for entry in data:
                    if entry["bezeichner"].lower() == unique_bez.lower() and entry["prompt"].lower() == prompt.lower():
                        duplicate = True
                        break
                if duplicate:
                    duplicate_count += 1
                    continue
                new_entry = {"id": str(uuid.uuid4()), "bezeichner": unique_bez, "prompt": prompt}
                data.append(new_entry)
                imported_count += 1
        status_var.set(f"Import complete: {imported_count} entries, {duplicate_count} duplicates skipped.")
        update_list()
    except Exception as e:
        status_var.set(f"Import error: {str(e)}")

def import_csv_window():
    win = tk.Toplevel(root)
    win.title("CSV Import")
    win.geometry("400x150")
    chosen_file_var = tk.StringVar()
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        chosen_file_var.set(file_path)
    tk.Button(win, text="Select File", command=select_file, bg="#FFA500", fg="#000000").pack(pady=10)
    tk.Label(win, textvariable=chosen_file_var, bg="#1F1F1F", fg="#FFA500").pack(pady=5)
    def do_import():
        if chosen_file_var.get():
            import_csv_file(chosen_file_var.get())
            win.destroy()
        else:
            status_var.set("No file selected.")
    tk.Button(win, text="Import", command=do_import, bg="#FFA500", fg="#000000").pack(pady=10)

# --- Info-Funktion: Öffnet ein Infofenster ---
def show_info():
    info_win = tk.Toplevel(root)
    info_win.title("About XYZ-Promt-Node-Helper")
    info_win.geometry("800x600")
    info_win.configure(bg="#1F1F1F")
    
    info_text = ( """
XYZ-Promt-Node-Helper – HELP & USER GUIDE
Version: """ + VERSION + """

WHAT DOES THIS PROGRAM DO?
---------------------------
The XYZ-Promt-Node-Helper is a desktop tool to manage, edit, and organize prompt entries – especially 
helpful for users of GUIs like Forge, AUTOMATIC1111, or ComfyUI. It allows you to structure prompts 
clearly and export them in multiple formats.

MAIN FEATURES & HOW TO USE
---------------------------
➕ Add Entry:
  - Enter a 'Label' and a comma-separated list of prompt elements.
  - Click 'Add Entry' to insert the entry.
  - Duplicate entries are automatically avoided.

✏️ Edit & Save:
  - Switch to 'Edit' mode to modify labels or prompt content.
  - Click 'Save' to apply changes.
  - Every save triggers an automatic backup.

🗑️ Delete Entries:
  - In View Mode:
      • Single-click a label to copy its prompt.
      • Double-click a label to mark the entire entry for deletion.
      • Double-click a prompt value to mark only that part for deletion.
  - In Edit Mode:
      • Use checkboxes to select entries for deletion.
  - Confirm via the 'Delete' button.

📁 BACKUP SYSTEM:
  - Every save or deletion creates an automatic backup.
  - Backup files are stored in:
      ./backup-XYZ-Promt-Node-Helper/
  - Backups older than 30 days are deleted automatically.

🗃️ STORAGE FILE:
  - All prompt entries are stored in:
      ./XYZ-Promt-Node-Helper.json

📤 Output Format:
  - Choose between 'Comma separated' (Forge, AUTOMATIC1111) or 'Line by line' (for ComfyUI-compatible nodes).
  - This affects copy behavior.

🔍 Filtering:
  - Enter keywords to highlight relevant entries.
  - Multiple terms are searched with OR logic.

📥 CSV Import:
  - Import prompt lists from CSV: Label, Prompt1, Prompt2, ...
  - Duplicate entries are ignored.

🕐 Long Press:
  - Hold a prompt button for ~2 seconds to copy its text.

✅ Toggle All:
  - Quickly activate/deactivate all prompt values.

📌 Always on Top:
  - Keeps the window in the foreground.

❓ Help Button:
  - Click '?' to view this help guide.
""" )
    info_label = tk.Text(info_win, bg="#1F1F1F", fg="#FFA500", wrap="word", bd=0)
    info_label.insert("1.0", info_text)
    info_label.config(state="disabled")
    info_label.pack(expand=True, fill="both", padx=10, pady=10)
    
    close_btn = tk.Button(info_win, text="Close", command=info_win.destroy, bg="#FFA500", fg="#000000")
    close_btn.pack(pady=10)

# --- GUI Aufbau ---
top_bar = tk.Frame(root, bg="#1F1F1F")
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
tk.Label(top_bar, textvariable=output_mode_status_var, bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg="#1F1F1F", fg="#FFA500",
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Button(top_bar, text="?", command=show_info, bg="#FFA500", fg="#000000", width=3).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg="#1F1F1F", fg="#FFA500").pack(side="right", padx=10)

entry_frame = tk.Frame(root, bg="#1F1F1F")
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Label:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(entry_frame, textvariable=bezeichner_var, width=30, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
bezeichner_entry.grid(row=0, column=1, padx=5)
tk.Label(entry_frame, text="Prompt:", bg="#1F1F1F", fg="#FFA500").grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
prompt_text.grid(row=0, column=3, padx=5)
btn_frame = tk.Frame(entry_frame, bg="#1F1F1F")
btn_frame.grid(row=0, column=4, columnspan=3, padx=5)

tk.Button(btn_frame, text="Add Entry", command=add_entry, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Paste", command=lambda: (prompt_text.delete("1.0", tk.END), prompt_text.insert("1.0", pyperclip.paste())), bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Save", command=save_data, bg="#FFA500", fg="#000000").pack(side="left", padx=2)
tk.Button(btn_frame, text="Delete", command=delete_marked, bg="red", fg="#FFFFFF").pack(side="left", padx=2)

second_frame = tk.Frame(root, bg="#1F1F1F")
second_frame.pack(fill="x", pady=5)
left_frame = tk.Frame(second_frame, bg="#1F1F1F")
left_frame.pack(side="left", fill="x", expand=True)
right_frame = tk.Frame(second_frame, bg="#1F1F1F")
right_frame.pack(side="right")
toggle_mode_btn = tk.Button(left_frame, text="Edit", command=toggle_mode, bg="#FFA500", fg="#000000")
toggle_mode_btn.pack(side="left", padx=(10,2))
toggle_values_btn = tk.Button(left_frame, text="Deactivate All", command=toggle_all_values, bg="#FFA500", fg="#000000")
toggle_values_btn.pack(side="left", padx=10)
tk.Label(left_frame, text="Filter:", bg="#1F1F1F", fg="#FFA500").pack(side="left", padx=(20,2))
filter_var = tk.StringVar()
filter_entry = tk.Entry(left_frame, textvariable=filter_var, width=50, bg="#000000", fg="#FFA500", insertbackground="#FFA500")
filter_entry.pack(side="left")
tk.Button(left_frame, text="Clear", command=lambda: filter_var.set(""), bg="#FFA500", fg="#000000").pack(side="left", padx=5)
filter_var.trace_add("write", lambda *args: update_list())

# Output Mode and Import CSV – right side
output_frame = tk.Frame(right_frame, bg="#1F1F1F")
output_frame.pack(side="right", padx=5)
radio1 = tk.Radiobutton(output_frame, text="Output 1 comma separated\n(e.g. Forge & AUTOMATIC1111)",
                        variable=output_mode_var, value="comma", bg="#1F1F1F", fg="#FFA500", selectcolor="#1F1F1F",
                        command=lambda: (update_output_mode_status(), update_list()))
radio1.pack(side="left", padx=5)
radio2 = tk.Radiobutton(output_frame, text="Output 2 Line by line\n(e.g. for ComfyUI-compatible nodes)",
                        variable=output_mode_var, value="line", bg="#1F1F1F", fg="#FFA500", selectcolor="#1F1F1F",
                        command=lambda: (update_output_mode_status(), update_list()))
radio2.pack(side="left", padx=5)
tk.Button(output_frame, text="Import CSV", command=import_csv_window, bg="#FFA500", fg="#000000").pack(side="left", padx=5)

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

def update_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    del checkbox_vars[:]
    del edit_widgets[:]
    global row_bez_state, row_value_states
    terms = [t.strip().lower() for t in filter_var.get().split(",") if t.strip()]
    row_added = False
    for idx, entry in enumerate(data):
        combined = f"{entry['bezeichner']} {entry['prompt']}".lower()
        if terms and not any(term in combined for term in terms):
            continue
        row_added = True
        eid = entry["id"]
        if eid not in row_bez_state:
            row_bez_state[eid] = 0
        values = [v.strip() for v in entry["prompt"].split(",") if v.strip()]
        if eid not in row_value_states:
            row_value_states[eid] = [0] * len(values)
        row_frame = tk.Frame(scrollable_frame, bg="#1F1F1F", relief="solid", bd=1)
        row_frame.pack(fill="x", padx=5, pady=2, anchor="w")
        if ansicht_var.get() == "edit":
            create_bearbeiten_row(row_frame, entry, idx)
        else:
            lbl_btn = tk.Button(row_frame, text=entry["bezeichner"], anchor="w", justify="left", padx=5, pady=2)
            update_button_appearance(lbl_btn, row_bez_state[eid], is_bez=True)
            if terms:
                text_lower = lbl_btn.cget("text").lower()
                if any(term in text_lower for term in terms) and row_bez_state[eid] != 2:
                    lbl_btn.config(fg="#cc3333")
            lbl_btn.pack(side="left")
            lbl_btn.bind("<Button-1>", lambda e, eid=eid: bezeichner_single_click(e, eid))
            lbl_btn.bind("<Double-Button-1>", lambda e, eid=eid: bezeichner_double_click(e, eid))
            # Container für die Value-Buttons mit Zeilenumbruch
            value_frame = tk.Frame(row_frame, bg="#1F1F1F")
            value_frame.pack(side="left", padx=2, pady=2, fill="x")
            max_buttons_per_line = 8
            button_count = 0
            current_line = tk.Frame(value_frame, bg="#1F1F1F")
            current_line.pack(fill="x")
            for i, val in enumerate(values):
                val_text = insert_linebreaks_display(val)
                val_btn = tk.Button(current_line, text=val_text, anchor="w", justify="left", wraplength=300)
                state = row_value_states[eid][i]
                update_button_appearance(val_btn, state)
                if terms:
                    text_lower = val_btn.cget("text").lower()
                    if any(term in text_lower for term in terms) and state != 2:
                        val_btn.config(fg="#cc3333")
                val_btn.pack(side="left", padx=2, pady=2)
                val_btn.bind("<ButtonPress-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_button_press(e, eid, idx, btn))
                val_btn.bind("<ButtonRelease-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_button_release(e, eid, idx, btn))
                val_btn.bind("<Double-Button-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_double_click(eid, idx, btn))
                button_count += 1
                if button_count % max_buttons_per_line == 0:
                    current_line = tk.Frame(value_frame, bg="#1F1F1F")
                    current_line.pack(fill="x")
    if not row_added:
        label = tk.Label(scrollable_frame, text="No entries available", bg="#1F1F1F", fg="#FFA500")
        label.pack(padx=5, pady=5)
    if ansicht_var.get() == "view":
        update_toggle_button_text()

def on_close():
    if save_required:
        if messagebox.askyesnocancel("Save", "The list has been modified. Save now?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_list()
root.mainloop()
