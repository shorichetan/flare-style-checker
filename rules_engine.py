# rules_engine.py

import en_core_web_sm
import language_tool_python

# Load NLP tools
nlp = en_core_web_sm.load()
tool = language_tool_python.LanguageTool('en-US')

custom_replacements = []

def set_custom_replacements(replacements):
    global custom_replacements
    custom_replacements = replacements

def to_sentence_case(text):
    if not text:
        return text
    return text[0].upper() + text[1:].lower()

def apply_rules(text, rules):
    suggestions = []
    original_text = text

    if rules['grammar']:
        corrected = tool.correct(text)
        if corrected != text:
            suggestions.append(("Grammar", text, corrected))
            text = corrected

    if rules['custom_terms']:
        for old, new in custom_replacements:
            if old in text:
                suggestions.append(("Custom Term", text, text.replace(old, new)))
                text = text.replace(old, new)

    if rules['passive']:
        doc = nlp(text)
        for sent in doc.sents:
            if any(tok.dep_ == "auxpass" for tok in sent):
                suggestions.append(("Passive Voice", sent.text, "Use active voice"))

    if rules['future']:
        if "will " in text:
            suggestions.append(("Future Tense", text, text.replace("will ", "")))
            text = text.replace("will ", "")

    if rules['ui']:
        for term in ["OK", "Cancel", "Next", "Back", "Apply", "Save", "Close"]:
            if term in text:
                new_text = text.replace(term, f"<b>{term}</b>")
                suggestions.append(("UI Term", text, new_text))
                text = new_text

    if rules['length']:
        doc = nlp(text)
        for sent in doc.sents:
            if len(sent.text.split()) > 25:
                suggestions.append(("Long Sentence", sent.text, "Shorten it"))

    return text, suggestions

def get_nlp():
    return nlp