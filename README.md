# 📝 Flare Style Checker

**A GUI tool to scan MadCap Flare HTML content for grammar and Microsoft Style Guide (MSTP) violations.**

## ✨ Features

- Grammar correction using [LanguageTool](https://languagetool.org/)
- Passive voice detection
- Future tense avoidance
- Long sentence warnings
- UI terms bolding
- Heading case enforcement
- Custom term replacement
- Export violations as CSV

## 🖥️ GUI Preview

> (📷 Add a screenshot or GIF here!)

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shorichetan/flare-style-checker.git
   cd flare-style-checker

## 🛠 Prerequisites

Before running the Flare Style Checker, ensure the following tools are installed on your system:

### ✅ 1. Python

- **Version:** Python 3.8 or higher  
- **Download:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
- ⚠️ **Important:** During installation, check the box that says **“Add Python to PATH”**.

### ✅ 2. Java Runtime Environment (JRE)

- Required for the `language_tool_python` library (used for grammar checking)
- **Download:** [https://www.java.com/en/download/](https://www.java.com/en/download/)
- After installation, confirm with:

  ```bash
  java -version



### Python Dependencies

Open a terminal or command prompt and run the following:

- pip install -r requirements.txt
- python -m spacy download en_core_web_sm