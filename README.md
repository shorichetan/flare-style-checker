# Flare Style Checker

**A GUI tool to scan MadCap Flare HTML content for grammar and Microsoft Style Guide (MSTP) violations.**

---

## Features

- Grammar correction using [LanguageTool](https://languagetool.org/)
- Passive voice detection
- Future tense avoidance
- Long sentence warnings
- UI term bolding
- Heading case enforcement
- Custom term replacement
- Export violations as CSV

---

## GUI Preview

> <img width="862" height="511" alt="image" src="https://github.com/user-attachments/assets/8596825a-107b-4887-ab19-9bd5d94748f4" />


---

## Prerequisites

Make sure the following are installed on your system:

### Python (3.8 or higher)
- Download: https://www.python.org/downloads/
- Verify installation:

```bash
python --version
```

### pip (Python package manager)
Check if pip is available:

```bash
pip --version
```

### Java 17 or newer (Required for LanguageTool)

LanguageTool requires **Java 17 or above** (not Java 8).

Install from:
- https://adoptium.net/en-GB/temurin/releases/
- https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html

Verify:

```bash
java -version
```

Expected output:
```
java version "17.x.x"
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shorichetan/flare-style-checker.git
cd flare-style-checker
```

2. Install required Python libraries:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install spacy beautifulsoup4 pandas language-tool-python
python -m spacy download en_core_web_sm
```

3. Run the GUI:

```bash
python flare_mstp_gui.py
```

---

## How to Use

1. Click **"Select Folder"** to choose your HTML files.
2. Select MSTP rules you want to apply.
3. Add custom term replacements (optional).
4. Click **"Start Scan"**.
5. Cleaned files go into `cleaned_output/`.
6. Click **"Export Violations Log"** to save issues to `violations_log.csv`.

---

## Output

- Cleaned HTML → `cleaned_output/`
- Style issues report → `violations_log.csv`

---

## Contributing

Pull requests and ideas are welcome!

---

## License

MIT License


## Build Standalone Executable

To build a standalone executable with PyInstaller, run the following commands in PowerShell:

```powershell
# Clean previous builds
Get-Item -Path .\build, .\dist, .\__pycache__ -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Remove-Item -Force .\flare_mstp_gui.spec -ErrorAction SilentlyContinue

# Build the executable
pyinstaller flare_mstp_gui.py --onefile `
  --add-data "rules_engine.py;." `
  --add-data "C:/Users/shori/AppData/Local/Programs/Python/Python313/Lib/site-packages/en_core_web_sm;en_core_web_sm"
```

This will generate a standalone executable in the `dist/` directory.
