import os
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from rules_engine import apply_rules, to_sentence_case, set_custom_replacements

# Globals
custom_replacements = []
INPUT_FOLDER = ""

# --- File Processing --- #

def process_file(filepath, rules):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    def review_change(tag, original, suggestion):
        dialog = tk.Toplevel()
        dialog.title("Review Suggestion")
        tk.Label(dialog, text="Original:").pack(anchor="w")
        tk.Message(dialog, text=original, width=500).pack()
        tk.Label(dialog, text="Suggestion:").pack(anchor="w")
        tk.Message(dialog, text=suggestion, width=500, fg="green").pack()
        action = tk.StringVar(value="Reject")

        def accept():
            action.set("Accept")
            dialog.destroy()

        def reject():
            action.set("Reject")
            dialog.destroy()

        tk.Button(dialog, text="Accept", command=accept).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(dialog, text="Reject", command=reject).pack(side=tk.RIGHT, padx=20, pady=10)
        dialog.wait_window()
        return action.get() == "Accept"

    for tag in soup.find_all(['p', 'li', 'td', 'th', 'span']):
        if tag.string and tag.string.strip():
            corrected_text, suggestions = apply_rules(str(tag.string), rules)
            for typ, orig, suggestion in suggestions:
                if review_change(tag, orig, suggestion):
                    tag.string.replace_with(suggestion)
                    changed = True

    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if heading.string and rules['headings']:
            corrected = to_sentence_case(heading.string)
            if corrected != heading.string:
                if review_change(heading, heading.string, corrected):
                    heading.string.replace_with(corrected)
                    changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

# --- GUI --- #

def start_scan():
    rules = {
        'grammar': grammar_var.get(),
        'passive': passive_var.get(),
        'future': future_var.get(),
        'length': length_var.get(),
        'ui': ui_var.get(),
        'headings': heading_var.get(),
        'custom_terms': custom_var.get(),
    }

    set_custom_replacements(custom_replacements)

    for root, _, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith(".htm") or file.endswith(".html"):
                process_file(os.path.join(root, file), rules)

    messagebox.showinfo("Done", f"Finished scanning and updating files in place.")

def select_folder():
    global INPUT_FOLDER
    INPUT_FOLDER = filedialog.askdirectory()
    folder_label.config(text=INPUT_FOLDER)

def add_custom_term():
    old = custom_entry_old.get()
    new = custom_entry_new.get()
    if old and new:
        custom_replacements.append((old, new))
        set_custom_replacements(custom_replacements)
        custom_listbox.insert(tk.END, f"{old} → {new}")
        custom_entry_old.delete(0, tk.END)
        custom_entry_new.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("MSTP Style Checker for MadCap Flare")
root.geometry("700x500")

folder_frame = tk.Frame(root)
folder_frame.pack(pady=10)
tk.Button(folder_frame, text="Select Folder", command=select_folder).pack(side=tk.LEFT)
folder_label = tk.Label(folder_frame, text="No folder selected")
folder_label.pack(side=tk.LEFT, padx=10)

check_frame = tk.Frame(root)
check_frame.pack(pady=10)

grammar_var = tk.BooleanVar(value=True)
passive_var = tk.BooleanVar(value=True)
future_var = tk.BooleanVar(value=True)
length_var = tk.BooleanVar(value=True)
ui_var = tk.BooleanVar(value=True)
heading_var = tk.BooleanVar(value=True)
custom_var = tk.BooleanVar(value=True)

tk.Checkbutton(check_frame, text="Grammar Correction", variable=grammar_var).grid(row=0, column=0, sticky="w")
tk.Checkbutton(check_frame, text="Passive Voice", variable=passive_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(check_frame, text="Future Tense", variable=future_var).grid(row=2, column=0, sticky="w")
tk.Checkbutton(check_frame, text="Long Sentences", variable=length_var).grid(row=3, column=0, sticky="w")
tk.Checkbutton(check_frame, text="UI Term Bolding", variable=ui_var).grid(row=0, column=1, sticky="w")
tk.Checkbutton(check_frame, text="Heading Case", variable=heading_var).grid(row=1, column=1, sticky="w")
tk.Checkbutton(check_frame, text="Custom Term Replacement", variable=custom_var).grid(row=2, column=1, sticky="w")

custom_frame = tk.LabelFrame(root, text="Add Custom Replacement")
custom_frame.pack(pady=10, fill="x", padx=20)

custom_entry_old = tk.Entry(custom_frame, width=20)
custom_entry_old.pack(side=tk.LEFT, padx=5)
tk.Label(custom_frame, text="→").pack(side=tk.LEFT)
custom_entry_new = tk.Entry(custom_frame, width=20)
custom_entry_new.pack(side=tk.LEFT, padx=5)
tk.Button(custom_frame, text="Add", command=add_custom_term).pack(side=tk.LEFT, padx=5)

custom_listbox = tk.Listbox(root, height=5)
custom_listbox.pack(padx=20, pady=5, fill="x")

action_frame = tk.Frame(root)
action_frame.pack(pady=20)
tk.Button(action_frame, text="Start Scan", command=start_scan).pack(side=tk.LEFT, padx=10)

root.mainloop()
