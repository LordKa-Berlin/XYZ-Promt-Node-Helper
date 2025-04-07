# Filename: XYZ-Promt-Node-Helper.py
# Version: V1.0.1.50
# Date: 2025-04-06
# Time: 17:05
# File storage name: XYZ-Promt-Node-Helper.json

import tkinter as tk

from tkinter import messagebox, filedialog, colorchooser
import os
import json
import pyperclip
import uuid
import shutil
import datetime
import time
import csv
import textwrap

VERSION = "V1.0.1.50"

# Determine the script directory and work relative to it
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(script_dir, "XYZ-Promt-Node-Helper.json")
BACKUP_DIR = os.path.join(script_dir, "backup-XYZ-Promt-Node-Helper")
COLOR_SETTINGS_FILE = os.path.join(script_dir, "backup-XYZ-Promt-Node-Helper.Colorsettings.json")

# Define original colors as a constant
ORIGINAL_COLORS = {
    "Main Background": "#1F1F1F",
    "Label Foreground": "#FFA500",
    "Entry Background": "#000000",
    "Entry Foreground": "#FFA500",
    "Entry Cursor": "#FFA500",
    "Action Button Background": "#FFA500",
    "Action Button Foreground": "#000000",
    "Delete Button Background": "red",
    "Delete Button Foreground": "#FFFFFF",
    "Bezeichner Button Normal Background": "#212121",
    "Bezeichner Button Normal Foreground": "orange",
    "Bezeichner Button Disabled Background": "#1F1F1F",
    "Value Button Normal Foreground": "#000000",
    "Value Button Normal Background": "#84672d",
    "Value Button Disabled Foreground": "#D3D3D3",
    "Button Marked for Deletion Background": "#FF0000",
    "Button Marked for Deletion Foreground": "#FFFFFF",
    "Highlight Foreground": "#cc3333"
}

# Define color variables for GUI elements
COLOR_BG_MAIN = ORIGINAL_COLORS["Main Background"]
COLOR_FG_LABEL = ORIGINAL_COLORS["Label Foreground"]
COLOR_BG_ENTRY = ORIGINAL_COLORS["Entry Background"]
COLOR_FG_ENTRY = ORIGINAL_COLORS["Entry Foreground"]
COLOR_CURSOR_ENTRY = ORIGINAL_COLORS["Entry Cursor"]
COLOR_BG_BUTTON_ACTION = ORIGINAL_COLORS["Action Button Background"]
COLOR_FG_BUTTON_ACTION = ORIGINAL_COLORS["Action Button Foreground"]
COLOR_BG_BUTTON_DELETE = ORIGINAL_COLORS["Delete Button Background"]
COLOR_FG_BUTTON_DELETE = ORIGINAL_COLORS["Delete Button Foreground"]
COLOR_BG_BUTTON_BEZ_NORMAL = ORIGINAL_COLORS["Bezeichner Button Normal Background"]
COLOR_FG_BUTTON_BEZ_NORMAL = ORIGINAL_COLORS["Bezeichner Button Normal Foreground"]
COLOR_BG_BUTTON_BEZ_DISABLED = ORIGINAL_COLORS["Bezeichner Button Disabled Background"]
COLOR_FG_BUTTON_VALUE_NORMAL = ORIGINAL_COLORS["Value Button Normal Foreground"]
COLOR_BG_BUTTON_VALUE_NORMAL = ORIGINAL_COLORS["Value Button Normal Background"]
COLOR_FG_BUTTON_VALUE_DISABLED = ORIGINAL_COLORS["Value Button Disabled Foreground"]
COLOR_BG_BUTTON_MARKED_DELETE = ORIGINAL_COLORS["Button Marked for Deletion Background"]
COLOR_FG_BUTTON_MARKED_DELETE = ORIGINAL_COLORS["Button Marked for Deletion Foreground"]
COLOR_FG_HIGHLIGHT = ORIGINAL_COLORS["Highlight Foreground"]

# Load or initialize color settings
default_colors = ORIGINAL_COLORS.copy()

if os.path.exists(COLOR_SETTINGS_FILE):
    with open(COLOR_SETTINGS_FILE, "r", encoding="utf-8") as f:
        loaded_colors = json.load(f)
    default_colors.update(loaded_colors)

# Apply loaded colors to variables
def update_color_variables():
    global COLOR_BG_MAIN, COLOR_FG_LABEL, COLOR_BG_ENTRY, COLOR_FG_ENTRY, COLOR_CURSOR_ENTRY
    global COLOR_BG_BUTTON_ACTION, COLOR_FG_BUTTON_ACTION, COLOR_BG_BUTTON_DELETE, COLOR_FG_BUTTON_DELETE
    global COLOR_BG_BUTTON_BEZ_NORMAL, COLOR_FG_BUTTON_BEZ_NORMAL, COLOR_BG_BUTTON_BEZ_DISABLED
    global COLOR_FG_BUTTON_VALUE_NORMAL, COLOR_BG_BUTTON_VALUE_NORMAL, COLOR_FG_BUTTON_VALUE_DISABLED
    global COLOR_BG_BUTTON_MARKED_DELETE, COLOR_FG_BUTTON_MARKED_DELETE, COLOR_FG_HIGHLIGHT
    COLOR_BG_MAIN = default_colors["Main Background"]
    COLOR_FG_LABEL = default_colors["Label Foreground"]
    COLOR_BG_ENTRY = default_colors["Entry Background"]
    COLOR_FG_ENTRY = default_colors["Entry Foreground"]
    COLOR_CURSOR_ENTRY = default_colors["Entry Cursor"]
    COLOR_BG_BUTTON_ACTION = default_colors["Action Button Background"]
    COLOR_FG_BUTTON_ACTION = default_colors["Action Button Foreground"]
    COLOR_BG_BUTTON_DELETE = default_colors["Delete Button Background"]
    COLOR_FG_BUTTON_DELETE = default_colors["Delete Button Foreground"]
    COLOR_BG_BUTTON_BEZ_NORMAL = default_colors["Bezeichner Button Normal Background"]
    COLOR_FG_BUTTON_BEZ_NORMAL = default_colors["Bezeichner Button Normal Foreground"]
    COLOR_BG_BUTTON_BEZ_DISABLED = default_colors["Bezeichner Button Disabled Background"]
    COLOR_FG_BUTTON_VALUE_NORMAL = default_colors["Value Button Normal Foreground"]
    COLOR_BG_BUTTON_VALUE_NORMAL = default_colors["Value Button Normal Background"]
    COLOR_FG_BUTTON_VALUE_DISABLED = default_colors["Value Button Disabled Foreground"]
    COLOR_BG_BUTTON_MARKED_DELETE = default_colors["Button Marked for Deletion Background"]
    COLOR_FG_BUTTON_MARKED_DELETE = default_colors["Button Marked for Deletion Foreground"]
    COLOR_FG_HIGHLIGHT = default_colors["Highlight Foreground"]

update_color_variables()

# Load data
data = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
for entry in data:
    if "id" not in entry:
        entry["id"] = str(uuid.uuid4())

# Global state dictionaries
row_bez_state = {}
row_value_states = {}

root = tk.Tk()
root.title("XYZ-Promt-Node-Helper")
screen_width = root.winfo_screenwidth()
root.geometry(f"{min(1800, screen_width)}x700")
root.configure(bg=COLOR_BG_MAIN)

status_var = tk.StringVar()
save_required = False
ansicht_var = tk.StringVar(value="view")
output_mode_var = tk.StringVar(value="comma")
output_mode_status_var = tk.StringVar()

def update_output_mode_status():
    if output_mode_var.get() == "comma":
        output_mode_status_var.set("Output Mode: comma separated")
    else:
        output_mode_status_var.set("Output Mode: line by line")
update_output_mode_status()

checkbox_vars = []
edit_widgets = []

def insert_linebreaks_display(text, limit=130):
    wrapped_lines = textwrap.wrap(text, width=limit)
    return "\n".join(wrapped_lines)

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

# --- Backup Functions ---
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
    files = [(os.path.join(backup_dir, f), os.path.getmtime(os.path.join(backup_dir, f)))
             for f in os.listdir(backup_dir) if f.startswith("XYZ-Promt-Node-Helper.json-")]
    files.sort(key=lambda x: x[1], reverse=True)
    to_check = files[10:]
    now = time.time()
    thirty_days = 30 * 24 * 3600
    for full_path, mtime in to_check:
        if now - mtime > thirty_days:
            os.remove(full_path)

# --- Button Appearance Update ---
def update_button_appearance(btn, state, is_bez=False):
    if state == 0:  # normal
        if is_bez:
            btn.config(bg=COLOR_BG_BUTTON_BEZ_NORMAL, fg=COLOR_FG_BUTTON_BEZ_NORMAL)
        else:
            btn.config(bg=COLOR_BG_BUTTON_VALUE_NORMAL, fg=COLOR_FG_BUTTON_VALUE_NORMAL)
    elif state == 1:  # disabled
        if is_bez:
            btn.config(bg=COLOR_BG_BUTTON_BEZ_DISABLED, fg=COLOR_FG_BUTTON_BEZ_NORMAL)
        else:
            btn.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_BUTTON_VALUE_DISABLED)
    elif state == 2:  # marked for deletion
        btn.config(bg=COLOR_BG_BUTTON_MARKED_DELETE, fg=COLOR_FG_BUTTON_MARKED_DELETE)

# --- Data Management Functions ---
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
        update_gui()

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
    update_gui()

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
        update_gui()

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

# --- View Mode Event Handlers ---
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
    update_gui()

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

# --- Edit Mode Row Creation ---
def create_bearbeiten_row(row_frame, entry, idx):
    eid = entry["id"]
    var = tk.BooleanVar()
    cb = tk.Checkbutton(row_frame, variable=var, bg=COLOR_BG_MAIN)
    cb.pack(side="left")
    checkbox_vars.append(var)
    bez_entry = tk.Entry(row_frame, width=20, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
    bez_entry.insert(0, entry["bezeichner"])
    bez_entry.pack(side="left", padx=(10, 5))
    prompt_widget = tk.Text(row_frame, height=3, width=100, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
    prompt_widget.insert("1.0", entry["prompt"])
    prompt_widget.pack(side="left")
    edit_widgets.append({
        "index": idx,
        "bez_widget": bez_entry,
        "prompt_widget": prompt_widget
    })

# --- Toggle All Values ---
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
    update_gui()

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

# --- Toggle Mode ---
def toggle_mode():
    if ansicht_var.get() == "view":
        ansicht_var.set("edit")
        toggle_mode_btn.config(text="View")
    else:
        ansicht_var.set("view")
        toggle_mode_btn.config(text="Edit")
    update_gui()

# --- Import CSV ---
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
        update_gui()
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
    tk.Button(win, text="Select File", command=select_file, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(pady=10)
    tk.Label(win, textvariable=chosen_file_var, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(pady=5)
    def do_import():
        if chosen_file_var.get():
            import_csv_file(chosen_file_var.get())
            win.destroy()
        else:
            status_var.set("No file selected.")
    tk.Button(win, text="Import", command=do_import, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(pady=10)

# --- Info Window ---
def show_info():
    info_win = tk.Toplevel(root)
    info_win.title("About XYZ-Promt-Node-Helper")
    info_win.geometry("800x600")
    info_win.configure(bg=COLOR_BG_MAIN)
    info_text = (f"""
XYZ-Promt-Node-Helper – HELP & USER GUIDE
Version: {VERSION}

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
""")
    info_label = tk.Text(info_win, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL, wrap="word", bd=0)
    info_label.insert("1.0", info_text)
    info_label.config(state="disabled")
    info_label.pack(expand=True, fill="both", padx=10, pady=10)
    tk.Button(info_win, text="Close", command=info_win.destroy, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(pady=10)

# --- Options Window ---
def open_options_window():
    options_win = tk.Toplevel(root)
    options_win.title("Color Settings")
    options_win.geometry("600x400")
    options_win.configure(bg=COLOR_BG_MAIN)

    listbox = tk.Listbox(options_win, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, selectbackground=COLOR_FG_HIGHLIGHT)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    for element in default_colors.keys():
        listbox.insert(tk.END, element)

    info_frame = tk.Frame(options_win, bg=COLOR_BG_MAIN)
    info_frame.pack(fill="x", pady=5)
    info_label = tk.Label(info_frame, text="Select an element", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL)
    info_label.pack(side="left", padx=5)

    color_before_var = tk.StringVar(value="")
    color_before_canvas = tk.Canvas(info_frame, width=20, height=20, bg=COLOR_BG_MAIN, highlightthickness=0)
    color_before_canvas.pack(side="left", padx=5)
    tk.Label(info_frame, text="Color Before:", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left")
    tk.Label(info_frame, textvariable=color_before_var, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left", padx=5)

    color_after_var = tk.StringVar(value="")
    color_after_canvas = tk.Canvas(info_frame, width=20, height=20, bg=COLOR_BG_MAIN, highlightthickness=0)
    color_after_canvas.pack(side="left", padx=5)
    tk.Label(info_frame, text="Color After:", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left")
    tk.Label(info_frame, textvariable=color_after_var, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left", padx=5)

    buttons_frame = tk.Frame(options_win, bg=COLOR_BG_MAIN)
    buttons_frame.pack(fill="x", pady=5)
    tk.Button(buttons_frame, text="Change Color", command=lambda: change_color(listbox, color_after_var, color_after_canvas),
              bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Preview", command=lambda: preview_color(listbox, color_after_var),
              bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Set", command=lambda: set_color(listbox, color_after_var),
              bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)
    tk.Button(buttons_frame, text="Reset", command=lambda: reset_colors(listbox),
              bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)

    def update_info(event):
        if listbox.curselection():
            selection = listbox.get(listbox.curselection())
            color = default_colors[selection]
            color_before_var.set(color)
            color_before_canvas.config(bg=color)
            color_after_var.set("")
            color_after_canvas.config(bg=COLOR_BG_MAIN)
            info_label.config(text=f"GUI Element: {selection}")

    listbox.bind("<<ListboxSelect>>", update_info)

def change_color(listbox, color_after_var, color_after_canvas):
    if listbox.curselection():
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            color_after_var.set(color)
            color_after_canvas.config(bg=color)

def preview_color(listbox, color_after_var):
    if listbox.curselection() and color_after_var.get():
        element = listbox.get(listbox.curselection())
        new_color = color_after_var.get()
        globals()[f"COLOR_{element.replace(' ', '_').upper()}"] = new_color
        update_gui()

def set_color(listbox, color_after_var):
    if listbox.curselection() and color_after_var.get():
        element = listbox.get(listbox.curselection())
        new_color = color_after_var.get()
        default_colors[element] = new_color
        globals()[f"COLOR_{element.replace(' ', '_').upper()}"] = new_color
        with open(COLOR_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_colors, f, indent=2)
        update_gui()
        status_var.set(f"Color for {element} set to {new_color}")

def reset_colors(listbox):
    global default_colors
    default_colors = ORIGINAL_COLORS.copy()
    update_color_variables()
    with open(COLOR_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(default_colors, f, indent=2)
    update_gui()
    status_var.set("Colors reset to defaults")
    if listbox.curselection():
        selection = listbox.get(listbox.curselection())
        color = default_colors[selection]
        listbox.event_generate("<<ListboxSelect>>")  # Trigger update_info manually

# --- GUI Setup and Update ---
def update_gui():
    update_color_variables()  # Ensure variables are synced with default_colors
    root.configure(bg=COLOR_BG_MAIN)
    top_bar.configure(bg=COLOR_BG_MAIN)
    for widget in top_bar.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL)
        elif isinstance(widget, tk.Button):
            if widget.cget("text") == "Delete":
                widget.config(bg=COLOR_BG_BUTTON_DELETE, fg=COLOR_FG_BUTTON_DELETE)
            else:
                widget.config(bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)
        elif isinstance(widget, tk.Checkbutton):
            widget.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL, selectcolor=COLOR_BG_MAIN)

    entry_frame.configure(bg=COLOR_BG_MAIN)
    for widget in entry_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL)
        elif isinstance(widget, tk.Entry):
            widget.config(bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
        elif isinstance(widget, tk.Text):
            widget.config(bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
        elif isinstance(widget, tk.Frame):
            widget.config(bg=COLOR_BG_MAIN)
            for btn in widget.winfo_children():
                if btn.cget("text") == "Delete":
                    btn.config(bg=COLOR_BG_BUTTON_DELETE, fg=COLOR_FG_BUTTON_DELETE)
                else:
                    btn.config(bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)

    second_frame.configure(bg=COLOR_BG_MAIN)
    left_frame.configure(bg=COLOR_BG_MAIN)
    for widget in left_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL)
        elif isinstance(widget, tk.Entry):
            widget.config(bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
        elif isinstance(widget, tk.Button):
            widget.config(bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)

    right_frame.configure(bg=COLOR_BG_MAIN)
    output_frame.configure(bg=COLOR_BG_MAIN)
    for widget in output_frame.winfo_children():
        if isinstance(widget, tk.Radiobutton):
            widget.config(bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL, selectcolor=COLOR_BG_MAIN)
        elif isinstance(widget, tk.Button):
            widget.config(bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)

    list_frame.configure(bg=COLOR_BG_MAIN)
    canvas.configure(bg=COLOR_BG_MAIN)
    scrollable_frame.configure(bg=COLOR_BG_MAIN)

    # Update dynamic list content
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    del checkbox_vars[:]
    del edit_widgets[:]
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
        row_frame = tk.Frame(scrollable_frame, bg=COLOR_BG_MAIN, relief="solid", bd=1)
        row_frame.pack(fill="x", padx=5, pady=2, anchor="w")
        if ansicht_var.get() == "edit":
            create_bearbeiten_row(row_frame, entry, idx)
        else:
            lbl_btn = tk.Button(row_frame, text=entry["bezeichner"], anchor="w", justify="left", padx=5, pady=2)
            update_button_appearance(lbl_btn, row_bez_state[eid], is_bez=True)
            if terms:
                text_lower = lbl_btn.cget("text").lower()
                if any(term in text_lower for term in terms) and row_bez_state[eid] != 2:
                    lbl_btn.config(fg=COLOR_FG_HIGHLIGHT)
            lbl_btn.pack(side="left")
            lbl_btn.bind("<Button-1>", lambda e, eid=eid: bezeichner_single_click(e, eid))
            lbl_btn.bind("<Double-Button-1>", lambda e, eid=eid: bezeichner_double_click(e, eid))
            value_frame = tk.Frame(row_frame, bg=COLOR_BG_MAIN)
            value_frame.pack(side="left", padx=2, pady=2, fill="x")
            max_buttons_per_line = 8
            button_count = 0
            current_line = tk.Frame(value_frame, bg=COLOR_BG_MAIN)
            current_line.pack(fill="x")
            for i, val in enumerate(values):
                val_text = insert_linebreaks_display(val)
                val_btn = tk.Button(current_line, text=val_text, anchor="w", justify="left", wraplength=300)
                state = row_value_states[eid][i]
                update_button_appearance(val_btn, state)
                if terms:
                    text_lower = val_btn.cget("text").lower()
                    if any(term in text_lower for term in terms) and state != 2:
                        val_btn.config(fg=COLOR_FG_HIGHLIGHT)
                val_btn.pack(side="left", padx=2, pady=2)
                val_btn.bind("<ButtonPress-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_button_press(e, eid, idx, btn))
                val_btn.bind("<ButtonRelease-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_button_release(e, eid, idx, btn))
                val_btn.bind("<Double-Button-1>", lambda e, eid=eid, idx=i, btn=val_btn: value_double_click(eid, idx, btn))
                button_count += 1
                if button_count % max_buttons_per_line == 0:
                    current_line = tk.Frame(value_frame, bg=COLOR_BG_MAIN)
                    current_line.pack(fill="x")
    if not row_added:
        tk.Label(scrollable_frame, text="No entries available", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(padx=5, pady=5)
    if ansicht_var.get() == "view":
        update_toggle_button_text()
    root.update_idletasks()  # Force GUI refresh

# --- GUI Setup ---
top_bar = tk.Frame(root, bg=COLOR_BG_MAIN)
top_bar.pack(fill="x")
tk.Label(top_bar, textvariable=status_var, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left", padx=10)
tk.Label(top_bar, textvariable=output_mode_status_var, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left", padx=10)
always_on_top = tk.BooleanVar(value=False)
tk.Checkbutton(top_bar, text="Always on Top", variable=always_on_top, bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL,
               command=lambda: root.wm_attributes("-topmost", always_on_top.get())).pack(side="right", padx=10)
tk.Button(top_bar, text="?", command=show_info, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION, width=3).pack(side="right", padx=10)
tk.Button(top_bar, text="Options", command=open_options_window, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="right", padx=10)
tk.Label(top_bar, text=f"Version: {VERSION}", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="right", padx=10)

entry_frame = tk.Frame(root, bg=COLOR_BG_MAIN)
entry_frame.pack(pady=10, fill="x")
tk.Label(entry_frame, text="Label:", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).grid(row=0, column=0)
bezeichner_var = tk.StringVar()
bezeichner_entry = tk.Entry(entry_frame, textvariable=bezeichner_var, width=30, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
bezeichner_entry.grid(row=0, column=1, padx=5)
tk.Label(entry_frame, text="Prompt:", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).grid(row=0, column=2)
prompt_text = tk.Text(entry_frame, height=3, width=60, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
prompt_text.grid(row=0, column=3, padx=5)
btn_frame = tk.Frame(entry_frame, bg=COLOR_BG_MAIN)
btn_frame.grid(row=0, column=4, columnspan=3, padx=5)

tk.Button(btn_frame, text="Add Entry", command=add_entry, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=2)
tk.Button(btn_frame, text="Paste", command=lambda: (prompt_text.delete("1.0", tk.END), prompt_text.insert("1.0", pyperclip.paste())), bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=2)
tk.Button(btn_frame, text="Save", command=save_data, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=2)
tk.Button(btn_frame, text="Delete", command=delete_marked, bg=COLOR_BG_BUTTON_DELETE, fg=COLOR_FG_BUTTON_DELETE).pack(side="left", padx=2)

second_frame = tk.Frame(root, bg=COLOR_BG_MAIN)
second_frame.pack(fill="x", pady=5)
left_frame = tk.Frame(second_frame, bg=COLOR_BG_MAIN)
left_frame.pack(side="left", fill="x", expand=True)
right_frame = tk.Frame(second_frame, bg=COLOR_BG_MAIN)
right_frame.pack(side="right")
toggle_mode_btn = tk.Button(left_frame, text="Edit", command=toggle_mode, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)
toggle_mode_btn.pack(side="left", padx=(10,2))
toggle_values_btn = tk.Button(left_frame, text="Deactivate All", command=toggle_all_values, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION)
toggle_values_btn.pack(side="left", padx=10)
tk.Label(left_frame, text="Filter:", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL).pack(side="left", padx=(20,2))
filter_var = tk.StringVar()
filter_entry = tk.Entry(left_frame, textvariable=filter_var, width=50, bg=COLOR_BG_ENTRY, fg=COLOR_FG_ENTRY, insertbackground=COLOR_CURSOR_ENTRY)
filter_entry.pack(side="left")
tk.Button(left_frame, text="Clear", command=lambda: filter_var.set(""), bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)
filter_var.trace_add("write", lambda *args: update_gui())

output_frame = tk.Frame(right_frame, bg=COLOR_BG_MAIN)
output_frame.pack(side="right", padx=5)
radio1 = tk.Radiobutton(output_frame, text="Output 1 comma separated\n(e.g. Forge & AUTOMATIC1111)",
                        variable=output_mode_var, value="comma", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL, selectcolor=COLOR_BG_MAIN,
                        command=lambda: (update_output_mode_status(), update_gui()))
radio1.pack(side="left", padx=5)
radio2 = tk.Radiobutton(output_frame, text="Output 2 Line by line\n(e.g. for ComfyUI-compatible nodes)",
                        variable=output_mode_var, value="line", bg=COLOR_BG_MAIN, fg=COLOR_FG_LABEL, selectcolor=COLOR_BG_MAIN,
                        command=lambda: (update_output_mode_status(), update_gui()))
radio2.pack(side="left", padx=5)
tk.Button(output_frame, text="Import CSV", command=import_csv_window, bg=COLOR_BG_BUTTON_ACTION, fg=COLOR_FG_BUTTON_ACTION).pack(side="left", padx=5)

list_frame = tk.Frame(root, bg=COLOR_BG_MAIN)
list_frame.pack(fill="both", expand=True)
canvas = tk.Canvas(list_frame, bg=COLOR_BG_MAIN, highlightthickness=0)
scrollbar_y = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollbar_x = tk.Scrollbar(list_frame, orient="horizontal", command=canvas.xview)
scrollable_frame = tk.Frame(canvas, bg=COLOR_BG_MAIN)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
canvas.pack(side="left", fill="both", expand=True)
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")

def on_close():
    if save_required:
        if messagebox.askyesnocancel("Save", "The list has been modified. Save now?"):
            save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_gui()
root.mainloop()