
---

## 🧠 **HELP & USER GUIDE** – *XYZ-Promt-Node-Helper v1.0.0.45*

### 💡 **What does this program do?**
The **XYZ-Promt-Node-Helper** is a desktop application that helps you manage, edit, and organize prompt entries — ideal for users working with GUIs like **Forge**, **AUTOMATIC1111**, or **ComfyUI**.  
It lets you structure prompts clearly and switch between variations quickly.

---

### 🧰 **Main Features & How to Use**

#### ➕ **Add Entry**
- Enter a **label** (e.g., “Portrait_Prompts”) and the corresponding **prompt words**, separated by commas.
- Click **“Add”** to insert the new entry.
- Duplicate entries are automatically prevented.

#### ✏️ **Edit & Save**
- Click **“Edit”** to switch into edit mode.
- You can directly modify the labels and prompt text.
- Click **“Save”** to apply changes — a **backup** is automatically created.

#### 🗑️ **Delete Entries**
- In **View Mode**:
  - **Single-click** a label: prompt content is copied to clipboard.
  - **Double-click** a label: marks the entire entry for deletion.
  - **Double-click** a prompt value: marks only that part for deletion.
- In **Edit Mode**:
  - Check the box to mark an entry for deletion upon saving.
- Click **“Delete”** to confirm and remove all marked items.

#### 🔄 **Switch Modes**
- Toggle between:
  - **View Mode** – interactive buttons for copying parts of prompts.
  - **Edit Mode** – direct text editing of entries.

#### 📤 **Output Mode Selection**
- In the top-right corner, choose:
  - **Comma separated** – ideal for Forge, AUTOMATIC1111, etc.
  - **Line by line** – best for ComfyUI or other tools requiring separate lines.
- Affects the format when copying prompts from the interface.

#### 🔍 **Filter/Search Function**
- Enter keywords in the **filter field** to live-filter your entries.
- Comma-separated terms are treated as **OR** logic.
- Matching entries/values are **highlighted in red**.

#### 📥 **Import CSV**
- Click **“Import CSV”** (top-right).
- Expected format: `Label, Prompt1, Prompt2, ...`
- Duplicate entries are automatically skipped.
- Great for importing bulk entries from Excel or Google Sheets.

#### ✅ **Toggle All On/Off**
- Button labeled **“activate all” / “deactivate all”**:
  - Toggles activation state for all prompt values.
  - Affects what will be copied when you click a label.

#### 🕐 **Long-Press Copy**
- Hold down a prompt value button for about **2 seconds** → the value is copied to clipboard.
- Ideal for copying single words or small phrases.

#### 💾 **Automatic Backups**
- Each time you save, a backup of your data is created.
- Backups older than 30 days are automatically removed.
- Backup folder: `backup-XYZ-Promt-Node-Helper` (same folder as the script).

#### 📌 **Always on Top**
- Keeps the app window above all others.
- Toggle via checkbox in the top-right corner.

#### ❓ **Help Button**
- The **“?”** button (top-right) opens a compact in-app help window with feature summaries.

---