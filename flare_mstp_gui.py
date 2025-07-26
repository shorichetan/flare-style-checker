# flare_mstp_gui.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bs4 import BeautifulSoup
import language_tool_python
import spacy
import pandas as pd

# Load NLP tools
nlp = spacy.load("en_core_web_sm")
tool = language_tool_python.LanguageTool('en-US')

# Globals
custom_replacements = []
violations = []
INPUT_FOLDER = ""
OUTPUT_FOLDER = "cleaned_output"

# --- MSTP Rule Engine --- #

def to_sentence_case(text):
    if not text:
        return text
    return text[0].upper() + text[1:].lower()

def apply_rules(text, rules):
    global violations
    original_text = text

    if rules['grammar']:
        text = tool.correct(text)

    if rules['custom_terms']:
        for old, new in custom_replacements:
            if old in text:
                violations.append(("Custom Term", old, new, original_text))
                text = text.replace(old, new)

    if rules['passive']:
        doc = nlp(text)
        for sent in doc.sents:
            if any(tok.dep_ == "auxpass" for tok in sent):
                violations.append(("Passive Voice", sent.text, "Use active voice", original_text))

    if rules['future']:
        if "will " in text:
            violations.append(("Future Tense", "will", "Use present tense", original_text))
            text = text.replace("will ", "")

    if rules['ui']:
        for term in ["OK", "Cancel", "Next", "Back", "Apply", "Save", "Close"]:
            if term in text:
                violations.append(("UI Term", term, f"<b>{term}</b>", original_text))
                text = text.replace(term, f"<b>{term}</b>")

    if rules['length']:
        doc = nlp(text)
        for sent in doc.sents:
            if len(sent.text.split()) > 25:
                violations.append(("Long Sentence", f"{len(sent.text.split())} words", "Shorten", sent.text))

    return text

# --- File Processing --- #

def process_file(filepath, rules):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all(['p', 'li', 'td', 'th', 'span']):
        if tag.string and tag.string.strip():
            corrected = apply_rules(tag.string, rules)
            tag.string.replace_with(corrected)

    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if heading.string and rules['headings']:
            corrected = to_sentence_case(heading.string)
            if corrected != heading.string:
                violations.append(("Heading Case", heading.string, corrected, corrected))
                heading.string.replace_with(corrected)

    rel_path = os.path.relpath(filepath, INPUT_FOLDER)
    out_path = os.path.join(OUTPUT_FOLDER, rel_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# --- GUI --- #

def start_scan():
    global violations
    violations = []

    rules = {
        'grammar': grammar_var.get(),
        'passive': passive_var.get(),
        'future': future_var.get(),
        'length': length_var.get(),
        'ui': ui_var.get(),
        'headings': heading_var.get(),
        'custom_terms': custom_var.get(),
    }

    for root, _, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith(".htm") or file.endswith(".html"):
                process_file(os.path.join(root, file), rules)

    messagebox.showinfo("Done", f"Processed files saved to {OUTPUT_FOLDER}")

def select_folder():
    global INPUT_FOLDER
    INPUT_FOLDER = filedialog.askdirectory()
    folder_label.config(text=INPUT_FOLDER)

def export_log():
    if not violations:
        messagebox.showinfo("No Violations", "No style violations found.")
        return
    df = pd.DataFrame(violations, columns=["Type", "Issue", "Suggestion", "Original Text"])
    df.to_csv("violations_log.csv", index=False)
    messagebox.showinfo("Exported", "Violations log saved as violations_log.csv")

def add_custom_term():
    old = custom_entry_old.get()
    new = custom_entry_new.get()
    if old and new:
        custom_replacements.append((old, new))
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
tk.Button(action_frame, text="Export Violations Log", command=export_log).pack(side=tk.LEFT, padx=10)

root.mainloop()